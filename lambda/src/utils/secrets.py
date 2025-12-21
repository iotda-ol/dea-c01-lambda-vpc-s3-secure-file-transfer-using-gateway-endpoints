"""
AWS Secrets Manager Utilities Module
Purpose: Retrieve secrets from AWS Secrets Manager
"""

import json
import boto3
from typing import Dict, Any

from core.logger import get_logger
from core.exceptions import AuthenticationError
from utils.retry import retry_with_backoff

logger = get_logger(__name__)


class SecretsManager:
    """AWS Secrets Manager utilities."""
    
    def __init__(self, region: str = 'us-east-1'):
        """
        Initialize Secrets Manager client.
        
        Args:
            region: AWS region
        """
        self.client = boto3.client('secretsmanager', region_name=region)
        self.cache = {}
    
    @retry_with_backoff(max_attempts=3, exceptions=(Exception,))
    def get_secret(self, secret_name: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Retrieve secret from AWS Secrets Manager.
        
        Args:
            secret_name: Name of the secret
            use_cache: Use cached value if available
        
        Returns:
            Secret value as dictionary
        
        Raises:
            AuthenticationError: If secret retrieval fails
        """
        # Check cache
        if use_cache and secret_name in self.cache:
            logger.debug(f"Using cached secret: {secret_name}")
            return self.cache[secret_name]
        
        try:
            logger.info(f"Retrieving secret: {secret_name}")
            response = self.client.get_secret_value(SecretId=secret_name)
            
            # Parse secret string
            if 'SecretString' in response:
                secret = json.loads(response['SecretString'])
            else:
                # Binary secret
                secret = response['SecretBinary']
            
            # Cache the secret
            if use_cache:
                self.cache[secret_name] = secret
            
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret
            
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {str(e)}")
            raise AuthenticationError(
                f"Failed to retrieve secret: {secret_name}",
                details={'secret_name': secret_name, 'error': str(e)}
            )
    
    def get_sftp_credentials(self, secret_name: str) -> Dict[str, str]:
        """
        Retrieve SFTP credentials from Secrets Manager.
        
        Args:
            secret_name: Name of the secret containing SFTP credentials
        
        Returns:
            Dictionary with 'username', 'password', and optionally 'private_key'
        """
        secret = self.get_secret(secret_name)
        
        required_keys = ['username']
        if not all(key in secret for key in required_keys):
            raise AuthenticationError(
                "Invalid SFTP credentials format",
                details={'secret_name': secret_name, 'required_keys': required_keys}
            )
        
        return secret
    
    def clear_cache(self) -> None:
        """Clear the secret cache."""
        self.cache.clear()
        logger.debug("Secret cache cleared")
