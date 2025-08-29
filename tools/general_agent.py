from langchain.tools import tool
from utils.llm import LLMConfig
from typing import Annotated
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm_client = LLMConfig.create_fast_config().create_llm()

@tool
def general_agent(query: Annotated[str, "The search query"]) -> str:
    """Perform a general talk with a user using a basic llm model"""

    print("[General Agent] Processing query...")

    # Use LLM to generate a response
    response = llm_client.invoke(input=query)
    print(f"Passing query to GENERAL AGENT: {response.content}")
    # Ensure the return value is always a string
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        # Join list items as string or extract string if possible
        return " ".join(str(item) for item in response.content)
    else:
        return str(response.content)