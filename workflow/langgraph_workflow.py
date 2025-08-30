from node.general_agent_node import general_talk
from node.internet_search_node import internet_search
from langgraph.graph import StateGraph
from typing import Dict, Any, cast, Optional
from state.state import State
from utils.llm import LLMConfig
from dotenv import load_dotenv, find_dotenv
from utils.json_types import AgentType
from memories.memories import MemoryManager
from datetime import datetime

load_dotenv(find_dotenv())

class LangGraphWorkflow:
    def __init__(self, user_id, thread_id, connection_string: str = "mongodb://localhost:27017/"):
        self.user_id = user_id
        self.thread_id = thread_id
        self.memory_manager = MemoryManager(connection_string)
        self._setup()
        self.AgentType = AgentType
        self.LLMConfig = LLMConfig

    def _setup(self):
        self._init_nodes()
        self._init_graph()
        self._init_config()

    def _init_nodes(self):
        self.general_talk_node = general_talk
        self.internet_search_node = internet_search

    def _init_config(self):
        self.config = {
            "user_id": self.user_id,
            "thread_id": self.thread_id
        }

    def load_conversation_history(self, limit: int = 10) -> list:
        """Load recent conversation history from memory."""
        try:
            messages = self.memory_manager.get_conversation_messages(self.user_id, self.thread_id, limit)
            return [
                {
                    "role": message.role,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat() if message.timestamp else None
                }
                for message in messages
            ]
        except Exception as e:
            print(f"Error loading conversation history: {e}")
            return []

    def save_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Save user message to memory."""
        try:
            return self.memory_manager.save_message(self.user_id, self.thread_id, "user", content, metadata)
        except Exception as e:
            print(f"Error saving user message: {e}")
            return ""

    def save_assistant_response(self, content: str, agent_type: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Save assistant response to memory."""
        try:
            memory_metadata = {
                "agent_type": agent_type,
                **(metadata or {})
            }
            return self.memory_manager.save_message(self.user_id, self.thread_id, "assistant", content, memory_metadata)
        except Exception as e:
            print(f"Error saving assistant response: {e}")
            return ""

    def clear_conversation_history(self) -> bool:
        """Clear conversation history for this specific thread."""
        return self.memory_manager.delete_conversation(self.user_id, self.thread_id)

    def get_thread_memories(self, limit: int = 50) -> list:
        """Get all messages for this specific thread."""
        try:
            messages = self.memory_manager.get_conversation_messages(self.user_id, self.thread_id, limit)
            return [
                {
                    "role": message.role,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat() if message.timestamp else None,
                    "metadata": message.metadata
                }
                for message in messages
            ]
        except Exception as e:
            print(f"Error getting thread memories: {e}")
            return []

    def decide_agent(self, state: State) -> str:
        # Get user's input from state to decide agent
        messages = state.get('messages', [])
        current_question = state.get('user_question', '')
        
        # If no user_question, try to get from last message
        if not current_question and messages:
            last_msg = messages[-1]
            if isinstance(last_msg, dict) and last_msg.get("role") == "user":
                current_question = last_msg.get("content", "")

        # Load conversation history for context
        conversation_history = self.load_conversation_history(5)  # Last 5 messages
        history_context = ""
        if conversation_history:
            history_context = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in conversation_history[-3:]  # Last 3 for context
            ])

        # Call LLM to decide which agent to use
        prompt = f"""Given the user's question and conversation history, determine which agent would be most appropriate to handle it:
        - Use 'general' for general conversation, basic questions, or tasks not requiring external data
        - Use 'internet_search' if the question requires current information, fact checking, or web search

        Conversation History:
        {history_context}

        Current Question: {current_question}

        Respond with just the agent type: either 'general' or 'internet_search'"""

        response = LLMConfig.create_fast_config().create_llm().invoke(prompt)

        # Parse LLM response and return agent type
        response_content = response.content
        if isinstance(response_content, list):
            agent_decision_str = str(response_content[0]).strip().lower()
        else:
            agent_decision_str = str(response_content).strip().lower()
            
        if "internet_search" in agent_decision_str:
            return self.AgentType.INTERNET_SEARCH.value
        return self.AgentType.GENERAL.value

    def _agent_decider_node(self):
        def decider_node(state: State, config=None) -> State:
            # Save user message to memory first
            current_question = state.get('user_question', '')
            if current_question:
                self.save_user_message(current_question)
            
            agent_type = self.decide_agent(state)
            
            # Convert State to Dict for node functions, then back to State
            state_dict = dict(state)
            
            if agent_type == self.AgentType.GENERAL.value:
                result_dict = self.general_talk_node(state_dict)
            elif agent_type == self.AgentType.INTERNET_SEARCH.value:
                result_dict = self.internet_search_node(state_dict)
            else:
                result_dict = state_dict
            
            # Save assistant response to memory
            response = result_dict.get('response', '')
            if response:
                self.save_assistant_response(
                    str(response), 
                    agent_type, 
                    {"processing_timestamp": datetime.now().isoformat()}
                )
            
            # Convert back to State - TypedDict can be created from dict
            return cast(State, result_dict)

        return decider_node

    def _init_graph(self) -> StateGraph:
        self.graph = StateGraph(State)
        self.graph.add_node("agent_decider", self._agent_decider_node())
        self.graph.add_node("end", lambda state: state)
        self.graph.add_edge("agent_decider", "end")
        self.graph.set_entry_point("agent_decider")
        self.compiled_graph = self.graph.compile()
        return self.graph

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Load conversation history and add to messages if not already present
        if not state.get("messages"):
            conversation_history = self.load_conversation_history(10)
            state["messages"] = conversation_history
        
        # Convert input dict to State for graph processing
        state_obj: State = cast(State, {
            "messages": state.get("messages", []),
            "user_id": state.get("user_id", self.user_id),
            "user_question": state.get("user_question"),
            "query": state.get("query"),
            "response": state.get("response"),
            "search_results": state.get("search_results"),
            "timestamp": state.get("timestamp"),
            "created_at": state.get("created_at")
        })
        
        # Remove None values to keep State clean
        state_obj = cast(State, {k: v for k, v in state_obj.items() if v is not None})
        
        result = self.compiled_graph.invoke(state_obj)
        
        if isinstance(result, str):
            return {"response": result}
        return dict(result)