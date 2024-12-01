import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_query(prompt, entity):
    """
    Process the query by replacing the placeholder with the entity.
    """
    try:
        return prompt.replace("{entity}", entity)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise
