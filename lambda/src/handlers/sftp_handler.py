"""
SFTP Handler Module
Purpose: Handle SFTP operations for file retrieval
"""

import os
import paramiko
from typing import Optional, List
from io import BytesIO

from core.logger import get_logger
from core.config import config
from core.exceptions import SFTPConnectionError, SFTPOperationError
from utils.retry import retry_with_backoff
from utils.secrets import SecretsManager

logger = get_logger(__name__)


class SFTPHandler:
    """Handle SFTP operations."""
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        Initialize SFTP handler.
        
        Args:
            host: SFTP server host
            port: SFTP server port
            username: SFTP username
            password: SFTP password
            private_key: Private key for authentication
            timeout: Connection timeout in seconds
        """
        self.host = host or config.sftp_host
        self.port = port or config.sftp_port
        self.username = username or config.sftp_username
        self.password = password
        self.private_key = private_key
        self.timeout = timeout or config.sftp_timeout
        
        self.client: Optional[paramiko.SSHClient] = None
        self.sftp: Optional[paramiko.SFTPClient] = None
        self.secrets_manager = SecretsManager(region=config.aws_region)
    
    def _load_credentials(self) -> None:
        """Load credentials from Secrets Manager if needed."""
        if not self.password and not self.private_key and config.sftp_secret_name:
            logger.info(f"Loading SFTP credentials from Secrets Manager")
            credentials = self.secrets_manager.get_sftp_credentials(config.sftp_secret_name)
            
            self.username = credentials.get('username', self.username)
            self.password = credentials.get('password')
            self.private_key = credentials.get('private_key')
    
    @retry_with_backoff(max_attempts=3, exceptions=(Exception,))
    def connect(self) -> None:
        """
        Establish SFTP connection.
        
        Raises:
            SFTPConnectionError: If connection fails
        """
        try:
            # Load credentials if needed
            self._load_credentials()
            
            logger.info(f"Connecting to SFTP server: {self.host}:{self.port}")
            
            # Create SSH client
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Prepare authentication
            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.username,
                'timeout': self.timeout
            }
            
            # Use password or private key
            if self.private_key:
                key_file = BytesIO(self.private_key.encode())
                pkey = paramiko.RSAKey.from_private_key(key_file)
                connect_kwargs['pkey'] = pkey
            elif self.password:
                connect_kwargs['password'] = self.password
            else:
                raise SFTPConnectionError(
                    "No authentication method provided (password or private key)"
                )
            
            # Connect
            self.client.connect(**connect_kwargs)
            
            # Open SFTP session
            self.sftp = self.client.open_sftp()
            
            logger.info("Successfully connected to SFTP server")
            
        except Exception as e:
            logger.error(f"Failed to connect to SFTP server: {str(e)}")
            raise SFTPConnectionError(
                f"Failed to connect to {self.host}:{self.port}",
                details={'host': self.host, 'port': self.port, 'error': str(e)}
            )
    
    def disconnect(self) -> None:
        """Close SFTP connection."""
        try:
            if self.sftp:
                self.sftp.close()
                self.sftp = None
            
            if self.client:
                self.client.close()
                self.client = None
            
            logger.info("Disconnected from SFTP server")
            
        except Exception as e:
            logger.warning(f"Error while disconnecting: {str(e)}")
    
    def download_file(self, remote_path: str, local_path: str) -> str:
        """
        Download file from SFTP server.
        
        Args:
            remote_path: Path to file on SFTP server
            local_path: Local destination path
        
        Returns:
            Path to downloaded file
        
        Raises:
            SFTPOperationError: If download fails
        """
        if not self.sftp:
            self.connect()
        
        try:
            logger.info(f"Downloading file from SFTP: {remote_path} -> {local_path}")
            
            # Create directory if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download file
            self.sftp.get(remote_path, local_path)
            
            logger.info(f"Successfully downloaded file from SFTP: {remote_path}")
            return local_path
            
        except Exception as e:
            logger.error(f"Failed to download file from SFTP: {str(e)}")
            raise SFTPOperationError(
                f"Failed to download file: {remote_path}",
                details={'remote_path': remote_path, 'local_path': local_path, 'error': str(e)}
            )
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        Upload file to SFTP server.
        
        Args:
            local_path: Path to local file
            remote_path: Destination path on SFTP server
        
        Returns:
            True if successful
        
        Raises:
            SFTPOperationError: If upload fails
        """
        if not self.sftp:
            self.connect()
        
        try:
            logger.info(f"Uploading file to SFTP: {local_path} -> {remote_path}")
            
            # Upload file
            self.sftp.put(local_path, remote_path)
            
            logger.info(f"Successfully uploaded file to SFTP: {remote_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload file to SFTP: {str(e)}")
            raise SFTPOperationError(
                f"Failed to upload file: {local_path}",
                details={'local_path': local_path, 'remote_path': remote_path, 'error': str(e)}
            )
    
    def list_files(self, remote_path: str = '.') -> List[str]:
        """
        List files in remote directory.
        
        Args:
            remote_path: Remote directory path
        
        Returns:
            List of file names
        
        Raises:
            SFTPOperationError: If listing fails
        """
        if not self.sftp:
            self.connect()
        
        try:
            logger.debug(f"Listing files in: {remote_path}")
            
            files = self.sftp.listdir(remote_path)
            logger.debug(f"Found {len(files)} files")
            
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            raise SFTPOperationError(
                f"Failed to list files in: {remote_path}",
                details={'remote_path': remote_path, 'error': str(e)}
            )
    
    def file_exists(self, remote_path: str) -> bool:
        """
        Check if file exists on SFTP server.
        
        Args:
            remote_path: Path to file on SFTP server
        
        Returns:
            True if file exists
        """
        if not self.sftp:
            self.connect()
        
        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error checking file existence: {str(e)}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
