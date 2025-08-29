from state.state import State
from tools.general_agent import general_agent
from utils.llm import LLMConfig
from dotenv import load_dotenv, find_dotenv
from typing import Dict, Any, List

load_dotenv(find_dotenv())

llm_client = LLMConfig.create_fast_config().create_llm()


def general_talk(state: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a general talk with a user using a basic llm model"""
    
    # Work with a copy to avoid modifying the original
    state_dict = state.copy()
    
    # Get the current message with proper type checking
    messages_raw = state_dict.get("messages", [])
    
    # Ensure messages is a list of dictionaries
    if not isinstance(messages_raw, list):
        messages: List[Dict[str, Any]] = []
    else:
        messages = [msg if isinstance(msg, dict) else {"role": "user", "content": str(msg)} 
                   for msg in messages_raw]
    
    # Extract current message content - prioritize user_question first
    current_message = state_dict.get("user_question", "")
    
    # If no user_question, get from last message
    if not current_message and messages:
        last_message = messages[-1]
        if "content" in last_message:
            current_message = str(last_message["content"])
    
    # Fallback to query if still no message
    if not current_message:
        current_message = state_dict.get("query", "")
    
    # Use general_agent tool to process the message
    if current_message:
        response = general_agent(current_message)
    else:
        response = "I didn't receive any message to respond to."
    
    # Ensure messages list exists
    if "messages" not in state_dict:
        state_dict["messages"] = []
    
    # Type-safe access to messages list
    messages_list = state_dict["messages"]
    if not isinstance(messages_list, list):
        messages_list = []
        state_dict["messages"] = messages_list
    
    # Add user message if it doesn't exist
    if current_message and (not messages or messages[-1].get("role") != "user"):
        messages_list.append({
            "role": "user",
            "content": current_message
        })
    
    # Add assistant response
    messages_list.append({
        "role": "assistant",
        "content": response
    })
    
    # Store the response in state
    state_dict["response"] = response
    
    return state_dict