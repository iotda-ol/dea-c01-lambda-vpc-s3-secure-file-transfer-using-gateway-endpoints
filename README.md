# DEA-C01: Secure File Transfer using AWS Lambda, VPC, and S3 Gateway Endpoints

[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20VPC%20%7C%20S3-orange)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.0%2B-purple)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

This repository demonstrates a secure and cost-effective solution for transferring files from a legacy SFTP system to Amazon S3 using AWS Lambda in a VPC. It resolves S3 timeout issues by configuring a VPC Gateway Endpoint for Amazon S3, eliminating the need for internet or NAT gateways, aligned with DEA-C01 (AWS Certified Data Engineer - Associate) best practices.

## 🎯 Overview

This project provides a **production-ready**, **highly modular**, and **well-documented** infrastructure for secure file transfers. It includes:

- ✅ **100-step instruction manual** (novice to expert)
- ✅ **Modular Terraform infrastructure** (6 reusable modules)
- ✅ **Reusable Python code** (organized into core, handlers, utils)
- ✅ **Multi-environment support** (dev, staging, prod)
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

- **[100-Step Instruction Manual](docs/manuals/100-STEP-INSTRUCTION-MANUAL.md)** - Complete guide from novice to expert
- **[Architecture Documentation](docs/architecture/ARCHITECTURE.md)** - System design and components
- **[Deployment Guide](docs/deployment/DEPLOYMENT.md)** - Detailed deployment instructions
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
