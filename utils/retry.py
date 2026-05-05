import time
from functools import wraps
from botocore.exceptions import ClientError
from utils.logger import logger

def retry_aws_call(max_retries=3, initial_backoff=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            backoff = initial_backoff
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    if error_code in ['Throttling', 'ThrottlingException', 'RequestLimitExceeded']:
                        logger.warning(f"Throttled on {func.__name__}. Retrying in {backoff} seconds...")
                        time.sleep(backoff)
                        retries += 1
                        backoff *= 2
                    else:
                        raise
            logger.error(f"Max retries reached for {func.__name__}")
            raise Exception(f"Max retries exceeded for AWS call {func.__name__}")
        return wrapper
    return decorator
