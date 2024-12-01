from groq import Groq
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_information(search_results, query):
    """
    Send web search results to the LLM for specific data extraction.
    """
    try:
        # Initialize the Groq client
        client = Groq()

        # Construct the messages for the model
        messages = [
            {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
            {"role": "user", "content": f"Extract relevant information from the following search results: {search_results}. Query: {query}"}
        ]

        # Truncate the messages if they are too long
        max_input_tokens = 4096 - 1024  # Reserve 1024 tokens for the completion
        total_chars = sum(len(msg["content"]) for msg in messages)

        if total_chars > max_input_tokens:
            logger.warning(f"Truncating input messages to fit within the token limit. Original length: {total_chars}, Max allowed: {max_input_tokens}")
            messages = [{"role": msg["role"], "content": msg["content"][:max_input_tokens]} for msg in messages]

        # Generate text using the model
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect the generated text
        generated_text = ""
        for chunk in completion:
            generated_text += chunk.choices[0].delta.content or ""

        return generated_text.strip()

    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise RuntimeError("An unexpected error occurred while processing the LLM response.")
