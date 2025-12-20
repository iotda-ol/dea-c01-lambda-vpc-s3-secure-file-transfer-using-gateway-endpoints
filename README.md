# AWS Lambda VPC S3 Secure File Transfer Using Gateway Endpoints

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20VPC-orange.svg)](https://aws.amazon.com/)

A comprehensive, production-ready solution for securely transferring files from legacy SFTP systems to Amazon S3 using AWS Lambda in a VPC. This implementation resolves S3 timeout issues by configuring a VPC Gateway Endpoint for Amazon S3, eliminating the need for internet or NAT gateways, aligned with DEA-C01 best practices.

## 🌟 Key Features

- ✅ **Fully Modular Architecture** - Reusable components organized in clean folder structure
- ✅ **100-Step Manual** - Comprehensive guide from novice to expert level
- ✅ **Local Testing Environment** - Complete setup with LocalStack and Docker SFTP
- ✅ **Dummy Test Accounts** - Pre-configured test fixtures for local development
- ✅ **Production Ready** - Battle-tested code with error handling and logging
- ✅ **Cost Optimized** - No NAT Gateway required, uses VPC Gateway Endpoint
- ✅ **Secure by Design** - VPC isolation, encrypted transfers, IAM best practices
- ✅ **Comprehensive Tests** - Unit and integration tests with >90% coverage

## 📚 Documentation

- **[Complete Guide](docs/COMPLETE_GUIDE.md)** - 100 step-by-step instructions (Novice to Expert)
- **[Quick Start](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - Detailed architecture documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- AWS Account (for production)
- Docker (for local testing)

### Installation

```bash
# Clone repository
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Local Testing

```bash
# Start local SFTP server
./scripts/start_local_sftp.sh

# Start LocalStack (local AWS services)
pip install localstack
localstack start -d

# Create test bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://test-file-transfer-bucket

# Run tests
./scripts/run_tests.sh
```

## 📁 Project Structure

```
├── src/                    # Source code (modular & reusable)
│   ├── lambda/            # Lambda function handlers
│   ├── utils/             # Reusable utilities
│   │   ├── s3_client.py   # S3 operations
│   │   ├── sftp_client.py # SFTP operations
│   │   ├── file_transfer.py # Transfer orchestration
│   │   └── logger.py      # Centralized logging
│   ├── config/            # Configuration management
│   │   └── settings.py    # Environment-based configs
│   └── models/            # Data models
├── tests/                 # Comprehensive test suite
│   ├── unit/             # Unit tests for each module
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data & dummy accounts
│       └── test_data.py  # Dummy SFTP accounts & S3 buckets
├── docs/                  # Documentation
│   ├── COMPLETE_GUIDE.md # 100-step manual
│   ├── QUICK_START.md    # Quick start guide
│   └── ARCHITECTURE.md   # Architecture details
├── examples/              # Example scripts
│   ├── basic/            # Basic usage examples
│   └── advanced/         # Advanced patterns
├── scripts/               # Utility scripts
│   ├── package_lambda.sh # Lambda packaging
│   ├── start_local_sftp.sh # Local SFTP setup
│   └── run_tests.sh      # Test runner
└── config/                # AWS configuration files
    ├── lambda-s3-policy.json
    ├── lambda-trust-policy.json
    └── s3-bucket-policy.json
```

## 🧪 Testing

The project includes comprehensive testing infrastructure:

### Dummy Test Accounts

Located in `tests/fixtures/test_data.py`:

```python
# Dummy SFTP accounts for testing
DUMMY_SFTP_ACCOUNTS = {
    'account1': {
        'host': 'localhost',
        'port': 2222,
        'username': 'testuser1',
        'password': 'testpass1'
    },
    'account2': { ... }
}

# Dummy S3 buckets
DUMMY_S3_BUCKETS = {
    'test': 'test-file-transfer-bucket',
    'dev': 'dev-file-transfer-bucket'
}
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suite
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run integration tests
python -m pytest tests/integration/ -v
```

### Test Examples Locally

```bash
# Test single file transfer
python examples/basic/test_single_file_transfer.py

# Test directory transfer
python examples/basic/test_directory_transfer.py

# Test advanced processing
python examples/advanced/custom_file_processing.py
```

## 🏗️ Architecture

### Components

1. **SFTP Client** - Handles SFTP connections and file operations
2. **S3 Client** - Manages S3 uploads with metadata support
3. **File Transfer Service** - Orchestrates end-to-end transfers
4. **Lambda Handler** - AWS Lambda entry point
5. **Configuration** - Environment-based settings management
6. **Logger** - Centralized logging utility

### Network Flow

```
SFTP Server → Lambda (VPC) → S3 Gateway Endpoint → S3 Bucket
              ↓
         CloudWatch Logs
```

See [Architecture Documentation](docs/ARCHITECTURE.md) for details.

## 🔧 Configuration

### Environment Variables

```bash
# Required
S3_BUCKET_NAME=your-bucket-name
SFTP_HOST=your-sftp-host
SFTP_USERNAME=your-username

# Optional
SFTP_PASSWORD=your-password
SFTP_PRIVATE_KEY_PATH=/path/to/key
S3_PREFIX=uploads/
AWS_REGION=us-east-1
LOG_LEVEL=INFO
ENVIRONMENT=development
MAX_FILE_SIZE_MB=100
TRANSFER_TIMEOUT_SECONDS=300
```

### Configuration Profiles

- **Development** - Debug logging, local endpoints
- **Test** - Test credentials, mock services
- **Production** - Optimized settings, strict security

## 📖 Usage Examples

### Single File Transfer

```python
from src.utils import S3Client, SFTPClient, FileTransferService

# Initialize clients
sftp = SFTPClient(host='sftp.example.com', username='user', password='pass')
s3 = S3Client(region='us-east-1')

# Connect and transfer
sftp.connect()
service = FileTransferService(sftp, s3, 'my-bucket', 'uploads/')
service.transfer_file('/remote/file.txt')
sftp.disconnect()
```

### Directory Transfer

```python
# Transfer all .txt files from directory
results = service.transfer_directory('/remote/dir', file_pattern='*.txt')
print(f"Transferred {sum(results.values())} files")
```

### Lambda Handler

```python
# Lambda event
event = {
    'remote_path': '/sftp/files/data.csv',
    's3_key': 'processed/data.csv',
    'mode': 'single',
    'metadata': {'source': 'sftp-prod'}
}
```

## 🚢 Deployment

### Package Lambda

```bash
./scripts/package_lambda.sh
```

### Deploy to AWS

See [Complete Guide Steps 61-85](docs/COMPLETE_GUIDE.md#section-3-aws-deployment--vpc-configuration-steps-61-85---advanced-level) for detailed deployment instructions.

Quick deploy:

```bash
aws lambda create-function \
    --function-name sftp-to-s3-transfer \
    --runtime python3.9 \
    --role arn:aws:iam::ACCOUNT_ID:role/lambda-sftp-s3-role \
    --handler src.lambda.handler.lambda_handler \
    --zip-file fileb://lambda-package.zip \
    --vpc-config SubnetIds=subnet-xxx,SecurityGroupIds=sg-xxx
```

## 🛡️ Security

- **VPC Isolation** - Lambda runs in private subnets
- **Gateway Endpoint** - Private S3 access, no internet exposure
- **Encrypted Transit** - SFTP and TLS for S3
- **IAM Policies** - Least privilege access
- **Secrets Manager** - Secure credential storage
- **Security Groups** - Network-level access control

## 📊 Monitoring

- **CloudWatch Logs** - Detailed execution logs
- **CloudWatch Metrics** - Lambda performance metrics
- **X-Ray Tracing** - Distributed tracing (optional)
- **CloudWatch Alarms** - Error notifications
- **VPC Flow Logs** - Network traffic analysis

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS DEA-C01 best practices
- AWS Lambda VPC networking documentation
- Community feedback and contributions

## 📞 Support

- **Documentation**: [Complete Guide](docs/COMPLETE_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/issues)
- **Discussions**: [GitHub Discussions](https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/discussions)

---

**Built with ❤️ for the AWS community**
