"""
Unit tests for S3 client.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import io
from src.utils.s3_client import S3Client


class TestS3Client(unittest.TestCase):
    """Test cases for S3Client class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.s3_client = S3Client(region='us-east-1')
        self.bucket = 'test-bucket'
        self.key = 'test-key.txt'
    
    @patch('src.utils.s3_client.boto3.client')
    def test_upload_file_success(self, mock_boto_client):
        """Test successful file upload."""
        # Setup
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        self.s3_client.client = mock_client
        
        file_obj = io.BytesIO(b'test content')
        
        # Execute
        result = self.s3_client.upload_file(file_obj, self.bucket, self.key)
        
        # Assert
        self.assertTrue(result)
        mock_client.upload_fileobj.assert_called_once()
    
    @patch('src.utils.s3_client.boto3.client')
    def test_upload_file_with_metadata(self, mock_boto_client):
        """Test file upload with metadata."""
        # Setup
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        self.s3_client.client = mock_client
        
        file_obj = io.BytesIO(b'test content')
        metadata = {'source': 'sftp', 'transferred_by': 'lambda'}
        
        # Execute
        result = self.s3_client.upload_file(
            file_obj, self.bucket, self.key, metadata=metadata
        )
        
        # Assert
        self.assertTrue(result)
        mock_client.upload_fileobj.assert_called_once()
    
    @patch('src.utils.s3_client.boto3.client')
    def test_file_exists_true(self, mock_boto_client):
        """Test file_exists returns True when file exists."""
        # Setup
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        self.s3_client.client = mock_client
        mock_client.head_object.return_value = {}
        
        # Execute
        result = self.s3_client.file_exists(self.bucket, self.key)
        
        # Assert
        self.assertTrue(result)
    
    @patch('src.utils.s3_client.boto3.client')
    def test_list_objects(self, mock_boto_client):
        """Test listing objects in bucket."""
        # Setup
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        self.s3_client.client = mock_client
        
        mock_client.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'file1.txt'},
                {'Key': 'file2.txt'},
            ]
        }
        
        # Execute
        result = self.s3_client.list_objects(self.bucket, prefix='')
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)


if __name__ == '__main__':
    unittest.main()
