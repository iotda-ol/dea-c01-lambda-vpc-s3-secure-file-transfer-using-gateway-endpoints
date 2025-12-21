"""
Secure File Transfer Lambda Function
Transfers files from legacy SFTP system to Amazon S3 via VPC Gateway Endpoint
"""

import os
import json
import logging
import boto3
from botocore.exceptions import ClientError
import paramiko
from io import BytesIO
from datetime import datetime

# Configure logging
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logger.setLevel(getattr(logging, log_level))

# Initialize AWS clients
s3_client = boto3.client('s3')
secrets_client = boto3.client('secretsmanager')

# Environment variables
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
SFTP_SECRET_ARN = os.environ.get('SFTP_SECRET_ARN')
SFTP_REMOTE_PATH = os.environ.get('SFTP_REMOTE_PATH', '/uploads')


def get_sftp_credentials():
    """
    Retrieve SFTP credentials from AWS Secrets Manager
    
    Returns:
        dict: Dictionary containing SFTP credentials
    """
    try:
        response = secrets_client.get_secret_value(SecretId=SFTP_SECRET_ARN)
        secret = json.loads(response['SecretString'])
        logger.info("Successfully retrieved SFTP credentials from Secrets Manager")
        return secret
    except ClientError as e:
        logger.error(f"Error retrieving SFTP credentials: {str(e)}")
        raise


def create_sftp_client(credentials):
    """
    Create and return an SFTP client connection
    
    Args:
        credentials (dict): SFTP credentials dictionary
        
    Returns:
        paramiko.SFTPClient: Connected SFTP client
        
    Note:
        This implementation uses AutoAddPolicy() which automatically accepts 
        any host key. In production, consider implementing proper host key 
        verification by storing known_hosts or using RejectPolicy with 
        pre-configured host keys for enhanced security.
    """
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        # Note: AutoAddPolicy() is used for compatibility but is vulnerable to MITM attacks
        # For production, consider: ssh.load_host_keys() or ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Prepare authentication
        host = credentials.get('host')
        port = credentials.get('port', 22)
        username = credentials.get('username')
        
        # Support both password and private key authentication
        password = credentials.get('password')
        private_key_str = credentials.get('private_key')
        
        if private_key_str:
            # Try to load private key (support multiple key types)
            private_key = None
            key_types = [
                ('RSA', paramiko.RSAKey),
                ('Ed25519', paramiko.Ed25519Key),
                ('ECDSA', paramiko.ECDSAKey),
                ('DSS', paramiko.DSSKey)
            ]
            
            for key_name, key_class in key_types:
                try:
                    private_key = key_class.from_private_key(BytesIO(private_key_str.encode()))
                    logger.info(f"Successfully loaded {key_name} private key")
                    break
                except Exception:
                    continue
            
            if not private_key:
                raise ValueError("Unable to load private key. Unsupported key format.")
            
            ssh.connect(hostname=host, port=port, username=username, pkey=private_key, timeout=30)
        elif password:
            # Use password authentication
            ssh.connect(hostname=host, port=port, username=username, password=password, timeout=30)
        else:
            raise ValueError("Neither password nor private_key provided in credentials")
        
        sftp = ssh.open_sftp()
        logger.info(f"Successfully connected to SFTP server: {host}:{port}")
        return sftp, ssh
        
    except Exception as e:
        logger.error(f"Error connecting to SFTP server: {str(e)}")
        raise


def transfer_file_to_s3(sftp, remote_file_path, s3_key):
    """
    Transfer a file from SFTP to S3
    
    Args:
        sftp: SFTP client
        remote_file_path (str): Path to file on SFTP server
        s3_key (str): S3 object key for the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Download file from SFTP to memory
        with BytesIO() as file_buffer:
            sftp.getfo(remote_file_path, file_buffer)
            file_buffer.seek(0)
            
            # Upload to S3
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Body=file_buffer,
                ServerSideEncryption='AES256',
                Metadata={
                    'source': 'sftp',
                    'transfer_date': datetime.utcnow().isoformat()
                }
            )
            
        logger.info(f"Successfully transferred file: {remote_file_path} -> s3://{S3_BUCKET_NAME}/{s3_key}")
        return True
        
    except ClientError as e:
        logger.error(f"S3 error transferring file {remote_file_path}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error transferring file {remote_file_path}: {str(e)}")
        return False


def list_files_in_directory(sftp, remote_path):
    """
    List files in a remote SFTP directory
    
    Args:
        sftp: SFTP client
        remote_path (str): Remote directory path
        
    Returns:
        list: List of file paths
    """
    try:
        files = []
        for entry in sftp.listdir_attr(remote_path):
            if not entry.filename.startswith('.'):  # Skip hidden files
                full_path = f"{remote_path.rstrip('/')}/{entry.filename}"
                
                # Check if it's a file
                try:
                    if sftp.stat(full_path).st_mode & 0o100000:  # Regular file
                        files.append(full_path)
                except:
                    pass
        
        logger.info(f"Found {len(files)} files in {remote_path}")
        return files
        
    except Exception as e:
        logger.error(f"Error listing files in {remote_path}: {str(e)}")
        return []


def lambda_handler(event, context):
    """
    Lambda handler function - main entry point
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        dict: Response with status and details
    """
    logger.info("Starting secure file transfer process")
    logger.info(f"Event: {json.dumps(event)}")
    
    sftp = None
    ssh = None
    
    try:
        # Validate environment variables
        if not S3_BUCKET_NAME:
            raise ValueError("S3_BUCKET_NAME environment variable not set")
        if not SFTP_SECRET_ARN:
            raise ValueError("SFTP_SECRET_ARN environment variable not set")
        
        # Get SFTP credentials
        credentials = get_sftp_credentials()
        
        # Connect to SFTP server
        sftp, ssh = create_sftp_client(credentials)
        
        # Get list of files to transfer
        files_to_transfer = list_files_in_directory(sftp, SFTP_REMOTE_PATH)
        
        if not files_to_transfer:
            logger.info("No files found to transfer")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No files to transfer',
                    'files_transferred': 0
                })
            }
        
        # Transfer files
        successful_transfers = 0
        failed_transfers = 0
        transferred_files = []
        
        for file_path in files_to_transfer:
            # Create S3 key (preserve directory structure)
            s3_key = file_path.lstrip('/')
            
            if transfer_file_to_s3(sftp, file_path, s3_key):
                successful_transfers += 1
                transferred_files.append(s3_key)
            else:
                failed_transfers += 1
        
        logger.info(f"Transfer complete. Successful: {successful_transfers}, Failed: {failed_transfers}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File transfer completed',
                'files_transferred': successful_transfers,
                'files_failed': failed_transfers,
                'transferred_files': transferred_files
            })
        }
        
    except Exception as e:
        logger.error(f"Error in file transfer process: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'File transfer failed',
                'error': str(e)
            })
        }
        
    finally:
        # Clean up connections
        if sftp:
            try:
                sftp.close()
            except:
                pass
        if ssh:
            try:
                ssh.close()
            except:
                pass
        
        logger.info("File transfer process completed")
