from tools.internet_search_agent import search
from state.state import State
from typing import Union



def internet_search(state: Union[State, dict]) -> dict:
    """Perform a general talk with a user using a basic llm model"""

    # Convert to dict - State is already dict-like (TypedDict)
    if hasattr(state, 'get'):
        state_dict = dict(state)
    else:
        state_dict = state

    # Get the current message
    messages = state_dict.get("messages", [])
    current_message = messages[-1]["content"] if messages else ""

    # Use general_agent tool to process the message
    response = search(current_message)

    # Add the response to messages
    if "message" not in state_dict:
        state_dict["messages"] = []

    state_dict["messages"].append({
        "role": "assistant",
        "content": response
    })

    return state_dict
