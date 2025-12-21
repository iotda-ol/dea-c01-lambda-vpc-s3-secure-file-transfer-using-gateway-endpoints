"""
Unit tests for Lambda handler.
"""
import unittest
from unittest.mock import Mock, patch
import json
from src.lambda.handler import lambda_handler, validate_event


class TestLambdaHandler(unittest.TestCase):
    """Test cases for Lambda handler function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.context = Mock()
        self.test_event = {
            'remote_path': '/sftp/test/file.txt',
            's3_key': 'test/file.txt',
            'mode': 'single'
        }
    
    @patch.dict('os.environ', {
        'S3_BUCKET_NAME': 'test-bucket',
        'SFTP_HOST': 'localhost',
        'SFTP_USERNAME': 'testuser',
        'SFTP_PASSWORD': 'testpass',
        'ENVIRONMENT': 'test'
    })
    @patch('src.lambda.handler.SFTPClient')
    @patch('src.lambda.handler.S3Client')
    def test_lambda_handler_single_file_success(self, mock_s3, mock_sftp):
        """Test successful single file transfer."""
        # Setup
        mock_sftp_instance = Mock()
        mock_sftp.return_value = mock_sftp_instance
        mock_sftp_instance.connect.return_value = True
        
        mock_s3_instance = Mock()
        mock_s3.return_value = mock_s3_instance
        
        # Mock FileTransferService
        with patch('src.lambda.handler.FileTransferService') as mock_transfer:
            mock_transfer_instance = Mock()
            mock_transfer.return_value = mock_transfer_instance
            mock_transfer_instance.transfer_file.return_value = True
            
            # Execute
            response = lambda_handler(self.test_event, self.context)
            
            # Assert
            self.assertEqual(response['statusCode'], 200)
            body = json.loads(response['body'])
            self.assertIn('message', body)
    
    def test_validate_event_success(self):
        """Test event validation with valid event."""
        event = {
            'remote_path': '/test/file.txt',
            'mode': 'single'
        }
        result = validate_event(event)
        self.assertTrue(result)
    
    def test_validate_event_missing_remote_path(self):
        """Test event validation with missing remote_path."""
        event = {
            'mode': 'single'
        }
        with self.assertRaises(ValueError):
            validate_event(event)


if __name__ == '__main__':
    unittest.main()
