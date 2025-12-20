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
