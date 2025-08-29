from workflow.langgraph_workflow import LangGraphWorkflow
from typing import Dict, Any


def main():
    # Initialize workflow with user and thread IDs
    user_id = "user123" # dummy data
    thread_id = "thread456" # dummy data
    workflow = LangGraphWorkflow(user_id=user_id, thread_id=thread_id)

    # Initialize conversation state
    conversation_state: Dict[str, Any] = {
        "messages": []
    }

    print("Chat started! Type 'quit' or 'exit' to end the conversation.")

    while True:
        # Get user input
        user_question = input("User: ").strip()

        # Check for exit conditions
        if user_question.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        if not user_question:
            continue

        # Add user message to conversation
        conversation_state["messages"].append({
            "role": "user",
            "content": user_question
        })
        conversation_state["user_question"] = user_question

        # Run the workflow
        try:
            result_state = workflow.run(conversation_state)
        except Exception as e:
            print(f"Workflow run failed: {e}")
            continue

        # Extract assistant reply
        assistant_reply = None
        if isinstance(result_state, dict):
            msgs = result_state.get("messages")
            if isinstance(msgs, list) and len(msgs) > 0:
                # Get the last assistant message
                for msg in reversed(msgs):
                    if isinstance(msg, dict) and msg.get("role") == "assistant":
                        assistant_reply = msg.get("content")
                        break
                    elif hasattr(msg, "content"):
                        assistant_reply = getattr(msg, "content", None)
                        break

            if not assistant_reply:
                assistant_reply = result_state.get("assistant_reply") or result_state.get("response")

        if assistant_reply:
            print(f"Assistant: {assistant_reply}")
            # Update conversation state with the full message history
            conversation_state = result_state if isinstance(result_state, dict) else conversation_state
        else:
            print("No response generated.")


if __name__ == "__main__":
    main()