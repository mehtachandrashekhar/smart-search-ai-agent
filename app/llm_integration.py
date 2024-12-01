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
    api_key = st.secrets["secrets"]["GROQ_API_KEY"]
    url = st.secrets["secrets"]["GROQ_API_URL"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Sanitize the query by removing URLs or special characters
    sanitized_query = query.replace("https://", "").replace("www.", "")

    prompt = f"Extract relevant information from the following search results: {search_results}. Query: {sanitized_query}"

    payload = {
        "model": st.secrets["secrets"]["GROQ_MODEL"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": st.secrets["secrets"]["GROQ_MAX_TOKENS"]
    }

    try:
        # Make the POST request to the API
        response = requests.post(url, headers=headers, json=payload)
        
        # Check for successful response
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Log the successful response
        logger.info(f"API response: {response.json()}")
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        logger.error(f"Error response from API: {response.text}")
        raise
    except Exception as e:
        logger.error(f"Error processing the API response: {e}")
        raise
