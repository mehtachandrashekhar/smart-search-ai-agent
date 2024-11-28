import requests
import os
import logging
import time
import tiktoken

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def truncate_text(text, max_tokens, encoding_name="cl100k_base"):
    """
    Truncate the text to ensure it does not exceed the maximum allowed tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoding.decode(truncated_tokens)
    return truncated_text

def extract_information(search_results, query):
    """
    Send web search results to the LLM for specific data extraction.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable is not set.")
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    url = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    max_tokens = int(os.getenv("GROQ_MAX_TOKENS", 100))
    context_max_tokens = int(os.getenv("GROQ_CONTEXT_MAX_TOKENS", 4096))  # Set the maximum context length

    try:
        # Calculate the total token length of the messages and the completion
        encoding = tiktoken.get_encoding("cl100k_base")
        search_results_tokens = encoding.encode(search_results)
        query_tokens = encoding.encode(query)
        total_tokens = len(search_results_tokens) + len(query_tokens) + max_tokens

        # Truncate the messages if necessary
        if total_tokens > context_max_tokens:
            excess_tokens = total_tokens - context_max_tokens
            truncated_search_results = truncate_text(search_results, len(search_results_tokens) - excess_tokens)
            truncated_query = truncate_text(query, len(query_tokens) - excess_tokens)
        else:
            truncated_search_results = search_results
            truncated_query = query

        messages = [
            {"role": "user", "content": f"Extract relevant information from the following search results: {truncated_search_results}. Query: {truncated_query}"}
        ]
        payload = {"model": model, "messages": messages, "max_tokens": max_tokens}

        # Implement rate limiting
        retry_after = 0
        while True:
            response = requests.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                logger.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            elif response.status_code == 400:
                logger.error(f"API request failed: {response.text}")
                raise ValueError(f"Invalid API response: {response.text}")
            else:
                response.raise_for_status()  # Raise an error for bad status codes
                break

        response_json = response.json()
        if "choices" in response_json:
            response_content = response_json["choices"][0].get("message", {}).get("content", "")
            return response_content.strip()
        else:
            logger.error("Invalid API response")
            raise ValueError("Invalid API response")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing the API response: {e}")
        raise
