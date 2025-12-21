"""
Configuration Module
Purpose: Centralized configuration management
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""
    
    # AWS Configuration
    aws_region: str = os.environ.get('AWS_REGION', 'us-east-1')
    
    # S3 Configuration
    s3_bucket: str = os.environ.get('S3_BUCKET', '')
    s3_prefix: str = os.environ.get('S3_PREFIX', 'uploads/')
    s3_storage_class: str = os.environ.get('S3_STORAGE_CLASS', 'STANDARD')
    
    # SFTP Configuration
    sftp_host: str = os.environ.get('SFTP_HOST', '')
    sftp_port: int = int(os.environ.get('SFTP_PORT', '22'))
    sftp_username: str = os.environ.get('SFTP_USERNAME', '')
    sftp_secret_name: str = os.environ.get('SFTP_SECRET_NAME', '')
    sftp_timeout: int = int(os.environ.get('SFTP_TIMEOUT', '30'))
    
    # Lambda Configuration
    function_name: str = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', '')
    function_version: str = os.environ.get('AWS_LAMBDA_FUNCTION_VERSION', '$LATEST')
    memory_limit_mb: int = int(os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', '512'))
    
    # Logging Configuration
    log_level: str = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Retry Configuration
    max_retries: int = int(os.environ.get('MAX_RETRIES', '3'))
    retry_delay: int = int(os.environ.get('RETRY_DELAY', '5'))
    
    # File Processing Configuration
    max_file_size_mb: int = int(os.environ.get('MAX_FILE_SIZE_MB', '100'))
    chunk_size_kb: int = int(os.environ.get('CHUNK_SIZE_KB', '1024'))
    
    # Feature Flags
    enable_encryption: bool = os.environ.get('ENABLE_ENCRYPTION', 'true').lower() == 'true'
    enable_compression: bool = os.environ.get('ENABLE_COMPRESSION', 'false').lower() == 'true'
    enable_virus_scan: bool = os.environ.get('ENABLE_VIRUS_SCAN', 'false').lower() == 'true'
    
    def validate(self) -> None:
        """
        Validate required configuration.
        
        Raises:
            ValueError: If required configuration is missing
        """
        required_fields = {
            's3_bucket': self.s3_bucket,
            'sftp_host': self.sftp_host,
            'sftp_username': self.sftp_username,
        }
        
        missing_fields = [k for k, v in required_fields.items() if not v]
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        return {
            'aws_region': self.aws_region,
            's3_bucket': self.s3_bucket,
            's3_prefix': self.s3_prefix,
            's3_storage_class': self.s3_storage_class,
            'sftp_host': self.sftp_host,
            'sftp_port': self.sftp_port,
            'sftp_username': self.sftp_username,
            'sftp_timeout': self.sftp_timeout,
            'function_name': self.function_name,
            'function_version': self.function_version,
            'memory_limit_mb': self.memory_limit_mb,
            'log_level': self.log_level,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'max_file_size_mb': self.max_file_size_mb,
            'chunk_size_kb': self.chunk_size_kb,
            'enable_encryption': self.enable_encryption,
            'enable_compression': self.enable_compression,
            'enable_virus_scan': self.enable_virus_scan,
        }


# Global configuration instance
config = Config()
