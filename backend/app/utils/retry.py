import time
from functools import wraps
from backend.app.utils.logger import logger


def retry(
    max_attempts: int = 3,
    delay: int = 2,
    allowed_exceptions: tuple = (Exception,)
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(1, max_attempts + 1):

                try:
                    logger.info(
                        f"Attempt {attempt} for {func.__name__}"
                    )

                    return func(*args, **kwargs)

                except allowed_exceptions as e:

                    logger.warning(
                        f"{func.__name__} failed on attempt "
                        f"{attempt}: {str(e)}"
                    )

                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after "
                            f"{max_attempts} attempts"
                        )
                        raise

                    time.sleep(delay)

        return wrapper

    return decorator