"""
SFTP client utility module.
Provides reusable SFTP operations for file transfer.
"""
import paramiko
from typing import Optional, List
from .logger import Logger
import io


logger = Logger.get_logger(__name__)


class SFTPClient:
    """SFTP client wrapper for file operations."""
    
    def __init__(
        self,
        host: str,
        username: str,
        port: int = 22,
        password: Optional[str] = None,
        private_key_path: Optional[str] = None
    ):
        """
        Initialize SFTP client.
        
        Args:
            host: SFTP server hostname
            username: SFTP username
            port: SFTP port (default: 22)
            password: SFTP password (optional)
            private_key_path: Path to private key file (optional)
        """
        self.host = host
        self.username = username
        self.port = port
        self.password = password
        self.private_key_path = private_key_path
        self.client = None
        self.sftp = None
    
    def connect(self) -> bool:
        """
        Establish SFTP connection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.username,
            }
            
            if self.password:
                connect_kwargs['password'] = self.password
            elif self.private_key_path:
                connect_kwargs['key_filename'] = self.private_key_path
            
            self.client.connect(**connect_kwargs)
            self.sftp = self.client.open_sftp()
            logger.info(f"Successfully connected to SFTP server {self.host}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to SFTP server: {str(e)}")
            return False
    
    def disconnect(self):
        """Close SFTP connection."""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        logger.info("SFTP connection closed")
    
    def list_files(self, remote_path: str = '.') -> List[str]:
        """
        List files in remote directory.
        
        Args:
            remote_path: Remote directory path
            
        Returns:
            List of filenames
        """
        try:
            if not self.sftp:
                raise Exception("SFTP connection not established")
            
            files = self.sftp.listdir(remote_path)
            logger.info(f"Listed {len(files)} files from {remote_path}")
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []
    
    def download_file(self, remote_path: str, local_file_obj: io.BytesIO) -> bool:
        """
        Download file from SFTP server.
        
        Args:
            remote_path: Remote file path
            local_file_obj: Local file object to write to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.sftp:
                raise Exception("SFTP connection not established")
            
            with self.sftp.open(remote_path, 'rb') as remote_file:
                local_file_obj.write(remote_file.read())
            
            local_file_obj.seek(0)
            logger.info(f"Successfully downloaded {remote_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download file: {str(e)}")
            return False
    
    def upload_file(self, local_file_obj: io.BytesIO, remote_path: str) -> bool:
        """
        Upload file to SFTP server.
        
        Args:
            local_file_obj: Local file object to upload
            remote_path: Remote file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.sftp:
                raise Exception("SFTP connection not established")
            
            with self.sftp.open(remote_path, 'wb') as remote_file:
                local_file_obj.seek(0)
                remote_file.write(local_file_obj.read())
            
            logger.info(f"Successfully uploaded to {remote_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            return False
    
    def file_exists(self, remote_path: str) -> bool:
        """
        Check if file exists on SFTP server.
        
        Args:
            remote_path: Remote file path
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            if not self.sftp:
                raise Exception("SFTP connection not established")
            
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
