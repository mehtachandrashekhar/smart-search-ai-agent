import requests
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_search(query):
    """
    Perform a web search using the SERPAPI.
    """
    api_key = st.secrets["api_keys"]["web_scraper"]
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing the API response: {e}")
        raise
