import time
import functools

def rate_limit(max_calls=1, period_seconds=1):
    """Simple rate limiter with a max number of calls and a period in seconds."""
    def decorator(func):
        calls = [0]
        last_call = [time.time()]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            elapsed_time = current_time - last_call[0]
            calls[0] += 1
            
            if elapsed_time >= period_seconds:
                last_call[0] = current_time
                calls[0] = 1
            else:
                if calls[0] > max_calls:
                    time.sleep(period_seconds - elapsed_time)
                else:
                    calls[0] += 1

            return func(*args, **kwargs)
        return wrapper
    return decorator