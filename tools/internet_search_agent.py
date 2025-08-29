import requests
import os
from prompt.internet_search_prompt import INTERNET_SEARCH_PROMPT

# Fetch the Perplexity API key from environment variables
def _fetch_perpexity_api_key():
    API = os.getenv("PERPLEXITY_API_KEY")
    if API is None:
        raise Exception("PERPLEXITY_API_KEY is not set")
    return API

# Search the web using the Perplexity API
def search(query):
    API_KEY = _fetch_perpexity_api_key()
    if API_KEY is None:
        raise ValueError("PERPLEXITY_API_KEY environment variable is not set.")

    # Prepare the API request payload
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": INTERNET_SEARCH_PROMPT
            },
            {   "role": "user",
                "content": query
            }
        ],
        "max_tokens": 500, # Limit the response length
        "temperature": 0.2, # Control the randomness of the output
        "top_p": 0.9, # Control the diversity of the output
        "return_citations": True, # Include citations in the response
        "search_domain_filter": ["perplexity.ai"], # Filter search results by domain
        "return_images": False, # Do not include images in the response
        "return_related_questions": False, # Do not include related questions in the response
        "search_recency_filter": "month" # Filter search results by recency
    }

    # Set up headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    try:
        response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)

        # Check for API errors
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        # Parse the successful response
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
   
    # Handle unexpected response format
    except (KeyError, IndexError) as e:
        raise Exception(f"Unexpected response format: {str(e)}")