"""
Basic example: Test directory transfer locally.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils import S3Client, SFTPClient, FileTransferService
from src.config import get_config


def main():
    """Test directory transfer."""
    print("Testing directory transfer...")
    
    # Get test configuration
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
    
    # Connect
    if not sftp_client.connect():
        print("Failed to connect to SFTP server")
        return
    
    try:
        # Create transfer service
        transfer_service = FileTransferService(
            sftp_client=sftp_client,
            s3_client=s3_client,
            s3_bucket=config.S3_BUCKET_NAME,
            s3_prefix='batch-uploads/'
        )
        
        # Transfer all files from directory
        remote_path = '/uploads'
        file_pattern = '*.txt'  # Only transfer .txt files
        
        results = transfer_service.transfer_directory(
            remote_path=remote_path,
            file_pattern=file_pattern
        )
        
        # Display results
        print(f"\nTransfer Results:")
        print(f"Total files: {len(results)}")
        successful = sum(1 for v in results.values() if v)
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        
        print("\nDetails:")
        for filename, success in results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {filename}")
    
    finally:
        sftp_client.disconnect()


if __name__ == '__main__':
    main()
