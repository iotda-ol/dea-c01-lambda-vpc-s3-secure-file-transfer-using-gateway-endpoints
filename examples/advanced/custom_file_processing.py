"""
Advanced example: Custom file processing with transformation.
"""
import os
import sys
import io
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils import S3Client, SFTPClient, Logger
from src.config import get_config


logger = Logger.get_logger(__name__)


class FileProcessor:
    """Advanced file processor with transformation capabilities."""
    
    def __init__(self, s3_client: S3Client, sftp_client: SFTPClient):
        self.s3_client = s3_client
        self.sftp_client = sftp_client
    
    def process_and_transfer(
        self,
        remote_path: str,
        s3_bucket: str,
        s3_key: str,
        transform_func=None
    ):
        """
        Download, transform, and upload file.
        
        Args:
            remote_path: SFTP file path
            s3_bucket: S3 bucket name
            s3_key: S3 object key
            transform_func: Optional transformation function
        """
        logger.info(f"Processing {remote_path}...")
        
        # Download from SFTP
        file_obj = io.BytesIO()
        if not self.sftp_client.download_file(remote_path, file_obj):
            logger.error("Failed to download file")
            return False
        
        # Apply transformation if provided
        if transform_func:
            file_obj.seek(0)
            content = file_obj.read()
            transformed_content = transform_func(content)
            file_obj = io.BytesIO(transformed_content)
        
        # Upload to S3
        metadata = {
            'original_filename': remote_path.split('/')[-1],
            'processed': 'true',
            'processor': 'FileProcessor'
        }
        
        if self.s3_client.upload_file(file_obj, s3_bucket, s3_key, metadata):
            logger.info("File processed and uploaded successfully")
            return True
        
        return False


def uppercase_transform(content: bytes) -> bytes:
    """Transform content to uppercase."""
    return content.decode('utf-8').upper().encode('utf-8')


def main():
    """Test advanced file processing."""
    print("Testing advanced file processing...")
    
    config = get_config('test')
    
    # Initialize clients
    s3_client = S3Client(
        region=config.S3_REGION,
        endpoint_url='http://localhost:4566'
    )
    
    sftp_client = SFTPClient(
        host=config.SFTP_HOST,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
        port=config.SFTP_PORT
    )
    
    if not sftp_client.connect():
        print("Failed to connect")
        return
    
    try:
        processor = FileProcessor(s3_client, sftp_client)
        
        # Process file with uppercase transformation
        success = processor.process_and_transfer(
            remote_path='/uploads/sample.txt',
            s3_bucket=config.S3_BUCKET_NAME,
            s3_key='processed/sample-uppercase.txt',
            transform_func=uppercase_transform
        )
        
        if success:
            print("✓ Advanced processing successful!")
        else:
            print("✗ Advanced processing failed")
    
    finally:
        sftp_client.disconnect()


if __name__ == '__main__':
    main()
