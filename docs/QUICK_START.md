# Quick Start Guide

This guide will help you get started with the AWS Lambda VPC S3 Secure File Transfer solution.

## Prerequisites

- Python 3.9 or higher
- AWS account (for production deployment)
- Docker (for local testing)
- Git

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Local Testing

### 1. Start Local Services

**Start SFTP Server:**
```bash
chmod +x scripts/start_local_sftp.sh
./scripts/start_local_sftp.sh
```

**Start LocalStack (for local S3):**
```bash
pip install localstack
localstack start -d
```

**Create test bucket:**
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://test-file-transfer-bucket
```

### 2. Run Tests

**Run all tests:**
```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

**Run specific tests:**
```bash
python -m pytest tests/unit/test_s3_client.py -v
```

### 3. Test Example Scripts

**Single file transfer:**
```bash
python examples/basic/test_single_file_transfer.py
```

**Directory transfer:**
```bash
python examples/basic/test_directory_transfer.py
```

## AWS Deployment

For complete deployment instructions, see the [Complete Guide](docs/COMPLETE_GUIDE.md) - Steps 61-85.

### Quick Deployment

1. **Package Lambda:**
```bash
chmod +x scripts/package_lambda.sh
./scripts/package_lambda.sh
```

2. **Create required AWS resources:**
- VPC with private subnets
- S3 VPC Gateway Endpoint
- Security groups
- IAM roles and policies

3. **Deploy Lambda:**
```bash
aws lambda create-function \
    --function-name sftp-to-s3-transfer \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sftp-s3-role \
    --handler src.lambda.handler.lambda_handler \
    --zip-file fileb://lambda-package.zip \
    --vpc-config SubnetIds=subnet-xxx,SecurityGroupIds=sg-xxx
```

## Configuration

### Environment Variables

Create a `.env` file:
```bash
ENVIRONMENT=development
S3_BUCKET_NAME=your-bucket-name
SFTP_HOST=your-sftp-host
SFTP_USERNAME=your-username
SFTP_PASSWORD=your-password
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

### AWS Lambda Environment Variables

Configure in Lambda console or via CLI:
- `S3_BUCKET_NAME`
- `SFTP_HOST`
- `SFTP_USERNAME`
- `S3_PREFIX`
- `AWS_REGION`
- `LOG_LEVEL`
- `ENVIRONMENT`

## Project Structure

```
├── src/                    # Source code
│   ├── lambda/            # Lambda handlers
│   ├── utils/             # Utilities (S3, SFTP, logging)
│   ├── config/            # Configuration
│   └── models/            # Data models
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data & dummy accounts
├── docs/                  # Documentation
│   └── COMPLETE_GUIDE.md # 100-step manual
├── examples/              # Example scripts
│   ├── basic/            # Basic examples
│   └── advanced/         # Advanced examples
├── scripts/               # Utility scripts
└── config/                # AWS configuration files
```

## Next Steps

1. Read the [Complete Guide](docs/COMPLETE_GUIDE.md) for detailed instructions
2. Explore the [examples](examples/) directory
3. Review the [test fixtures](tests/fixtures/) for dummy accounts
4. Customize configuration for your use case

## Common Issues

### SFTP Connection Timeout
- Check SFTP server is running
- Verify credentials
- Check network connectivity

### S3 Upload Fails
- Verify IAM permissions
- Check bucket exists
- Ensure VPC Gateway Endpoint is configured

### Lambda Timeout
- Increase Lambda timeout setting
- Check VPC Gateway Endpoint routes
- Verify network configuration

## Getting Help

- Read the troubleshooting section in the [Complete Guide](docs/COMPLETE_GUIDE.md)
- Check existing issues on GitHub
- Open a new issue with details

## License

See LICENSE file for details.
