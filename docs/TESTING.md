# Testing Guide

## Overview

This project includes comprehensive testing infrastructure with:
- Unit tests for individual components
- Integration tests for end-to-end workflows
- Test fixtures with dummy accounts
- Local testing environment
- Mock services for AWS and SFTP

## Test Structure

```
tests/
├── __init__.py
├── unit/                       # Unit tests
│   ├── test_s3_client.py      # S3 client tests
│   ├── test_sftp_client.py    # SFTP client tests
│   └── test_lambda_handler.py # Lambda handler tests
├── integration/                # Integration tests
│   └── test_file_transfer_integration.py
└── fixtures/                   # Test data
    └── test_data.py           # Dummy accounts & data
```

## Running Tests

### All Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run using script
./scripts/run_tests.sh
```

### Specific Test Suites

```bash
# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests only
python -m pytest tests/integration/ -v

# Specific test file
python -m pytest tests/unit/test_s3_client.py -v

# Specific test method
python -m pytest tests/unit/test_s3_client.py::TestS3Client::test_upload_file_success -v
```

### Test Options

```bash
# Verbose output
python -m pytest tests/ -v

# Show print statements
python -m pytest tests/ -s

# Stop on first failure
python -m pytest tests/ -x

# Run last failed tests
python -m pytest tests/ --lf

# Run tests matching pattern
python -m pytest tests/ -k "test_upload"
```

## Test Fixtures

### Dummy SFTP Accounts

Located in `tests/fixtures/test_data.py`:

```python
from tests.fixtures.test_data import TestFixtures

# Get SFTP credentials
creds = TestFixtures.get_sftp_credentials('account1')
# Returns: {'host': 'localhost', 'port': 2222, 'username': 'testuser1', ...}

# Get test bucket
bucket = TestFixtures.get_test_bucket('test')
# Returns: 'test-file-transfer-bucket'

# Get sample file
file_obj = TestFixtures.get_sample_file('small.txt')
# Returns: BytesIO object with test content
```

### Available Test Accounts

```python
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
```

### Sample Test Files

```python
SAMPLE_FILES = {
    'small.txt': b'This is a small test file.',
    'medium.txt': b'Medium size test content.\n' * 100,
    'large.txt': b'Large file content.\n' * 10000
}
```

## Local Testing Environment

### Setup

1. **Start SFTP Server:**
```bash
./scripts/start_local_sftp.sh
```

2. **Start LocalStack:**
```bash
pip install localstack
localstack start -d
```

3. **Create Test Bucket:**
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://test-file-transfer-bucket
```

### Verify Setup

```bash
# Check SFTP server
docker ps | grep sftp

# Check LocalStack
aws --endpoint-url=http://localhost:4566 s3 ls

# Test SFTP connection
sftp -P 2222 testuser@localhost
```

## Unit Tests

### S3 Client Tests

```bash
python -m pytest tests/unit/test_s3_client.py -v
```

**Test Coverage:**
- File upload with/without metadata
- File download
- File existence check
- List objects
- Delete object
- Error handling

### SFTP Client Tests

```bash
python -m pytest tests/unit/test_sftp_client.py -v
```

**Test Coverage:**
- Connection establishment
- File listing
- File upload/download
- File existence check
- Disconnection
- Error handling

### Lambda Handler Tests

```bash
python -m pytest tests/unit/test_lambda_handler.py -v
```

**Test Coverage:**
- Single file transfer
- Directory transfer
- Event validation
- Error scenarios
- Response format

## Integration Tests

### File Transfer Integration

```bash
python -m pytest tests/integration/test_file_transfer_integration.py -v
```

**Test Coverage:**
- End-to-end file transfer
- SFTP to S3 workflow
- Multiple file transfers
- Error recovery

## Writing New Tests

### Unit Test Example

```python
import unittest
from unittest.mock import Mock, patch
from src.utils.s3_client import S3Client


class TestMyFeature(unittest.TestCase):
    """Test cases for my feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.s3_client = S3Client(region='us-east-1')
    
    @patch('src.utils.s3_client.boto3.client')
    def test_my_feature(self, mock_boto_client):
        """Test description."""
        # Setup
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Execute
        result = self.s3_client.my_method()
        
        # Assert
        self.assertTrue(result)
        mock_client.my_method.assert_called_once()
```

### Integration Test Example

```python
import unittest
from src.utils import S3Client, SFTPClient, FileTransferService
from tests.fixtures.test_data import TestFixtures


class TestMyIntegration(unittest.TestCase):
    """Integration test example."""
    
    def setUp(self):
        """Set up test environment."""
        self.fixtures = TestFixtures()
        self.creds = self.fixtures.get_sftp_credentials()
        self.bucket = self.fixtures.get_test_bucket()
    
    def test_integration_scenario(self):
        """Test integration scenario."""
        # Test implementation
        pass
```

## Test Best Practices

### 1. Use Descriptive Names

```python
# Good
def test_upload_file_with_metadata_succeeds(self):
    pass

# Bad
def test_upload(self):
    pass
```

### 2. Follow AAA Pattern

```python
def test_feature(self):
    # Arrange - Set up test data
    test_data = "example"
    
    # Act - Execute the feature
    result = my_function(test_data)
    
    # Assert - Verify the outcome
    self.assertEqual(result, expected_value)
```

### 3. Isolate Tests

```python
# Each test should be independent
def setUp(self):
    # Reset state before each test
    self.client = S3Client()

def tearDown(self):
    # Clean up after each test
    pass
```

### 4. Use Mocks Appropriately

```python
# Mock external dependencies
@patch('src.utils.s3_client.boto3.client')
def test_with_mock(self, mock_client):
    # Test implementation
    pass
```

### 5. Test Edge Cases

```python
def test_empty_file(self):
    """Test handling of empty files."""
    pass

def test_large_file(self):
    """Test handling of large files."""
    pass

def test_invalid_credentials(self):
    """Test error handling for invalid credentials."""
    pass
```

## Coverage Reports

### Generate Coverage Report

```bash
# HTML report
python -m pytest tests/ --cov=src --cov-report=html

# Terminal report
python -m pytest tests/ --cov=src --cov-report=term-missing

# XML report (for CI/CD)
python -m pytest tests/ --cov=src --cov-report=xml
```

### View HTML Report

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Coverage Goals

- **Overall Coverage:** >90%
- **Critical Paths:** 100%
- **Utility Functions:** >95%
- **Error Handlers:** >90%

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          python -m pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting Tests

### Tests Not Found

```bash
# Ensure you're in project root
pwd

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify test discovery
python -m pytest --collect-only
```

### Import Errors

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Check virtual environment
which python
```

### Mock Issues

```python
# Use correct import path for mocking
@patch('src.utils.s3_client.boto3.client')  # Correct
@patch('boto3.client')  # May not work
```

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Test Coverage Best Practices](https://testing.googleblog.com/)
