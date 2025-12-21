# Architecture Overview

## High-Level Architecture

```
┌─────────────────┐
│  SFTP Server    │
│  (Legacy)       │
└────────┬────────┘
         │
         │ Port 22
         │
    ┌────▼────────────────────────────────────┐
    │           VPC                            │
    │  ┌────────────────────────────────┐     │
    │  │  Private Subnet                │     │
    │  │  ┌──────────────────────┐      │     │
    │  │  │  Lambda Function     │      │     │
    │  │  │  - SFTP Download     │      │     │
    │  │  │  - S3 Upload         │      │     │
    │  │  └──────────┬───────────┘      │     │
    │  └─────────────┼──────────────────┘     │
    │                │                         │
    │  ┌─────────────▼──────────────────┐     │
    │  │  S3 VPC Gateway Endpoint       │     │
    │  │  - Private connection to S3    │     │
    │  │  - No NAT/IGW required         │     │
    │  └─────────────┬──────────────────┘     │
    └────────────────┼────────────────────────┘
                     │
                     │ Private AWS Network
                     │
              ┌──────▼──────┐
              │  Amazon S3  │
              │   Bucket    │
              └─────────────┘
```

## Component Details

### 1. Lambda Function in VPC
- **Purpose:** Execute file transfer logic
- **Network:** Private subnet (no internet access)
- **Security:** Security group controls traffic
- **Benefits:**
  - Isolated environment
  - Controlled network access
  - Enhanced security

### 2. S3 VPC Gateway Endpoint
- **Purpose:** Private connection to S3
- **Type:** Gateway Endpoint (not Interface)
- **Benefits:**
  - No data transfer charges
  - No timeout issues
  - Traffic stays within AWS network
  - No NAT Gateway needed (cost savings)

### 3. File Transfer Flow

```
1. EventBridge triggers Lambda (scheduled or event-based)
2. Lambda connects to SFTP server via VPC
3. Lambda downloads file(s) from SFTP
4. Lambda uploads to S3 via Gateway Endpoint
5. CloudWatch logs capture execution details
6. S3 event notifications trigger downstream processing (optional)
```

### 4. Security Layers

**Network Security:**
- VPC isolation
- Security groups
- Private subnets
- VPC Gateway Endpoint

**IAM Security:**
- Lambda execution role
- Least privilege policies
- S3 bucket policies
- VPC endpoint policies

**Data Security:**
- SFTP encryption
- TLS for S3
- S3 encryption at rest
- Secrets Manager for credentials

## Modular Architecture

### Code Organization

```
┌─────────────────────────────────────┐
│  Lambda Handler (Orchestrator)      │
├─────────────────────────────────────┤
│  ├─ File Transfer Service           │
│  │   └─ High-level transfer logic   │
│  ├─ SFTP Client (Utility)           │
│  │   └─ SFTP operations             │
│  ├─ S3 Client (Utility)             │
│  │   └─ S3 operations               │
│  ├─ Logger (Utility)                │
│  │   └─ Centralized logging         │
│  └─ Config (Settings)               │
│      └─ Environment management      │
└─────────────────────────────────────┘
```

### Key Benefits

1. **Reusability:** Each module can be used independently
2. **Testability:** Modules tested in isolation
3. **Maintainability:** Clear separation of concerns
4. **Scalability:** Easy to extend functionality
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
┌─────────┐     ┌──────────┐     ┌─────────┐     ┌─────────┐
│ Trigger │────▶│ Lambda   │────▶│  SFTP   │────▶│  Files  │
└─────────┘     │ Handler  │     │ Client  │     │Downloaded│
                └────┬─────┘     └─────────┘     └────┬────┘
                     │                                 │
                     │                                 │
                     ▼                                 ▼
                ┌─────────┐                      ┌──────────┐
                │ Config  │                      │  Memory  │
                │ Manager │                      │  Buffer  │
                └─────────┘                      └────┬─────┘
                                                      │
                                                      ▼
                                                 ┌──────────┐
                                                 │    S3    │
                                                 │  Client  │
                                                 └────┬─────┘
                                                      │
                                                      ▼
                                                 ┌──────────┐
                                                 │ S3 Bucket│
                                                 └──────────┘
```

## Network Topology

```
VPC (10.0.0.0/16)
│
├─ Private Subnet 1 (10.0.1.0/24) - AZ1
│  ├─ Lambda ENI
│  └─ Security Group
│
├─ Private Subnet 2 (10.0.2.0/24) - AZ2
│  ├─ Lambda ENI (redundancy)
│  └─ Security Group
│
└─ Route Table
   ├─ Local route (10.0.0.0/16)
   └─ S3 Gateway Endpoint (prefix list)
```

## Scalability Considerations

1. **Lambda Concurrency:**
   - Default: 1000 concurrent executions
   - Reserved concurrency for guaranteed capacity
   - Provisioned concurrency for consistent performance

2. **S3 Performance:**
   - Automatic scaling
   - 5,500 PUT/s per prefix
   - Use multiple prefixes for higher throughput

3. **SFTP Connection:**
   - Connection pooling (if needed)
   - Retry logic for transient failures
   - Timeout handling

## Cost Optimization

1. **No NAT Gateway:** Save $0.045/hour + data transfer
2. **S3 Gateway Endpoint:** No data transfer charges
3. **Lambda:** Pay only for execution time
4. **S3 Lifecycle Policies:** Archive old files to Glacier

## Monitoring & Observability

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│ CloudWatch  │──▶│  Dashboards  │──▶│   Alarms    │
│    Logs     │   │              │   │             │
└─────────────┘   └──────────────┘   └─────────────┘
      │
      ├─ Lambda execution logs
      ├─ VPC flow logs
      └─ S3 access logs
```

## Disaster Recovery

1. **Multi-AZ Deployment:** Lambda spans multiple AZs
2. **S3 Durability:** 99.999999999% durability
3. **Versioning:** S3 bucket versioning enabled
4. **Backups:** Automated S3 backup policies
5. **Cross-Region Replication:** Optional for critical data
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
