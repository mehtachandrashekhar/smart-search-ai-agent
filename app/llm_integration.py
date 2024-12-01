import requests
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_information(search_results, query):
    """
    Send web search results to the LLM for specific data extraction.
    """
    # Fetch required settings from Streamlit secrets
    api_key = st.secrets["secrets"]["GROQ_API_KEY"]
    url = st.secrets["secrets"]["GROQ_API_URL"]
    model = st.secrets["secrets"]["GROQ_MODEL"]
    max_tokens = st.secrets["secrets"]["GROQ_MAX_TOKENS"]

    # Construct the payload for the API request
    prompt = f"Extract relevant information from the following search results: {search_results}. Query: {query}"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        # Make the API request
        logger.info("Sending request to LLM API...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        # Parse and return the result
        result = response.json()
        logger.info("LLM API response received successfully.")
        return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    except requests.exceptions.RequestException as e:
        logger.error(f"LLM API request failed: {e}")
        raise RuntimeError("Failed to connect to the LLM API. Please check your API key and URL.")
    except KeyError as e:
        logger.error(f"Unexpected response structure: {e}")
        raise RuntimeError("Unexpected response from the LLM API. Please check the API configuration.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise RuntimeError("An unexpected error occurred while processing the LLM response.")
