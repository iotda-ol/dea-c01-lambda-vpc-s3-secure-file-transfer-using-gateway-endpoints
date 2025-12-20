"""
Logging utility module.
Provides centralized logging functionality for the application.
"""
import logging
import sys
from typing import Optional


class Logger:
    """Custom logger class for consistent logging across the application."""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str, level: str = 'INFO') -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name (typically __name__ of the module)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)
        
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def setup_lambda_logging(cls, level: str = 'INFO'):
        """
        Setup logging for AWS Lambda environment.
        
        Args:
            level: Logging level
        """
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)
        
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
