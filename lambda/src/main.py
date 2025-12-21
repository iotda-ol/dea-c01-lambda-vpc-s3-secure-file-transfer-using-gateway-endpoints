"""
Main Lambda Handler
Purpose: Entry point for Lambda function execution
"""

import os
import tempfile
from typing import Dict, Any

from core.logger import get_logger, StructuredLogger
from core.config import config
from core.exceptions import BaseFileTransferException
from handlers.s3_handler import S3Handler
from handlers.sftp_handler import SFTPHandler

logger = get_logger(__name__)
structured_logger = StructuredLogger(__name__, function=config.function_name)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for secure file transfer.
    
    Args:
        event: Lambda event data
        context: Lambda context object
    
    Returns:
        Response dictionary with transfer results
    """
    structured_logger.info(
        "Lambda function invoked",
        request_id=context.request_id,
        function_version=context.function_version
    )
    
    try:
        # Validate configuration
        config.validate()
        
        # Extract event parameters
        remote_file_path = event.get('remote_file_path')
        s3_key = event.get('s3_key')
        metadata = event.get('metadata', {})
        
        if not remote_file_path:
            raise ValueError("Missing required parameter: remote_file_path")
        
        structured_logger.info(
            "Processing file transfer",
            remote_file_path=remote_file_path,
            s3_key=s3_key
        )
        
        # Create temporary directory for file operations
        with tempfile.TemporaryDirectory() as temp_dir:
            local_file_path = os.path.join(temp_dir, os.path.basename(remote_file_path))
            
            # Download file from SFTP
            structured_logger.info("Downloading file from SFTP")
            with SFTPHandler() as sftp:
                sftp.download_file(remote_file_path, local_file_path)
            
            structured_logger.info("File downloaded successfully", size=os.path.getsize(local_file_path))
            
            # Upload file to S3
            structured_logger.info("Uploading file to S3")
            s3_handler = S3Handler()
            result = s3_handler.upload_file(
                local_path=local_file_path,
                s3_key=s3_key,
                metadata=metadata
            )
            
            structured_logger.info(
                "File uploaded successfully",
                s3_uri=result['s3_uri'],
                checksum=result['checksum']
            )
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': {
                'message': 'File transfer completed successfully',
                'remote_file_path': remote_file_path,
                's3_uri': result['s3_uri'],
                'checksum': result['checksum'],
                'size': result['size']
            }
        }
        
        structured_logger.info("Lambda function completed successfully")
        return response
        
    except BaseFileTransferException as e:
        structured_logger.error(
            "File transfer error",
            error=str(e),
            details=e.details
        )
        
        return {
            'statusCode': 500,
            'body': {
                'message': 'File transfer failed',
                'error': str(e),
                'details': e.details
            }
        }
        
    except Exception as e:
        structured_logger.error(
            "Unexpected error",
            error=str(e)
        )
        
        return {
            'statusCode': 500,
            'body': {
                'message': 'Unexpected error occurred',
                'error': str(e)
            }
        }
