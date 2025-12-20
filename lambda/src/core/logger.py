"""
Logger Module
Purpose: Centralized logging configuration for Lambda function
"""

import logging
import os
import sys
from typing import Optional


def get_logger(
    name: str,
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string
    
    Returns:
        Configured logger instance
    """
    # Get log level from environment or use provided level
    log_level = level or os.environ.get('LOG_LEVEL', 'INFO')
    
    # Default format string
    if format_string is None:
        format_string = (
            '[%(levelname)s] %(asctime)s - %(name)s - '
            '%(funcName)s:%(lineno)d - %(message)s'
        )
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger


class StructuredLogger:
    """
    Structured logging for better CloudWatch Insights queries.
    """
    
    def __init__(self, name: str, **default_fields):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
            **default_fields: Default fields to include in all log messages
        """
        self.logger = get_logger(name)
        self.default_fields = default_fields
    
    def _log(self, level: str, message: str, **fields):
        """Internal log method."""
        log_data = {**self.default_fields, **fields, 'message': message}
        log_message = ' | '.join(f'{k}={v}' for k, v in log_data.items())
        getattr(self.logger, level)(log_message)
    
    def debug(self, message: str, **fields):
        """Log debug message."""
        self._log('debug', message, **fields)
    
    def info(self, message: str, **fields):
        """Log info message."""
        self._log('info', message, **fields)
    
    def warning(self, message: str, **fields):
        """Log warning message."""
        self._log('warning', message, **fields)
    
    def error(self, message: str, **fields):
        """Log error message."""
        self._log('error', message, **fields)
    
    def critical(self, message: str, **fields):
        """Log critical message."""
        self._log('critical', message, **fields)
