"""
Custom Exceptions Module
Purpose: Define application-specific exceptions
"""


class BaseFileTransferException(Exception):
    """Base exception for file transfer operations."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception.
        
        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class S3OperationError(BaseFileTransferException):
    """Exception raised for S3 operation errors."""
    pass


class SFTPConnectionError(BaseFileTransferException):
    """Exception raised for SFTP connection errors."""
    pass


class SFTPOperationError(BaseFileTransferException):
    """Exception raised for SFTP operation errors."""
    pass


class FileValidationError(BaseFileTransferException):
    """Exception raised for file validation errors."""
    pass


class ConfigurationError(BaseFileTransferException):
    """Exception raised for configuration errors."""
    pass


class AuthenticationError(BaseFileTransferException):
    """Exception raised for authentication errors."""
    pass


class FileSizeLimitExceeded(BaseFileTransferException):
    """Exception raised when file size exceeds limit."""
    pass


class RetryExhausted(BaseFileTransferException):
    """Exception raised when all retry attempts are exhausted."""
    pass


class TimeoutError(BaseFileTransferException):
    """Exception raised when operation times out."""
    pass
