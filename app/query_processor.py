import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_query(prompt, entity):
    """
    Process the query by replacing the placeholder with the entity.
    """
    if entity is None:
        logger.error(f"Entity is None for prompt: {prompt}")
        raise ValueError("Entity cannot be None")
    return prompt.replace("{entity}", entity)
