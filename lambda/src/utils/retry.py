"""
Retry Utilities Module
Purpose: Provide retry logic for resilient operations
"""

import time
from typing import Callable, Any, Type, Tuple
from functools import wraps

from core.logger import get_logger
from core.exceptions import RetryExhausted

logger = get_logger(__name__)


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: int = 1,
    max_delay: int = 60,
    backoff_factor: int = 2,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        backoff_factor: Multiplier for delay after each attempt
        exceptions: Tuple of exception types to catch and retry
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = base_delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(
                        f"Attempt {attempt}/{max_attempts} for {func.__name__}"
                    )
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {str(e)}"
                    )
                    
                    if attempt < max_attempts:
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            # All attempts exhausted
            raise RetryExhausted(
                f"Failed after {max_attempts} attempts",
                details={'last_exception': str(last_exception)}
            )
        
        return wrapper
    return decorator


def retry_on_condition(
    max_attempts: int = 3,
    delay: int = 1,
    condition: Callable[[Any], bool] = lambda x: True
):
    """
    Decorator for retrying based on return value condition.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries (seconds)
        condition: Function to check if retry is needed (returns True to retry)
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                result = func(*args, **kwargs)
                
                if not condition(result):
                    return result
                
                if attempt < max_attempts:
                    logger.info(
                        f"Condition not met for {func.__name__}, "
                        f"retrying in {delay} seconds... (attempt {attempt}/{max_attempts})"
                    )
                    time.sleep(delay)
            
            logger.warning(
                f"Condition not met after {max_attempts} attempts for {func.__name__}"
            )
            return result
        
        return wrapper
    return decorator
