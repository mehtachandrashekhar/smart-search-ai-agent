import requests
import os
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
    headers = {"Authorization": f"Bearer {api_key}"}
    prompt = f"Extract relevant information from the following search results: {search_results}. Query: {query}"
    payload = {
        "model": st.secrets["secrets"]["GROQ_MODEL"],
        "prompt": prompt,
        "max_tokens": st.secrets["secrets"]["GROQ_MAX_TOKENS"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing the API response: {e}")
        raise
