# Troubleshooting Guide

## Common Issues and Solutions

### Lambda Function Issues

#### Issue: Lambda timeout after 3 seconds
**Symptoms:**
- Function times out before completing
- CloudWatch logs show "Task timed out after 3.00 seconds"

**Solution:**
1. Increase timeout in Lambda configuration:
   ```hcl
   # terraform/environments/dev/main.tf
   timeout = 300  # 5 minutes
   ```
2. Redeploy with Terraform:
   ```bash
   terraform apply
   ```

#### Issue: Lambda out of memory
**Symptoms:**
- "Process exited before completing request"
- High memory usage in CloudWatch metrics

**Solution:**
1. Increase memory allocation:
   ```hcl
   memory_size = 1024  # 1GB
   ```
2. Optimize code to reduce memory usage
3. Process files in chunks

#### Issue: Lambda VPC timeout
**Symptoms:**
- "Unable to connect to S3"
- Timeout when accessing AWS services

**Solution:**
1. Verify VPC Gateway Endpoint is configured:
   ```bash
   aws ec2 describe-vpc-endpoints
   ```
2. Check security group allows outbound HTTPS (443)
3. Verify route table has endpoint route

---

### S3 Access Issues

#### Issue: Access Denied when uploading to S3
**Symptoms:**
- "Access Denied" error in CloudWatch logs
- Status code 403

**Solution:**
1. Verify IAM role has S3 permissions:
   ```bash
   aws iam get-role-policy --role-name secure-transfer-dev-lambda-execution-role --policy-name lambda-s3-policy
   ```
2. Check S3 bucket policy allows VPC endpoint access
3. Verify bucket exists and name is correct

#### Issue: S3 bucket not found
**Symptoms:**
- "NoSuchBucket" error
- Status code 404

**Solution:**
1. Verify bucket name in environment variables:
   ```bash
   aws lambda get-function-configuration --function-name secure-transfer-dev-function
   ```
2. Check bucket exists:
   ```bash
   aws s3 ls s3://your-bucket-name
   ```
3. Ensure bucket is in the same region

---

### SFTP Connection Issues

#### Issue: Cannot connect to SFTP server
**Symptoms:**
- "Connection refused"
- "Connection timed out"

**Solution:**
1. Verify security group allows outbound on port 22:
   ```bash
   aws ec2 describe-security-groups --group-ids sg-xxxxx
   ```
2. Test connectivity from Lambda VPC:
   - Deploy test Lambda
   - Try telnet to SFTP host:port
3. Check SFTP server allows Lambda's IP range

#### Issue: SFTP authentication failed
**Symptoms:**
- "Authentication failed"
- "Invalid credentials"

**Solution:**
1. Verify credentials in Secrets Manager:
   ```bash
   aws secretsmanager get-secret-value --secret-id dev/sftp-credentials
   ```
2. Check username and password are correct
3. Verify IAM role has Secrets Manager permissions

---

### Terraform Issues

#### Issue: S3 bucket name already exists
**Symptoms:**
- "BucketAlreadyExists"
- Terraform apply fails

**Solution:**
1. Choose a globally unique bucket name
2. Update terraform.tfvars:
   ```hcl
   s3_bucket_name = "my-unique-bucket-name-12345"
   ```

#### Issue: Terraform state locked
**Symptoms:**
- "Error locking state"
- "Lock Info"

**Solution:**
1. Wait for other operations to complete
2. Force unlock (use carefully):
   ```bash
   terraform force-unlock <lock-id>
   ```

#### Issue: Resource already exists
**Symptoms:**
- "AlreadyExists"
- Terraform can't create resource

**Solution:**
1. Import existing resource:
   ```bash
   terraform import module.vpc.aws_vpc.main vpc-xxxxx
   ```
2. Or manually delete conflicting resource
3. Run terraform apply again

---

### Networking Issues

#### Issue: VPC endpoint not working
**Symptoms:**
- S3 requests timing out
- Using NAT gateway instead of endpoint

**Solution:**
1. Verify endpoint is in "available" state:
   ```bash
   aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-xxxxx
   ```
2. Check route table associations
3. Verify endpoint policy allows required actions

#### Issue: DNS resolution failing
**Symptoms:**
- "Could not resolve hostname"
- DNS lookup errors

**Solution:**
1. Enable DNS support in VPC:
   ```hcl
   enable_dns_support   = true
   enable_dns_hostnames = true
   ```
2. Verify VPC DNS settings:
   ```bash
   aws ec2 describe-vpc-attribute --vpc-id vpc-xxxxx --attribute enableDnsSupport
   ```

---

### Security Issues

#### Issue: Cannot retrieve secrets
**Symptoms:**
- "Access denied to secret"
- Secrets Manager errors

**Solution:**
1. Verify IAM role has Secrets Manager permissions
2. Check secret ARN is correct
3. Ensure secret exists in same region

#### Issue: KMS encryption errors
**Symptoms:**
- "KMS key not found"
- Encryption/decryption errors

**Solution:**
1. Verify KMS key exists and is enabled
2. Check IAM role has KMS permissions
3. Ensure key policy allows Lambda role

---

### Performance Issues

#### Issue: Slow file transfers
**Symptoms:**
- Long execution duration
- High network latency

**Solution:**
1. Increase Lambda memory (CPU scales with memory)
2. Use multipart upload for large files
3. Optimize chunk size
4. Consider parallel processing

#### Issue: High costs
**Symptoms:**
- Unexpected AWS bills
- High Lambda duration costs

**Solution:**
1. Optimize Lambda memory/timeout
2. Enable S3 Intelligent-Tiering
3. Set up lifecycle policies
4. Review CloudWatch logs retention

---

### Debugging Tips

#### Enable Debug Logging
```hcl
# terraform/environments/dev/main.tf
environment_variables = {
  LOG_LEVEL = "DEBUG"
}
```

#### View CloudWatch Logs
```bash
# Recent logs
aws logs tail /aws/lambda/secure-transfer-dev-function --since 1h

# Follow logs in real-time
aws logs tail /aws/lambda/secure-transfer-dev-function --follow

# Filter errors
aws logs tail /aws/lambda/secure-transfer-dev-function --filter-pattern "ERROR"
```

#### Check Lambda Metrics
```bash
# View invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-function \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum

# View errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-function \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

#### Test Lambda Locally
```bash
cd lambda
python src/main.py
```

#### Validate Terraform
```bash
cd terraform/environments/dev
terraform validate
terraform fmt -check
```

---

### Getting Help

If you're still stuck:
1. Check CloudWatch logs for detailed error messages
2. Review AWS service quotas and limits
3. Consult AWS documentation
4. Open a GitHub issue with:
   - Error message
   - CloudWatch logs
   - Terraform output
   - Steps to reproduce

---

### Additional Resources

- [AWS Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html)
- [S3 Troubleshooting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshooting.html)
- [VPC Troubleshooting](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-troubleshooting.html)
- [Terraform Troubleshooting](https://www.terraform.io/docs/cli/commands/troubleshooting.html)
