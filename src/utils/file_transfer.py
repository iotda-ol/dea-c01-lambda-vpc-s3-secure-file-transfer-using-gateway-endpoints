"""
File transfer service module.
Orchestrates file transfer from SFTP to S3.
"""
import io
from typing import Optional, Dict, List
from .logger import Logger
from .s3_client import S3Client
from .sftp_client import SFTPClient


logger = Logger.get_logger(__name__)


class FileTransferService:
    """Service class to handle file transfers between SFTP and S3."""
    
    def __init__(
        self,
        sftp_client: SFTPClient,
        s3_client: S3Client,
        s3_bucket: str,
        s3_prefix: str = ''
    ):
        """
        Initialize file transfer service.
        
        Args:
            sftp_client: SFTP client instance
            s3_client: S3 client instance
            s3_bucket: S3 bucket name
            s3_prefix: S3 key prefix
        """
        self.sftp_client = sftp_client
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
    
    def transfer_file(
        self,
        remote_path: str,
        s3_key: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Transfer a single file from SFTP to S3.
        
        Args:
            remote_path: Path to file on SFTP server
            s3_key: S3 object key (if None, uses filename from remote_path)
            metadata: Optional metadata to attach to S3 object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate S3 key if not provided
            if s3_key is None:
                filename = remote_path.split('/')[-1]
                s3_key = f"{self.s3_prefix}{filename}"
            else:
                s3_key = f"{self.s3_prefix}{s3_key}"
            
            logger.info(f"Starting transfer: {remote_path} -> s3://{self.s3_bucket}/{s3_key}")
            
            # Download from SFTP
            file_obj = io.BytesIO()
            if not self.sftp_client.download_file(remote_path, file_obj):
                return False
            
            # Upload to S3
            if not self.s3_client.upload_file(file_obj, self.s3_bucket, s3_key, metadata):
                return False
            
            logger.info(f"Successfully transferred file to S3")
            return True
            
        except Exception as e:
            logger.error(f"Error during file transfer: {str(e)}")
            return False
    
    def transfer_directory(
        self,
        remote_path: str,
        file_pattern: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Transfer all files from a directory on SFTP to S3.
        
        Args:
            remote_path: Path to directory on SFTP server
            file_pattern: Optional pattern to filter files
            
        Returns:
            Dictionary mapping filenames to transfer status
        """
        results = {}
        
        try:
            files = self.sftp_client.list_files(remote_path)
            
            for filename in files:
                # Apply file pattern filter if provided
                if file_pattern and not self._matches_pattern(filename, file_pattern):
                    continue
                
                file_path = f"{remote_path.rstrip('/')}/{filename}"
                success = self.transfer_file(file_path)
                results[filename] = success
            
            successful = sum(1 for v in results.values() if v)
            logger.info(f"Transfer complete: {successful}/{len(results)} files successful")
            
        except Exception as e:
            logger.error(f"Error during directory transfer: {str(e)}")
        
        return results
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """
        Check if filename matches pattern.
        
        Args:
            filename: Filename to check
            pattern: Pattern to match (supports * wildcard)
            
        Returns:
            True if matches, False otherwise
        """
        import re
        pattern_regex = pattern.replace('*', '.*')
        return bool(re.match(f"^{pattern_regex}$", filename))
