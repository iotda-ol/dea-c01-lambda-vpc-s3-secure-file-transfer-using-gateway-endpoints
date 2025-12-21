"""
Basic example: Test single file transfer locally.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils import S3Client, SFTPClient, FileTransferService
from src.config import get_config


def main():
    """Test single file transfer."""
    print("Testing single file transfer...")
    
    # Get test configuration
    config = get_config('test')
    
    # Initialize clients (using local endpoints for testing)
    s3_client = S3Client(
        region=config.S3_REGION,
        endpoint_url='http://localhost:4566'  # LocalStack
    )
    
    sftp_client = SFTPClient(
        host=config.SFTP_HOST,
        username=config.SFTP_USERNAME,
        password=config.SFTP_PASSWORD,
        port=config.SFTP_PORT
    )
    
    # Connect to SFTP
    if not sftp_client.connect():
        print("Failed to connect to SFTP server")
        return
    
    try:
        # Create transfer service
        transfer_service = FileTransferService(
            sftp_client=sftp_client,
            s3_client=s3_client,
            s3_bucket=config.S3_BUCKET_NAME,
            s3_prefix='test-uploads/'
        )
        
        # Transfer a file
        remote_path = '/uploads/test-file.txt'
        metadata = {
            'source': 'test-sftp-server',
            'environment': 'test'
        }
        
        success = transfer_service.transfer_file(
            remote_path=remote_path,
            s3_key='test-file.txt',
            metadata=metadata
        )
        
        if success:
            print("✓ File transfer successful!")
        else:
            print("✗ File transfer failed")
    
    finally:
        sftp_client.disconnect()


if __name__ == '__main__':
    main()
