"""
Main Lambda function handler.
Orchestrates file transfer from SFTP to S3 using VPC Gateway Endpoint.
"""
import json
from typing import Dict, Any
from src.config import get_config
from src.utils import Logger, S3Client, SFTPClient, FileTransferService


# Initialize logger
logger = Logger.get_logger(__name__)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        Response dictionary with status and results
    """
    logger.info(f"Starting Lambda execution. Event: {json.dumps(event)}")
    
    try:
        # Get configuration
        config = get_config()
        Logger.setup_lambda_logging(config.LOG_LEVEL)
        
        # Validate configuration
        config.validate()
        
        # Extract parameters from event
        remote_path = event.get('remote_path', config.SFTP_REMOTE_PATH)
        file_pattern = event.get('file_pattern')
        transfer_mode = event.get('mode', 'single')  # 'single' or 'directory'
        
        # Initialize clients
        s3_client = S3Client(region=config.S3_REGION)
        sftp_client = SFTPClient(
            host=config.SFTP_HOST,
            username=config.SFTP_USERNAME,
            port=config.SFTP_PORT,
            password=config.SFTP_PASSWORD,
            private_key_path=config.SFTP_PRIVATE_KEY_PATH
        )
        
        # Connect to SFTP
        if not sftp_client.connect():
            raise Exception("Failed to connect to SFTP server")
        
        try:
            # Initialize transfer service
            transfer_service = FileTransferService(
                sftp_client=sftp_client,
                s3_client=s3_client,
                s3_bucket=config.S3_BUCKET_NAME,
                s3_prefix=config.S3_PREFIX
            )
            
            # Perform transfer based on mode
            if transfer_mode == 'directory':
                results = transfer_service.transfer_directory(
                    remote_path=remote_path,
                    file_pattern=file_pattern
                )
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Directory transfer completed',
                        'results': results,
                        'total_files': len(results),
                        'successful': sum(1 for v in results.values() if v)
                    })
                }
            else:
                # Single file transfer
                s3_key = event.get('s3_key')
                metadata = event.get('metadata')
                
                success = transfer_service.transfer_file(
                    remote_path=remote_path,
                    s3_key=s3_key,
                    metadata=metadata
                )
                
                if success:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'message': 'File transfer completed successfully',
                            'remote_path': remote_path,
                            's3_bucket': config.S3_BUCKET_NAME
                        })
                    }
                else:
                    raise Exception("File transfer failed")
        
        finally:
            # Always disconnect SFTP
            sftp_client.disconnect()
    
    except Exception as e:
        logger.error(f"Lambda execution failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error during file transfer',
                'error': str(e)
            })
        }


def validate_event(event: Dict[str, Any]) -> bool:
    """
    Validate Lambda event structure.
    
    Args:
        event: Event dictionary
        
    Returns:
        True if valid, raises Exception otherwise
    """
    if 'remote_path' not in event and 'mode' in event and event['mode'] == 'single':
        raise ValueError("remote_path is required for single file transfer")
    
    return True
