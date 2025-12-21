"""
Test fixtures for integration tests.
Provides dummy accounts and test data.
"""
import io


class TestFixtures:
    """Test data fixtures."""
    
    # Dummy SFTP credentials
    DUMMY_SFTP_ACCOUNTS = {
        'account1': {
            'host': 'localhost',
            'port': 2222,
            'username': 'testuser1',
            'password': 'testpass1'
        },
        'account2': {
            'host': 'localhost',
            'port': 2222,
            'username': 'testuser2',
            'password': 'testpass2'
        }
    }
    
    # Dummy S3 buckets
    DUMMY_S3_BUCKETS = {
        'test': 'test-file-transfer-bucket',
        'dev': 'dev-file-transfer-bucket'
    }
    
    # Sample file contents
    SAMPLE_FILES = {
        'small.txt': b'This is a small test file.',
        'medium.txt': b'Medium size test content.\n' * 100,
        'large.txt': b'Large file content.\n' * 10000
    }
    
    @classmethod
    def get_sample_file(cls, filename: str) -> io.BytesIO:
        """
        Get sample file as BytesIO object.
        
        Args:
            filename: Name of sample file
            
        Returns:
            BytesIO object with file content
        """
        content = cls.SAMPLE_FILES.get(filename, b'Default content')
        return io.BytesIO(content)
    
    @classmethod
    def get_sftp_credentials(cls, account_name: str = 'account1') -> dict:
        """
        Get dummy SFTP credentials.
        
        Args:
            account_name: Name of the account
            
        Returns:
            Dictionary with SFTP credentials
        """
        return cls.DUMMY_SFTP_ACCOUNTS.get(
            account_name,
            cls.DUMMY_SFTP_ACCOUNTS['account1']
        )
    
    @classmethod
    def get_test_bucket(cls, env: str = 'test') -> str:
        """
        Get test S3 bucket name.
        
        Args:
            env: Environment name
            
        Returns:
            S3 bucket name
        """
        return cls.DUMMY_S3_BUCKETS.get(env, cls.DUMMY_S3_BUCKETS['test'])
