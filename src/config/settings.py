"""
Configuration settings for the S3 file transfer Lambda function.
Centralizes all configuration parameters for easy management.
"""
import os
from typing import Optional


class Config:
    """Base configuration class with common settings."""
    
    # S3 Configuration
    S3_BUCKET_NAME: str = os.getenv('S3_BUCKET_NAME', '')
    S3_PREFIX: str = os.getenv('S3_PREFIX', 'uploads/')
    S3_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    
    # VPC Configuration
    VPC_ID: str = os.getenv('VPC_ID', '')
    SUBNET_IDS: list = os.getenv('SUBNET_IDS', '').split(',')
    SECURITY_GROUP_IDS: list = os.getenv('SECURITY_GROUP_IDS', '').split(',')
    
    # SFTP Configuration
    SFTP_HOST: str = os.getenv('SFTP_HOST', '')
    SFTP_PORT: int = int(os.getenv('SFTP_PORT', '22'))
    SFTP_USERNAME: str = os.getenv('SFTP_USERNAME', '')
    SFTP_PASSWORD: Optional[str] = os.getenv('SFTP_PASSWORD')
    SFTP_PRIVATE_KEY_PATH: Optional[str] = os.getenv('SFTP_PRIVATE_KEY_PATH')
    SFTP_REMOTE_PATH: str = os.getenv('SFTP_REMOTE_PATH', '/')
    
    # Transfer Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv('MAX_FILE_SIZE_MB', '100'))
    CHUNK_SIZE_MB: int = int(os.getenv('CHUNK_SIZE_MB', '5'))
    TRANSFER_TIMEOUT_SECONDS: int = int(os.getenv('TRANSFER_TIMEOUT_SECONDS', '300'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Retry Configuration
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_BACKOFF_FACTOR: int = int(os.getenv('RETRY_BACKOFF_FACTOR', '2'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration parameters."""
        required_fields = [
            'S3_BUCKET_NAME',
            'SFTP_HOST',
            'SFTP_USERNAME',
        ]
        
        for field in required_fields:
            if not getattr(cls, field):
                raise ValueError(f"Missing required configuration: {field}")
        
        return True


class DevelopmentConfig(Config):
    """Development environment configuration."""
    LOG_LEVEL: str = 'DEBUG'
    S3_BUCKET_NAME: str = os.getenv('S3_BUCKET_NAME', 'dev-file-transfer-bucket')


class ProductionConfig(Config):
    """Production environment configuration."""
    LOG_LEVEL: str = 'WARNING'
    MAX_FILE_SIZE_MB: int = int(os.getenv('MAX_FILE_SIZE_MB', '500'))


class TestConfig(Config):
    """Test environment configuration."""
    LOG_LEVEL: str = 'DEBUG'
    S3_BUCKET_NAME: str = 'test-file-transfer-bucket'
    SFTP_HOST: str = 'localhost'
    SFTP_PORT: int = 2222
    SFTP_USERNAME: str = 'testuser'
    SFTP_PASSWORD: str = 'testpass'
    SFTP_REMOTE_PATH: str = '/uploads'


def get_config(env: str = None) -> Config:
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name (development, production, test)
        
    Returns:
        Configuration object
    """
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestConfig,
    }
    
    return configs.get(env.lower(), DevelopmentConfig)
