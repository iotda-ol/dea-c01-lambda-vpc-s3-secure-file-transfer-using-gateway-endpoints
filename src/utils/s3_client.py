"""
S3 client utility module.
Provides reusable S3 operations with proper error handling.
"""
import boto3
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from .logger import Logger


logger = Logger.get_logger(__name__)


class S3Client:
    """S3 client wrapper for file operations."""
    
    def __init__(self, region: str = 'us-east-1', endpoint_url: Optional[str] = None):
        """
        Initialize S3 client.
        
        Args:
            region: AWS region
            endpoint_url: Optional custom endpoint URL (for testing)
        """
        self.region = region
        self.endpoint_url = endpoint_url
        self.client = self._create_client()
    
    def _create_client(self):
        """Create boto3 S3 client."""
        config_params = {'region_name': self.region}
        if self.endpoint_url:
            config_params['endpoint_url'] = self.endpoint_url
        
        return boto3.client('s3', **config_params)
    
    def upload_file(
        self,
        file_obj: BinaryIO,
        bucket: str,
        key: str,
        metadata: Optional[dict] = None
    ) -> bool:
        """
        Upload file to S3.
        
        Args:
            file_obj: File object to upload
            bucket: S3 bucket name
            key: S3 object key
            metadata: Optional metadata dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata
            
            self.client.upload_fileobj(file_obj, bucket, key, ExtraArgs=extra_args)
            logger.info(f"Successfully uploaded file to s3://{bucket}/{key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {str(e)}")
            return False
    
    def download_file(self, bucket: str, key: str, file_obj: BinaryIO) -> bool:
        """
        Download file from S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            file_obj: File object to write to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.download_fileobj(bucket, key, file_obj)
            logger.info(f"Successfully downloaded file from s3://{bucket}/{key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to download file from S3: {str(e)}")
            return False
    
    def file_exists(self, bucket: str, key: str) -> bool:
        """
        Check if file exists in S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            return False
    
    def list_objects(self, bucket: str, prefix: str = '') -> list:
        """
        List objects in S3 bucket.
        
        Args:
            bucket: S3 bucket name
            prefix: Optional prefix filter
            
        Returns:
            List of object keys
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return []
            
            return [obj['Key'] for obj in response['Contents']]
            
        except ClientError as e:
            logger.error(f"Failed to list objects: {str(e)}")
            return []
    
    def delete_object(self, bucket: str, key: str) -> bool:
        """
        Delete object from S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            logger.info(f"Successfully deleted s3://{bucket}/{key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete object: {str(e)}")
            return False
