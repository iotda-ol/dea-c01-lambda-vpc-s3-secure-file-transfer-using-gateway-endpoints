"""
S3 Handler Module
Purpose: Handle S3 operations for file transfer
"""

import os
import boto3
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError

from core.logger import get_logger
from core.config import config
from core.exceptions import S3OperationError
from utils.retry import retry_with_backoff
from utils.validators import FileValidator

logger = get_logger(__name__)


class S3Handler:
    """Handle S3 operations."""
    
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize S3 handler.
        
        Args:
            bucket_name: S3 bucket name (defaults to config)
            region: AWS region (defaults to config)
        """
        self.bucket_name = bucket_name or config.s3_bucket
        self.region = region or config.aws_region
        self.client = boto3.client('s3', region_name=self.region)
        self.validator = FileValidator(max_size_mb=config.max_file_size_mb)
    
    @retry_with_backoff(max_attempts=3, exceptions=(ClientError,))
    def upload_file(
        self,
        local_path: str,
        s3_key: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        storage_class: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload file to S3.
        
        Args:
            local_path: Path to local file
            s3_key: S3 object key (defaults to filename with prefix)
            metadata: Custom metadata
            storage_class: S3 storage class
        
        Returns:
            Upload result with S3 URL and metadata
        
        Raises:
            S3OperationError: If upload fails
        """
        try:
            # Validate file
            self.validator.validate(local_path)
            
            # Generate S3 key if not provided
            if s3_key is None:
                filename = os.path.basename(local_path)
                s3_key = f"{config.s3_prefix}{filename}"
            
            # Calculate checksum
            checksum = FileValidator.calculate_checksum(local_path)
            
            # Prepare metadata
            upload_metadata = metadata or {}
            upload_metadata['checksum'] = checksum
            
            # Prepare extra args
            extra_args = {
                'Metadata': upload_metadata,
                'StorageClass': storage_class or config.s3_storage_class
            }
            
            # Enable server-side encryption
            if config.enable_encryption:
                extra_args['ServerSideEncryption'] = 'AES256'
            
            logger.info(f"Uploading file to S3: {local_path} -> s3://{self.bucket_name}/{s3_key}")
            
            # Upload file
            self.client.upload_file(
                Filename=local_path,
                Bucket=self.bucket_name,
                Key=s3_key,
                ExtraArgs=extra_args
            )
            
            logger.info(f"Successfully uploaded file to S3: {s3_key}")
            
            return {
                'bucket': self.bucket_name,
                'key': s3_key,
                's3_uri': f"s3://{self.bucket_name}/{s3_key}",
                'checksum': checksum,
                'size': os.path.getsize(local_path),
                'storage_class': extra_args['StorageClass']
            }
            
        except Exception as e:
            logger.error(f"Failed to upload file to S3: {str(e)}")
            raise S3OperationError(
                f"Failed to upload file: {local_path}",
                details={'local_path': local_path, 's3_key': s3_key, 'error': str(e)}
            )
    
    @retry_with_backoff(max_attempts=3, exceptions=(ClientError,))
    def download_file(self, s3_key: str, local_path: str) -> str:
        """
        Download file from S3.
        
        Args:
            s3_key: S3 object key
            local_path: Local destination path
        
        Returns:
            Path to downloaded file
        
        Raises:
            S3OperationError: If download fails
        """
        try:
            logger.info(f"Downloading file from S3: s3://{self.bucket_name}/{s3_key} -> {local_path}")
            
            # Create directory if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download file
            self.client.download_file(
                Bucket=self.bucket_name,
                Key=s3_key,
                Filename=local_path
            )
            
            logger.info(f"Successfully downloaded file from S3: {s3_key}")
            return local_path
            
        except Exception as e:
            logger.error(f"Failed to download file from S3: {str(e)}")
            raise S3OperationError(
                f"Failed to download file: {s3_key}",
                details={'s3_key': s3_key, 'local_path': local_path, 'error': str(e)}
            )
    
    @retry_with_backoff(max_attempts=3, exceptions=(ClientError,))
    def get_object_metadata(self, s3_key: str) -> Dict[str, Any]:
        """
        Get object metadata from S3.
        
        Args:
            s3_key: S3 object key
        
        Returns:
            Object metadata
        
        Raises:
            S3OperationError: If operation fails
        """
        try:
            logger.debug(f"Getting metadata for S3 object: {s3_key}")
            
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            return {
                'size': response['ContentLength'],
                'last_modified': response['LastModified'],
                'etag': response['ETag'],
                'metadata': response.get('Metadata', {})
            }
            
        except Exception as e:
            logger.error(f"Failed to get metadata for S3 object: {str(e)}")
            raise S3OperationError(
                f"Failed to get metadata: {s3_key}",
                details={'s3_key': s3_key, 'error': str(e)}
            )
    
    def delete_file(self, s3_key: str) -> bool:
        """
        Delete file from S3.
        
        Args:
            s3_key: S3 object key
        
        Returns:
            True if successful
        
        Raises:
            S3OperationError: If deletion fails
        """
        try:
            logger.info(f"Deleting file from S3: {s3_key}")
            
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            logger.info(f"Successfully deleted file from S3: {s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file from S3: {str(e)}")
            raise S3OperationError(
                f"Failed to delete file: {s3_key}",
                details={'s3_key': s3_key, 'error': str(e)}
            )
    
    def list_objects(self, prefix: Optional[str] = None, max_keys: int = 1000) -> list:
        """
        List objects in S3 bucket.
        
        Args:
            prefix: Object key prefix filter
            max_keys: Maximum number of keys to return
        
        Returns:
            List of object keys
        """
        try:
            prefix = prefix or config.s3_prefix
            logger.debug(f"Listing objects with prefix: {prefix}")
            
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            objects = [obj['Key'] for obj in response.get('Contents', [])]
            logger.debug(f"Found {len(objects)} objects")
            
            return objects
            
        except Exception as e:
            logger.error(f"Failed to list objects: {str(e)}")
            raise S3OperationError(
                "Failed to list objects",
                details={'prefix': prefix, 'error': str(e)}
            )
