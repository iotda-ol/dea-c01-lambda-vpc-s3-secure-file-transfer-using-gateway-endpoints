"""
Integration tests for file transfer service.
"""
import unittest
from unittest.mock import Mock, patch
import io
from src.utils import S3Client, SFTPClient, FileTransferService
from tests.fixtures.test_data import TestFixtures


class TestFileTransferIntegration(unittest.TestCase):
    """Integration tests for file transfer."""
    
    def setUp(self):
        """Set up test environment."""
        self.fixtures = TestFixtures()
        self.sftp_creds = self.fixtures.get_sftp_credentials()
        self.test_bucket = self.fixtures.get_test_bucket()
    
    @patch('src.utils.sftp_client.paramiko.SSHClient')
    @patch('src.utils.s3_client.boto3.client')
    def test_end_to_end_file_transfer(self, mock_s3_client, mock_ssh_client):
        """Test complete file transfer from SFTP to S3."""
        # Setup SFTP mock
        mock_ssh = Mock()
        mock_ssh_client.return_value = mock_ssh
        mock_sftp = Mock()
        mock_ssh.open_sftp.return_value = mock_sftp
        
        # Mock SFTP file read
        test_file = self.fixtures.get_sample_file('small.txt')
        mock_remote_file = Mock()
        mock_remote_file.read.return_value = test_file.read()
        mock_sftp.open.return_value.__enter__ = Mock(return_value=mock_remote_file)
        mock_sftp.open.return_value.__exit__ = Mock(return_value=False)
        
        # Setup S3 mock
        mock_s3 = Mock()
        mock_s3_client.return_value = mock_s3
        
        # Create clients
        sftp_client = SFTPClient(**self.sftp_creds)
        sftp_client.sftp = mock_sftp
        
        s3_client = S3Client()
        s3_client.client = mock_s3
        
        # Create transfer service
        transfer_service = FileTransferService(
            sftp_client=sftp_client,
            s3_client=s3_client,
            s3_bucket=self.test_bucket,
            s3_prefix='test/'
        )
        
        # Execute transfer
        result = transfer_service.transfer_file('/remote/small.txt')
        
        # Assert
        self.assertTrue(result)
        mock_s3.upload_fileobj.assert_called_once()


if __name__ == '__main__':
    unittest.main()
