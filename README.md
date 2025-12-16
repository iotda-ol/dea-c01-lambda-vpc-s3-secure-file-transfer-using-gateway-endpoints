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
