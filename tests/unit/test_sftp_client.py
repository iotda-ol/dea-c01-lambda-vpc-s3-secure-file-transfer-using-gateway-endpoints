"""
Unit tests for SFTP client.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import io
from src.utils.sftp_client import SFTPClient


class TestSFTPClient(unittest.TestCase):
    """Test cases for SFTPClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sftp_client = SFTPClient(
            host='localhost',
            username='testuser',
            password='testpass'
        )
    
    @patch('src.utils.sftp_client.paramiko.SSHClient')
    def test_connect_success(self, mock_ssh_client):
        """Test successful SFTP connection."""
        # Setup
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        mock_client.open_sftp.return_value = Mock()
        
        # Execute
        result = self.sftp_client.connect()
        
        # Assert
        self.assertTrue(result)
        mock_client.connect.assert_called_once()
    
    @patch('src.utils.sftp_client.paramiko.SSHClient')
    def test_list_files(self, mock_ssh_client):
        """Test listing files on SFTP server."""
        # Setup
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        mock_sftp = Mock()
        mock_client.open_sftp.return_value = mock_sftp
        mock_sftp.listdir.return_value = ['file1.txt', 'file2.txt']
        
        self.sftp_client.sftp = mock_sftp
        
        # Execute
        result = self.sftp_client.list_files('/remote/path')
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIn('file1.txt', result)
    
    @patch('src.utils.sftp_client.paramiko.SSHClient')
    def test_file_exists_true(self, mock_ssh_client):
        """Test file_exists returns True when file exists."""
        # Setup
        mock_sftp = Mock()
        mock_sftp.stat.return_value = Mock()
        self.sftp_client.sftp = mock_sftp
        
        # Execute
        result = self.sftp_client.file_exists('/remote/file.txt')
        
        # Assert
        self.assertTrue(result)
    
    @patch('src.utils.sftp_client.paramiko.SSHClient')
    def test_disconnect(self, mock_ssh_client):
        """Test SFTP disconnection."""
        # Setup
        mock_client = Mock()
        mock_sftp = Mock()
        self.sftp_client.client = mock_client
        self.sftp_client.sftp = mock_sftp
        
        # Execute
        self.sftp_client.disconnect()
        
        # Assert
        mock_sftp.close.assert_called_once()
        mock_client.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
