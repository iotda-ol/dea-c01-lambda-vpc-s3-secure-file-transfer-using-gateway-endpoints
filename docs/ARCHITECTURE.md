# Architecture Overview

## Solution Architecture

This solution implements a secure file transfer system that moves files from a legacy SFTP server to Amazon S3 using AWS Lambda functions running in a VPC with S3 Gateway Endpoints.

## Components

### 1. VPC Configuration
- **VPC**: Isolated network environment (10.0.0.0/16)
- **Private Subnets**: Two private subnets across different availability zones for high availability
  - Subnet 1: 10.0.1.0/24 in AZ-a
  - Subnet 2: 10.0.2.0/24 in AZ-b
- **No Internet Gateway or NAT Gateway**: Cost-optimized design using VPC endpoints

### 2. S3 Gateway Endpoint
- **Purpose**: Provides private connectivity between VPC and Amazon S3 without requiring internet access
- **Benefits**:
  - No data transfer charges for S3 access
  - Traffic never leaves AWS network
  - Resolves timeout issues with VPC Lambda accessing S3
  - Eliminates need for NAT Gateway ($0.045/hour savings)
- **Route Table**: Associated with private subnet route tables for automatic routing

### 3. Lambda Function
- **Runtime**: Python 3.11
- **VPC Configuration**: Deployed in private subnets
- **Memory**: 512 MB
- **Timeout**: 300 seconds (5 minutes)
- **Network**: Attached to Lambda security group with controlled egress

### 4. Security Groups
- **Lambda Security Group**:
  - Egress to HTTPS (443) for S3 API calls via Gateway Endpoint
  - Egress to SFTP port (22) for connecting to legacy SFTP server

### 5. S3 Bucket
- **Encryption**: AES-256 server-side encryption enabled by default
- **Versioning**: Enabled for data protection
- **Public Access**: Completely blocked
- **Lifecycle Policies**: Automated transitions for cost optimization

### 6. IAM Roles and Policies (Least Privilege)
- **Lambda Execution Role**: Minimal permissions required
  - S3: PutObject, PutObjectAcl, ListBucket (scoped to specific bucket)
  - CloudWatch Logs: CreateLogStream, PutLogEvents (scoped to specific log group)
  - EC2: Network interface management for VPC Lambda
  - Secrets Manager: GetSecretValue (scoped to specific secret)

### 7. AWS Secrets Manager
- **Purpose**: Securely store SFTP credentials (username, private key/password)
- **Access**: Lambda retrieves credentials at runtime
- **Encryption**: Encrypted at rest with AWS KMS

### 8. CloudWatch Logs
- **Log Group**: Dedicated log group for Lambda function
- **Retention**: 7 days (configurable)
- **Purpose**: Monitoring, debugging, and audit trail

### 9. EventBridge (Optional)
- **Schedule Rule**: Triggers Lambda on a schedule (disabled by default)
- **Frequency**: Configurable (default: 1 hour)

## Data Flow

```
[Legacy SFTP Server]
         |
         | (1) Lambda connects via SFTP
         |     (private subnet, egress port 22)
         v
[Lambda Function in VPC]
         |
         | (2) Retrieves credentials
         v
[AWS Secrets Manager]
         |
         | (3) Downloads file from SFTP
         v
[Lambda Memory Buffer]
         |
         | (4) Uploads to S3 via Gateway Endpoint
         |     (HTTPS on port 443, stays in AWS network)
         v
[S3 VPC Gateway Endpoint]
         |
         | (5) Stores file
         v
[S3 Bucket (Encrypted)]
         |
         | (6) Logs operation
         v
[CloudWatch Logs]
```

## Network Flow

1. Lambda function runs in **private subnets** (no internet access)
2. SFTP connection goes through VPC's internet route (if legacy SFTP is external)
3. S3 API calls route through **S3 Gateway Endpoint** (stays within AWS network)
4. CloudWatch Logs are accessible via AWS service endpoints
5. Secrets Manager access via AWS PrivateLink (implicit)

## High Availability

- Lambda function can run in multiple availability zones
- Private subnets span multiple AZs
- S3 provides 99.999999999% (11 9's) durability
- No single point of failure in the architecture

## Scalability

- Lambda auto-scales based on incoming events
- S3 automatically scales to handle any number of requests
- VPC Gateway Endpoint scales automatically

## Cost Optimization (DEA-C01 Best Practices)

1. **No NAT Gateway**: Saves ~$32.40/month per NAT Gateway
2. **S3 Gateway Endpoint**: Free (no data processing or hourly charges)
3. **Lambda**: Pay only for compute time (no idle charges)
4. **S3 Lifecycle Policies**: Automatic transition to lower-cost storage classes
5. **CloudWatch Logs**: Short retention period (7 days)
6. **No Elastic IPs or Internet Gateways**: Additional cost savings
