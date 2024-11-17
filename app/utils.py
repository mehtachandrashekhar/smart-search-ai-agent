# app/utils.py
import time

def rate_limit(delay=1):
    """Simple rate limiter with a delay in seconds."""
    time.sleep(delay)
