# DEA-C01: Secure File Transfer using AWS Lambda, VPC, and S3 Gateway Endpoints

[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20VPC%20%7C%20S3-orange)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0%2B-purple)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

This repository demonstrates a secure and cost-effective solution for transferring files from a legacy SFTP system to Amazon S3 using AWS Lambda in a VPC. It resolves S3 timeout issues by configuring a VPC Gateway Endpoint for Amazon S3, eliminating the need for internet or NAT gateways, aligned with DEA-C01 (AWS Certified Data Engineer - Associate) best practices.

## 🎯 Overview

This project provides a **production-ready**, **highly modular**, and **well-documented** infrastructure for secure file transfers. It includes:

- ✅ **Universal Infrastructure Composer** (AWS, GCP, Azure support)
- ✅ **100-step instruction manual** (novice to expert)
- ✅ **Modular Terraform infrastructure** (6 reusable modules)
- ✅ **Reusable Python code** (organized into core, handlers, utils)
- ✅ **Multi-environment support** (dev, staging, prod)
- ✅ **Multi-cloud deployment patterns** (complete IaC for all clouds)
- ✅ **Comprehensive documentation** (architecture, deployment, troubleshooting)
- ✅ **Utility scripts** (deployment, testing, monitoring)
- ✅ **Security best practices** (encryption, least privilege, VPC isolation)

## 📁 Repository Structure

```
.
├── docs/                          # Documentation
│   ├── manuals/                   # Instruction manuals
│   │   └── 100-STEP-INSTRUCTION-MANUAL.md
│   ├── architecture/              # Architecture documentation
│   │   └── ARCHITECTURE.md
│   ├── deployment/                # Deployment guides
│   │   └── DEPLOYMENT.md
│   ├── api/                       # API documentation
│   └── troubleshooting/           # Troubleshooting guides
│
├── map-diagram-infra/            # Universal Infrastructure Composer
│   ├── README.md                  # Overview and navigation
│   ├── QUICK-REFERENCE.md         # Quick reference guide
│   ├── VISUAL-INDEX.md            # Visual diagram index
│   ├── infrastructure-diagram.md  # Mermaid diagrams (all architectures)
│   ├── cloud-service-mapping.md   # AWS/GCP/Azure service mappings
│   ├── component-details.md       # Deep technical documentation
│   ├── deployment-patterns.md     # Cloud-specific deployment guides
│   └── iac-reference.md           # Complete Terraform code (all clouds)
│
├── terraform/                     # Infrastructure as Code
│   ├── modules/                   # Reusable Terraform modules
│   │   ├── vpc/                   # VPC module
│   │   ├── s3/                    # S3 bucket module
│   │   ├── lambda/                # Lambda function module
│   │   ├── gateway-endpoint/      # VPC Gateway Endpoint module
│   │   ├── iam/                   # IAM roles and policies module
│   │   └── security-groups/       # Security groups module
│   └── environments/              # Environment-specific configurations
│       ├── dev/                   # Development environment
│       ├── staging/               # Staging environment
│       └── prod/                  # Production environment
│
├── lambda/                        # Lambda function code
│   ├── src/                       # Source code
│   │   ├── core/                  # Core utilities
│   │   │   ├── logger.py          # Logging utilities
│   │   │   ├── config.py          # Configuration management
│   │   │   └── exceptions.py      # Custom exceptions
│   │   ├── handlers/              # Business logic handlers
│   │   │   ├── s3_handler.py      # S3 operations
│   │   │   └── sftp_handler.py    # SFTP operations
│   │   ├── utils/                 # Helper utilities
│   │   │   ├── retry.py           # Retry logic
│   │   │   ├── validators.py      # File validation
│   │   │   └── secrets.py         # Secrets Manager integration
│   │   └── main.py                # Lambda handler entry point
│   ├── tests/                     # Test files
│   └── requirements.txt           # Python dependencies
│
├── scripts/                       # Utility scripts
│   ├── deployment/                # Deployment scripts
│   │   ├── package-lambda.sh      # Package Lambda function
│   │   ├── deploy.sh              # Deploy infrastructure
│   │   └── test-lambda.sh         # Test Lambda function
│   ├── monitoring/                # Monitoring scripts
│   │   └── tail-logs.sh           # Monitor CloudWatch logs
│   └── maintenance/               # Maintenance scripts
│       └── cleanup.sh             # Cleanup resources
│
├── config/                        # Configuration files
│   ├── dev/                       # Dev configuration
│   ├── staging/                   # Staging configuration
│   └── prod/                      # Production configuration
│
├── examples/                      # Example configurations
│   ├── basic/                     # Basic usage examples
│   ├── advanced/                  # Advanced examples
│   └── production/                # Production examples
│
└── tests/                         # Test infrastructure
    ├── unit/                      # Unit tests
    ├── integration/               # Integration tests
    └── e2e/                       # End-to-end tests
```

