# Security Best Practices

## Overview

This solution implements defense-in-depth security principles aligned with AWS Well-Architected Framework and DEA-C01 security best practices.

## 1. Network Security

### VPC Isolation
- **Private Subnets Only**: Lambda functions run in private subnets with no direct internet access
- **No Public IPs**: Resources don't have public IP addresses
- **Security Groups**: Stateful firewall rules control traffic

### Security Group Configuration
```
Lambda Security Group:
- Ingress: None (Lambda doesn't accept incoming connections)
- Egress:
  - Port 443 (HTTPS) to 0.0.0.0/0 for S3 API calls
  - Port 22 (SFTP) to 0.0.0.0/0 for legacy SFTP access
```

### VPC Gateway Endpoint
- Traffic to S3 never leaves AWS network
- Endpoint policy restricts access to specific bucket and actions
- Route table associations ensure traffic uses endpoint

## 2. Data Encryption

### Encryption in Transit
- **S3**: All API calls use HTTPS (TLS 1.2+)
- **SFTP**: SSH protocol provides encryption
- **Secrets Manager**: API calls use HTTPS
- **CloudWatch Logs**: API calls use HTTPS

### Encryption at Rest
- **S3 Bucket**: AES-256 server-side encryption (SSE-S3)
- **Secrets Manager**: Encrypted with AWS KMS
- **CloudWatch Logs**: Encrypted by default

## 3. Identity and Access Management (IAM)

### Least Privilege Principle

#### Lambda Execution Role - S3 Access
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:PutObject",
    "s3:PutObjectAcl"
  ],
  "Resource": "arn:aws:s3:::bucket-name/*"
}
```
- Only write access to specific bucket
- No read, delete, or list bucket configuration permissions

#### Lambda Execution Role - Secrets Manager
```json
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue"],
  "Resource": "arn:aws:secretsmanager:region:account:secret:secret-name"
}
```
- Only GetSecretValue permission
- Scoped to specific secret ARN

#### Lambda Execution Role - CloudWatch Logs
```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:region:account:log-group:/aws/lambda/function-name:*"
}
```
- Only write access to specific log group
- No read, delete, or configuration permissions

#### Lambda Execution Role - VPC Access
```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:CreateNetworkInterface",
    "ec2:DescribeNetworkInterfaces",
    "ec2:DeleteNetworkInterface",
    "ec2:AssignPrivateIpAddresses",
    "ec2:UnassignPrivateIpAddresses"
  ],
  "Resource": "*"
}
```
- Required for Lambda VPC execution
- Automatically managed by AWS Lambda service

## 4. Secrets Management

### SFTP Credentials in Secrets Manager
- **Never hardcoded**: Credentials stored securely in Secrets Manager
- **Rotation**: Supports automatic rotation (implement based on requirements)
- **Auditing**: All access logged to CloudWatch Logs
- **Encryption**: Encrypted with AWS KMS

### Secret Structure
```json
{
  "username": "sftp_user",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...",
  "host": "sftp.example.com",
  "port": 22
}
```

## 5. S3 Bucket Security

### Public Access Block (All Enabled)
- Block public ACLs
- Block public bucket policies
- Ignore public ACLs
- Restrict public buckets

### Bucket Versioning
- Enabled for data protection
- Protects against accidental deletion
- Maintains file history

### VPC Endpoint Policy
```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::account:role/lambda-role"
  },
  "Action": [
    "s3:PutObject",
    "s3:PutObjectAcl",
    "s3:GetObject",
    "s3:ListBucket"
  ],
  "Resource": [
    "arn:aws:s3:::bucket-name",
    "arn:aws:s3:::bucket-name/*"
  ]
}
```

## 6. Logging and Monitoring

### CloudWatch Logs
- All Lambda invocations logged
- Includes:
  - Execution start/end
  - File transfer operations
  - Errors and exceptions
  - Performance metrics

### CloudWatch Metrics
- Lambda invocation count
- Duration
- Error rate
- Concurrent executions

### Audit Trail
- AWS CloudTrail captures API calls
- S3 access logs (optional, can be enabled)
- Lambda execution logs in CloudWatch

## 7. Compliance Considerations

### Data Residency
- All resources deployed in single AWS region
- Data never crosses region boundaries
- VPC provides network isolation

### Access Control
- IAM for authentication and authorization
- Security groups for network access control
- S3 bucket policies for data access control

### Audit Requirements
- CloudWatch Logs: 7-day retention (configurable)
- CloudTrail: Records all API activity
- S3 versioning: Maintains file history

## 8. Incident Response

### Lambda Function Isolation
- VPC isolation limits blast radius
- No incoming network connections
- Controlled egress rules

### Rollback Capability
- Terraform state management
- S3 versioning for data recovery
- Lambda function versioning (can be enabled)

## 9. Vulnerability Management

### Dependency Management
- Python dependencies specified in requirements.txt
- Regular updates recommended
- Pin versions for reproducibility

### Patch Management
- Lambda runtime managed by AWS
- Automatic security patches for managed services
- VPC infrastructure managed by AWS

## 10. Security Checklist

Before Deployment:
- [ ] Review and customize security group rules
- [ ] Update SFTP credentials in Secrets Manager
- [ ] Review IAM policies for least privilege
- [ ] Enable CloudTrail in AWS account
- [ ] Configure S3 bucket lifecycle policies
- [ ] Set appropriate CloudWatch Logs retention
- [ ] Review VPC endpoint policy
- [ ] Test Lambda function in isolated environment

After Deployment:
- [ ] Verify S3 public access is blocked
- [ ] Test file transfer functionality
- [ ] Review CloudWatch Logs for errors
- [ ] Verify encryption at rest and in transit
- [ ] Monitor CloudWatch metrics
- [ ] Set up CloudWatch alarms for failures
- [ ] Document incident response procedures
- [ ] Schedule regular security reviews

## 11. Security Incident Scenarios

### Compromised SFTP Credentials
1. Rotate credentials in Secrets Manager
2. Review CloudWatch Logs for unauthorized access
3. Check S3 bucket for unexpected files
4. Update Lambda environment if needed

### Lambda Function Abuse
1. Check CloudWatch Logs for unusual activity
2. Review Lambda invocation metrics
3. Update security group rules if needed
4. Rotate IAM role credentials

### S3 Data Breach Attempt
1. Review S3 access logs (if enabled)
2. Check VPC Flow Logs (if enabled)
3. Verify bucket policies and ACLs
4. Review IAM policies for unauthorized changes
