"""
File Validation Utilities Module
Purpose: Validate files before processing
"""

import os
import hashlib
from typing import Optional, List

from core.logger import get_logger
from core.exceptions import FileValidationError, FileSizeLimitExceeded

logger = get_logger(__name__)


class FileValidator:
    """File validation utilities."""
    
    def __init__(self, max_size_mb: int = 100, allowed_extensions: Optional[List[str]] = None):
        """
        Initialize file validator.
        
        Args:
            max_size_mb: Maximum file size in MB
            allowed_extensions: List of allowed file extensions (None = all allowed)
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_extensions = allowed_extensions or []
    
    def validate_size(self, file_path: str) -> bool:
        """
        Validate file size.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if valid
        
        Raises:
            FileSizeLimitExceeded: If file exceeds size limit
        """
        file_size = os.path.getsize(file_path)
        
        if file_size > self.max_size_bytes:
            raise FileSizeLimitExceeded(
                f"File size {file_size} exceeds limit {self.max_size_bytes}",
                details={
                    'file_size': file_size,
                    'max_size': self.max_size_bytes,
                    'file_path': file_path
                }
            )
        
        logger.debug(f"File size validation passed: {file_size} bytes")
        return True
    
    def validate_extension(self, file_path: str) -> bool:
        """
        Validate file extension.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if valid
        
        Raises:
            FileValidationError: If extension not allowed
        """
        if not self.allowed_extensions:
            return True
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext not in self.allowed_extensions:
            raise FileValidationError(
                f"File extension {ext} not allowed",
                details={
                    'extension': ext,
                    'allowed_extensions': self.allowed_extensions,
                    'file_path': file_path
                }
            )
        
        logger.debug(f"File extension validation passed: {ext}")
        return True
    
    def validate(self, file_path: str) -> bool:
        """
        Validate file (size and extension).
        
        Args:
            file_path: Path to file
        
        Returns:
            True if all validations pass
        """
        self.validate_size(file_path)
        self.validate_extension(file_path)
        return True
    
    @staticmethod
    def calculate_checksum(file_path: str, algorithm: str = 'sha256') -> str:
        """
        Calculate file checksum.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256)
        
        Returns:
            Hexadecimal checksum string
        """
        hash_func = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        checksum = hash_func.hexdigest()
        logger.debug(f"Calculated {algorithm} checksum: {checksum}")
        return checksum
    
    @staticmethod
    def verify_checksum(file_path: str, expected_checksum: str, algorithm: str = 'sha256') -> bool:
        """
        Verify file checksum.
        
        Args:
            file_path: Path to file
            expected_checksum: Expected checksum value
            algorithm: Hash algorithm
        
        Returns:
            True if checksum matches
        
        Raises:
            FileValidationError: If checksum doesn't match
        """
        actual_checksum = FileValidator.calculate_checksum(file_path, algorithm)
        
        if actual_checksum != expected_checksum:
            raise FileValidationError(
                "Checksum verification failed",
                details={
                    'expected': expected_checksum,
                    'actual': actual_checksum,
                    'algorithm': algorithm,
                    'file_path': file_path
                }
            )
        
        logger.debug("Checksum verification passed")
        return True
