import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_query(prompt, entity):
    """
    Process the query by replacing the {entity} placeholder in the prompt with the actual entity.
    Args:
        prompt (str): The prompt containing the {entity} placeholder.
        entity (str): The entity to replace the placeholder.
    Returns:
        str: The formatted query with the placeholder replaced.
    Raises:
        ValueError: If the placeholder is not found in the prompt.
        Exception: For unexpected processing errors.
    """
    try:
        # Validate that the placeholder exists in the prompt
        if "{entity}" not in prompt:
            raise ValueError("The prompt does not contain the {entity} placeholder.")
        
        # Replace placeholder with the entity
        formatted_query = prompt.replace("{entity}", entity)
        logger.info(f"Processed query: {formatted_query}")
        return formatted_query
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing query: {e}")
        raise