## 🚀 Quick Start

### Prerequisites

- AWS CLI v2.x ([Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- Terraform v1.0+ ([Install](https://www.terraform.io/downloads))
- Python 3.11+ ([Install](https://www.python.org/downloads/))
- Git ([Install](https://git-scm.com/downloads))

### 1. Clone Repository

```bash
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints
```

### 2. Configure AWS

```bash
aws configure
# Enter your AWS credentials
```

### 3. Package Lambda Function

```bash
chmod +x scripts/deployment/package-lambda.sh
./scripts/deployment/package-lambda.sh
```

### 4. Configure Variables

```bash
cd terraform/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 5. Deploy Infrastructure

```bash
chmod +x ../../../scripts/deployment/deploy.sh
../../../scripts/deployment/deploy.sh dev
```

### 6. Test Function

```bash
chmod +x ../../../scripts/deployment/test-lambda.sh
../../../scripts/deployment/test-lambda.sh secure-transfer-dev-function
```

## 📖 Documentation

### Core Documentation
- **[100-Step Instruction Manual](docs/manuals/100-STEP-INSTRUCTION-MANUAL.md)** - Complete guide from novice to expert
- **[Architecture Documentation](docs/architecture/ARCHITECTURE.md)** - System design and components
- **[Deployment Guide](docs/deployment/DEPLOYMENT.md)** - Detailed deployment instructions
- **[Troubleshooting Guide](docs/troubleshooting/)** - Common issues and solutions

### 🌐 Universal Infrastructure Composer (Multi-Cloud Support)

**📊 Complete infrastructure diagrams and deployment guides for AWS, GCP, and Azure**

- **[Quick Reference](map-diagram-infra/QUICK-REFERENCE.md)** - Fast navigation and key information
- **[Visual Index](map-diagram-infra/VISUAL-INDEX.md)** - Diagram gallery with use cases
- **[Infrastructure Diagrams](map-diagram-infra/infrastructure-diagram.md)** - Complete Mermaid diagrams:
  - High-level cloud-agnostic architecture
  - Detailed component diagrams
  - Network flow sequences
  - Security architecture
  - Cost optimization patterns
  - Multi-region deployment
- **[Cloud Service Mapping](map-diagram-infra/cloud-service-mapping.md)** - AWS ↔ GCP ↔ Azure equivalents:
  - Complete service mapping table
  - Pricing comparisons ($2.20-$3.46/month)
  - Migration guides between clouds
- **[Component Details](map-diagram-infra/component-details.md)** - Technical deep dive:
  - Compute, Network, Storage layers
  - Security, Monitoring, Automation
  - Data flow and error handling
- **[Deployment Patterns](map-diagram-infra/deployment-patterns.md)** - Step-by-step guides:
  - AWS deployment (Lambda + VPC Gateway Endpoint)
  - GCP deployment (Cloud Functions + Private Google Access)
  - Azure deployment (Functions + Service Endpoints)
- **[IaC Reference](map-diagram-infra/iac-reference.md)** - Production-ready Terraform:
  - Complete AWS Terraform (8 files)
  - Complete GCP Terraform (8 files)
  - Complete Azure Terraform (7 files)

**Why Universal?** Deploy the same secure file transfer architecture on any cloud provider with confidence. All three implementations feature FREE private connectivity, eliminating NAT Gateway costs.
- **[Troubleshooting Guide](docs/troubleshooting/)** - Common issues and solutions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       AWS Cloud                              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              VPC (10.0.0.0/16)                      │    │
│  │                                                      │    │
│  │  ┌──────────────┐      ┌──────────────┐           │    │
│  │  │Private Subnet│      │Private Subnet│           │    │
│  │  │  (Lambda)    │      │    (Multi-AZ)│           │    │
│  │  └──────┬───────┘      └──────────────┘           │    │
│  │         │                                           │    │
│  │         │                                           │    │
│  │  ┌──────▼─────────────────────────────────┐       │    │
│  │  │     S3 Gateway Endpoint (Free!)        │       │    │
│  │  └──────┬─────────────────────────────────┘       │    │
│  └─────────┼──────────────────────────────────────────┘    │
│            │                                                │
│     ┌──────▼────────┐                                      │
│     │  S3 Bucket    │                                      │
│     │  (Encrypted)  │                                      │
│     └───────────────┘                                      │
└─────────────────────────────────────────────────────────────┘
         │
         │ SFTP (Internet)
         │
┌────────▼──────────┐
│  Legacy SFTP      │
│    Server         │
└───────────────────┘
```

**Key Benefits:**
- ❌ No NAT Gateway ($32/month saved)
- ❌ No Internet Gateway required
- ✅ Private S3 access via Gateway Endpoint (FREE)
- ✅ Enhanced security with VPC isolation
- ✅ Cost-effective and scalable

## 🔒 Security Features

- **VPC Isolation**: Lambda runs in private subnets with no internet access for S3
- **Gateway Endpoint**: Private connection to S3 (no data leaves AWS network)
- **Encryption**: 
  - Data in transit: TLS/HTTPS
  - Data at rest: S3 SSE-AES256 or SSE-KMS
- **IAM Least Privilege**: Minimal required permissions
- **Secrets Manager**: Secure credential storage
- **Security Groups**: Restrictive network rules
- **CloudWatch Logs**: Complete audit trail

## 💰 Cost Optimization

| Component | Monthly Cost | Note |
|-----------|--------------|------|
| Lambda | ~$0.20 | For 1000 executions/month |
| S3 | Variable | Pay for storage + requests |
| VPC | $0 | No NAT gateway needed! |
| Gateway Endpoint | $0 | FREE for S3 |
| CloudWatch Logs | ~$0.50 | 1GB logs/month |
| **Total** | **~$0.70** | **+ S3 storage costs** |

**Savings vs NAT Gateway:** ~$32/month per AZ!

## 🧪 Testing

```bash
# Run unit tests
cd lambda
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Test Lambda function
./scripts/deployment/test-lambda.sh
```

## 📊 Monitoring

```bash
# Monitor logs in real-time
./scripts/monitoring/tail-logs.sh secure-transfer-dev-function

# View CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-function \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## 🔄 CI/CD

The repository is designed for CI/CD integration. Example GitHub Actions workflow:

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1
      - name: Terraform Init
        run: cd terraform/environments/dev && terraform init
      - name: Terraform Apply
        run: cd terraform/environments/dev && terraform apply -auto-approve
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🏆 Certification Alignment

This project aligns with:
- ✅ **AWS Certified Data Engineer - Associate (DEA-C01)**
- ✅ AWS Certified Solutions Architect - Associate
- ✅ AWS Certified Developer - Associate

Covers exam domains:
- Data ingestion and transformation
- Data storage and management
- Security and compliance
- Cost optimization
- Operational excellence

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/issues)
- 📖 Documentation: [docs/](docs/)
- 💬 Discussions: [GitHub Discussions](https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/discussions)

## 🌟 Acknowledgments

Built with best practices from:
- AWS Well-Architected Framework
- Terraform Best Practices
- Python PEP 8 Style Guide
- AWS DEA-C01 Study Guide

---

**⭐ If you find this project helpful, please star the repository!**
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
# Secure File Transfer: Lambda VPC with S3 Gateway Endpoints

[![DEA-C01](https://img.shields.io/badge/AWS-DEA--C01-orange)](https://aws.amazon.com/certification/certified-data-engineer-associate/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0+-purple)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview

This repository demonstrates a **secure, cost-effective solution** for transferring files from a legacy SFTP system to Amazon S3 using AWS Lambda deployed in a VPC. The solution resolves S3 connectivity timeout issues by provisioning a **VPC Gateway Endpoint** for Amazon S3, eliminating the need for expensive Internet Gateways or NAT Gateways.

### Key Features

✅ **Secure Architecture**: VPC-isolated Lambda with no public internet access  
✅ **Cost Optimized**: ~95% cost reduction vs EC2-based solutions (~$3/month vs $65/month)  
✅ **DEA-C01 Aligned**: Follows AWS Certified Data Engineer Associate best practices  
✅ **S3 Gateway Endpoint**: Free, private connectivity to S3 without NAT Gateway  
✅ **Least Privilege IAM**: Minimal permissions for each component  
✅ **Encryption**: End-to-end encryption at rest and in transit  
✅ **Automated Lifecycle**: S3 lifecycle policies for cost optimization  
✅ **Production Ready**: Comprehensive logging, monitoring, and error handling  

## Architecture

```
┌─────────────────────┐
│  Legacy SFTP Server │
└──────────┬──────────┘
           │ Port 22 (SSH)
           │
┌──────────▼─────────────────────────────────────────┐
│                  AWS VPC                            │
│  ┌──────────────────────────────────────────────┐  │
│  │         Private Subnet (10.0.1.0/24)         │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │                                        │  │  │
│  │  │     Lambda Function (Python 3.11)     │  │  │
│  │  │     - VPC-enabled                     │  │  │
│  │  │     - Security Group attached         │  │  │
│  │  │     - Retrieves SFTP credentials      │  │  │
│  │  │                                        │  │  │
│  │  └───────────────┬────────────────────────┘  │  │
│  │                  │                            │  │
│  │                  │ HTTPS (Port 443)           │  │
│  │                  │                            │  │
│  │  ┌───────────────▼────────────────────────┐  │  │
│  │  │      S3 VPC Gateway Endpoint           │  │  │
│  │  │      - No data transfer charges        │  │  │
│  │  │      - Traffic stays in AWS network    │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                       │
                       │ Private connection
                       │
        ┌──────────────▼──────────────┐
        │    Amazon S3 Bucket         │
        │    - AES-256 Encryption     │
        │    - Versioning enabled     │
        │    - Lifecycle policies     │
        │    - Public access blocked  │
        └─────────────────────────────┘
```

### How It Solves S3 Timeout Issues

**Problem**: Lambda functions in VPCs without internet access cannot reach S3, resulting in connection timeouts.

**Traditional Solution**: Add NAT Gateway ($32.40/month + data transfer costs)

**This Solution**: Use S3 VPC Gateway Endpoint (FREE)
- No hourly charges
- No data processing charges
- Traffic never leaves AWS network
- Automatic route table integration

## Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Terraform >= 1.0
- Python >= 3.11
- bash shell

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
# 1. Clone repository
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints

# 2. Configure variables
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your SFTP details

# 3. Build and deploy
cd ..
bash scripts/build_lambda.sh
bash scripts/deploy.sh
```

### Configure SFTP Credentials

After deployment, update the Secrets Manager secret:

```bash
# Get secret ARN
cd terraform
SECRET_ARN=$(terraform output -raw sftp_secret_arn)

# Update credentials (password authentication)
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-username",
    "password": "your-password",
    "host": "sftp.example.com",
    "port": 22
  }'
```

### Test the Function

```bash
# Invoke Lambda function
LAMBDA_NAME=$(terraform output -raw lambda_function_name)
aws lambda invoke --function-name $LAMBDA_NAME response.json

# View logs
LOG_GROUP=$(terraform output -raw cloudwatch_log_group)
aws logs tail $LOG_GROUP --follow
```

## Repository Structure

```
.
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── terraform/                         # Terraform infrastructure code
│   ├── main.tf                        # Provider and backend configuration
│   ├── variables.tf                   # Input variables
│   ├── vpc.tf                         # VPC, subnets, security groups
│   ├── s3.tf                          # S3 bucket and gateway endpoint
│   ├── iam.tf                         # IAM roles and policies
│   ├── lambda.tf                      # Lambda function and CloudWatch
│   ├── secrets.tf                     # Secrets Manager configuration
│   ├── outputs.tf                     # Output values
│   └── terraform.tfvars.example       # Example variables file
├── lambda/                            # Lambda function code
│   ├── lambda_function.py             # Main Lambda handler
│   └── requirements.txt               # Python dependencies
├── scripts/                           # Deployment scripts
│   ├── build_lambda.sh                # Build Lambda package
│   └── deploy.sh                      # Deploy infrastructure
└── docs/                              # Documentation
    ├── ARCHITECTURE.md                # Architecture details
    ├── SECURITY.md                    # Security best practices
    ├── COST_OPTIMIZATION.md           # Cost optimization guide
    └── DEPLOYMENT.md                  # Detailed deployment guide
```

## Features in Detail

### 1. VPC Configuration

- **Private Subnets**: Lambda runs in private subnets with no internet access
- **Multi-AZ**: Subnets span multiple availability zones for high availability
- **Security Groups**: Restrictive firewall rules (HTTPS to S3, SSH to SFTP)
- **No NAT Gateway**: Cost savings of ~$32/month per AZ

### 2. S3 Gateway Endpoint

- **Free Service**: No hourly or data transfer charges
- **Private Connectivity**: Traffic never traverses the internet
- **Automatic Routing**: Integrates with VPC route tables
- **Endpoint Policy**: Least-privilege access control

### 3. Lambda Function

- **Python 3.11**: Latest stable runtime
- **VPC-Enabled**: Runs in private subnets
- **Paramiko Library**: Secure SFTP client
- **Error Handling**: Comprehensive exception handling and logging
- **Memory**: 512 MB (adjustable based on file sizes)
- **Timeout**: 5 minutes (adjustable)

### 4. Security Features

- **Least Privilege IAM**: Minimal permissions for each component
- **Secrets Manager**: Secure credential storage with encryption
- **S3 Encryption**: AES-256 server-side encryption
- **Versioning**: Protection against accidental deletion
- **Public Access Block**: All public access disabled
- **VPC Isolation**: No public internet exposure

### 5. Cost Optimization

- **S3 Lifecycle Policies**: Automatic transition to cheaper storage classes
  - Day 30: Move to Standard-IA (46% savings)
  - Day 90: Move to Glacier Instant Retrieval (83% savings)
  - Day 180: Move to Deep Archive (96% savings)
- **Lambda Pay-Per-Use**: No idle costs
- **CloudWatch Logs**: 7-day retention to minimize storage
- **No NAT Gateway**: ~$32/month savings
- **Bucket Key Encryption**: Reduces KMS costs by 99%

### 6. Monitoring and Logging

- **CloudWatch Logs**: All Lambda invocations logged
- **Structured Logging**: JSON format for easy parsing
- **CloudWatch Metrics**: Duration, errors, invocations
- **EventBridge**: Optional scheduled execution

## Cost Estimate

### Monthly Cost Breakdown (1,000 transfers, 100 MB avg file size)

| Service | Cost |
|---------|------|
| Lambda (1,000 invocations, 30s avg) | $0.25 |
| S3 Storage (100 GB with lifecycle) | $2.30 |
| S3 Requests (1,000 PUTs) | $0.01 |
| Secrets Manager | $0.40 |
| CloudWatch Logs | $0.05 |
| S3 Gateway Endpoint | $0.00 |
| **Total** | **~$3.00/month** |

**Compare to EC2-based solution**: ~$65/month (95% cost reduction)

## Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed architecture and component descriptions
- **[Security Best Practices](docs/SECURITY.md)**: Comprehensive security guidelines
- **[Cost Optimization](docs/COST_OPTIMIZATION.md)**: DEA-C01 cost optimization strategies
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Step-by-step deployment instructions

## DEA-C01 Best Practices Demonstrated

This solution demonstrates key concepts from the AWS Certified Data Engineer Associate (DEA-C01) exam:

1. ✅ **Cost Optimization**: VPC Gateway Endpoints, S3 lifecycle policies, serverless architecture
2. ✅ **Security**: Least privilege IAM, encryption at rest and in transit, VPC isolation
3. ✅ **Data Transfer**: Efficient SFTP to S3 transfer using Lambda
4. ✅ **Storage Optimization**: S3 lifecycle policies for automatic tier transitions
5. ✅ **Networking**: VPC endpoints for private connectivity
6. ✅ **Monitoring**: CloudWatch Logs and metrics for operational visibility
7. ✅ **Automation**: Infrastructure as Code with Terraform

## Troubleshooting

### Lambda Timeout

**Issue**: Lambda function times out
**Solution**: Check VPC Gateway Endpoint is attached to route table

```bash
# Verify endpoint
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=YOUR_VPC_ID"
```

### S3 Access Denied

**Issue**: Lambda cannot write to S3
**Solution**: Verify IAM policy and VPC endpoint policy

```bash
# Check Lambda role policies
aws iam list-attached-role-policies --role-name YOUR_ROLE_NAME
```

### SFTP Connection Failed

**Issue**: Cannot connect to SFTP server
**Solution**: Check security group egress rules and credentials

```bash
# View CloudWatch Logs
aws logs tail /aws/lambda/YOUR_FUNCTION_NAME --follow
```

## Contributing

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
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- AWS Documentation and Best Practices
- DEA-C01 Exam Guide
- AWS Well-Architected Framework
- Terraform AWS Provider Documentation

## Support

For issues and questions:
- Open an issue in GitHub
- Review documentation in the `docs/` directory
- Check AWS documentation for service-specific questions

## Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Certified Data Engineer](https://aws.amazon.com/certification/certified-data-engineer-associate/)

---

**Built with ❤️ for DEA-C01 certification preparation and real-world AWS data engineering**
