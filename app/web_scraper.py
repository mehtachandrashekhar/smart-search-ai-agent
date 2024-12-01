import requests
import logging
import streamlit as st
from app.utils import rate_limit

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@rate_limit(max_calls=5, period_seconds=10)
def perform_search(query):
    """
    Perform a web search using the SERPAPI.
    """
    # Fetch the API key from Streamlit secrets
    api_key = st.secrets["api_keys"]["web_scraper"]
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key
    }

    try:
        # Log the query being searched
        logger.info(f"Performing search for query: {query}")

        # Make the GET request to the SerpAPI
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad status codes

        # Log and return the JSON response
        logger.info("Search request successful.")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise RuntimeError("Failed to fetch search results due to an HTTP error.")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        raise RuntimeError("Failed to connect to the web search API. Please check your network.")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        raise RuntimeError("The web search API timed out. Try again later.")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise RuntimeError("An error occurred while fetching search results.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise RuntimeError("An unexpected error occurred. Please try again.")