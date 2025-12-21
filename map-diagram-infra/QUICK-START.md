# Quick Start Guide
## Multi-Cloud Infrastructure Deployment

This quick start guide helps you deploy the secure file transfer solution on AWS, GCP, or Azure.

---

## Choose Your Cloud Provider

### Option 1: AWS (Recommended for Cost)
**Monthly Cost:** ~$3.46  
**Best For:** Mature ecosystem, free VPC Gateway Endpoint, extensive AWS integrations

**Quick Deploy:**
```bash
# 1. Install prerequisites
aws configure
terraform init

# 2. Review architecture
cat map-diagram-infra/VISUAL-DIAGRAMS.md | less

# 3. Deploy using Terraform
cd terraform/environments/dev
terraform init
terraform plan
terraform apply

# 4. Configure SFTP credentials
aws secretsmanager put-secret-value \
  --secret-id $(terraform output -raw sftp_secret_arn) \
  --secret-string '{
    "username": "your-username",
    "password": "your-password",
    "host": "sftp.example.com",
    "port": 22
  }'

# 5. Test function
aws lambda invoke \
  --function-name $(terraform output -raw lambda_function_name) \
  response.json
```

---

### Option 2: GCP (Lowest Storage Cost)
**Monthly Cost:** ~$3.11 (without VPC Connector) or ~$54.21 (with VPC Connector)  
**Best For:** BigQuery integration, slightly cheaper storage

**Quick Deploy:**
```bash
# 1. Install prerequisites
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Review GCP-specific architecture
# See INFRASTRUCTURE-COMPOSER.md Section: GCP Cloud Functions

# 3. Create Cloud Functions deployment
cd cloud-functions  # (you'll need to adapt Lambda code)

# 4. Deploy function
gcloud functions deploy file-transfer \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=file_transfer_handler \
  --vpc-connector=projects/PROJECT_ID/locations/REGION/connectors/CONNECTOR \
  --set-env-vars GCS_BUCKET_NAME=your-bucket-name,SECRET_NAME=sftp-credentials

# 5. Create secret
echo -n '{"username":"user","password":"pass","host":"sftp.example.com","port":22}' | \
  gcloud secrets create sftp-credentials --data-file=-

# 6. Test function
gcloud functions call file-transfer --gen2
```

**Note:** You need to adapt the Lambda Python code to Cloud Functions format. See COMPONENT-MAPPING-TABLE.md for SDK differences.

---

### Option 3: Azure (Best for Microsoft Ecosystem)
**Monthly Cost:** ~$4.80  
**Best For:** Microsoft integrations, Active Directory, hybrid cloud

**Quick Deploy:**
```bash
# 1. Install prerequisites
az login
az account set --subscription YOUR_SUBSCRIPTION_ID

# 2. Review Azure-specific architecture
# See INFRASTRUCTURE-COMPOSER.md Section: Azure Functions

# 3. Create resource group
az group create --name file-transfer-rg --location eastus

# 4. Create storage account
az storage account create \
  --name filetransfersa123 \
  --resource-group file-transfer-rg \
  --location eastus \
  --sku Standard_LRS

# 5. Create function app
az functionapp create \
  --resource-group file-transfer-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name file-transfer-func \
  --storage-account filetransfersa123

# 6. Enable VNet integration
az functionapp vnet-integration add \
  --name file-transfer-func \
  --resource-group file-transfer-rg \
  --vnet myVNet \
  --subnet function-subnet

# 7. Create Key Vault and store secret
az keyvault create \
  --name file-transfer-kv \
  --resource-group file-transfer-rg \
  --location eastus

az keyvault secret set \
  --vault-name file-transfer-kv \
  --name sftp-credentials \
  --value '{"username":"user","password":"pass","host":"sftp.example.com","port":22}'

# 8. Deploy function code
func azure functionapp publish file-transfer-func
```

**Note:** You need to adapt the Lambda Python code to Azure Functions format. See COMPONENT-MAPPING-TABLE.md for differences.

---

## Architecture Decision Matrix

Use this matrix to choose the right cloud provider:

| **Criteria** | **AWS** | **GCP** | **Azure** | **Winner** |
|-------------|---------|---------|-----------|-----------|
| **Monthly Cost** | $3.46 | $3.11 (or $54.21) | $4.80 | GCP (without connector) |
| **Setup Complexity** | Low | Medium | Medium | AWS |
| **Private Connectivity Cost** | FREE | FREE (but needs connector) | FREE | AWS/Azure |
| **Documentation Quality** | Excellent | Good | Good | AWS |
| **Existing Infrastructure** | Depends on you | Depends on you | Depends on you | N/A |
| **Storage Cost** | $0.023/GB | $0.020/GB | $0.018/GB | Azure |
| **Serverless Maturity** | Excellent | Good | Good | AWS |
| **Enterprise Integration** | Good | Good | Excellent (MS) | Azure |

---

## Common Configuration Steps (All Providers)

### 1. Prepare SFTP Credentials
```json
{
  "username": "your-sftp-username",
  "password": "your-sftp-password",
  "host": "sftp.example.com",
  "port": 22
}
```

Or with SSH key:
```json
{
  "username": "your-sftp-username",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
  "host": "sftp.example.com",
  "port": 22
}
```

### 2. Configure File Transfer Settings
```bash
# Environment variables (adjust for your cloud provider)
S3_BUCKET_NAME=your-bucket-name          # AWS
GCS_BUCKET_NAME=your-bucket-name         # GCP
STORAGE_ACCOUNT_NAME=your-account-name   # Azure

SFTP_REMOTE_PATH=/remote/path/
LOG_LEVEL=INFO
```

### 3. Test SFTP Connection (Local)
```python
import paramiko

# Test SFTP connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname='sftp.example.com',
    username='your-username',
    password='your-password',
    port=22
)
sftp = ssh.open_sftp()
print(sftp.listdir('/remote/path/'))
sftp.close()
ssh.close()
```

### 4. Monitor Execution
**AWS:**
```bash
aws logs tail /aws/lambda/file-transfer-function --follow
```

**GCP:**
```bash
gcloud logging read "resource.type=cloud_function AND resource.labels.function_name=file-transfer" --limit 50 --format json
```

**Azure:**
```bash
az monitor app-insights query \
  --app file-transfer-func \
  --analytics-query "traces | where timestamp > ago(1h) | order by timestamp desc"
```

---

## Troubleshooting Quick Reference

### Issue: Function Timeout
**Cause:** Cannot reach object storage from serverless function

**Solutions:**
- **AWS:** Verify VPC Gateway Endpoint is attached to route table
- **GCP:** Ensure Private Google Access is enabled on subnet and VPC Connector is configured
- **Azure:** Check Service Endpoint is enabled on subnet and NSG allows outbound to Storage

### Issue: Access Denied to Storage
**Cause:** Insufficient permissions

**Solutions:**
- **AWS:** Check IAM role has `s3:PutObject` permission for specific bucket
- **GCP:** Verify Service Account has `roles/storage.objectCreator` role
- **Azure:** Ensure Managed Identity has `Storage Blob Data Contributor` role assignment

### Issue: Cannot Retrieve Secrets
**Cause:** No permission to access secrets service

**Solutions:**
- **AWS:** Check IAM role has `secretsmanager:GetSecretValue` permission
- **GCP:** Verify Service Account has `roles/secretmanager.secretAccessor` role
- **Azure:** Ensure Managed Identity has Key Vault access policy configured

### Issue: SFTP Connection Failed
**Cause:** Network rules blocking egress or invalid credentials

**Solutions:**
1. Check security group/firewall allows egress to SFTP server on port 22
2. Verify SFTP credentials are correct in secrets service
3. Test SFTP connection from local machine first
4. Check SFTP server is accessible from cloud provider's IP range

---

## Cost Optimization Tips

### 1. Enable Storage Lifecycle Policies
All providers support automatic tiering:
- **AWS:** Standard → Standard-IA (30d) → Glacier IR (90d) → Deep Archive (180d)
- **GCP:** Standard → Nearline (30d) → Coldline (90d) → Archive (365d)
- **Azure:** Hot → Cool (30d) → Archive (90d)

### 2. Optimize Function Memory/Timeout
- Start with 512 MB and adjust based on actual usage
- Set timeout to minimum required (test with larger files)
- Use CloudWatch/Monitoring to track actual resource usage

### 3. Minimize Secret Manager Costs
- Cache secrets in function memory (avoid API calls on every invocation)
- Use environment variables for non-sensitive configuration

### 4. Reduce Logging Costs
- Set appropriate log retention (7-30 days)
- Use structured logging (JSON) for easier filtering
- Only log errors and important events in production

---

## Migration Between Providers

### Exporting from Current Provider
1. Export secrets from current secrets service
2. Download Terraform state (if using Terraform)
3. Document current configuration
4. Export logs for audit trail

### Deploying to New Provider
1. Adapt Terraform configuration using examples in INFRASTRUCTURE-COMPOSER.md
2. Import secrets to new provider's secrets service
3. Adapt function code for new SDK (see COMPONENT-MAPPING-TABLE.md)
4. Deploy infrastructure
5. Test thoroughly in staging environment
6. Cutover during low-traffic period

### Parallel Running (During Migration)
1. Deploy to both providers
2. Split traffic (e.g., 10% new, 90% old)
3. Monitor both systems for 1-2 weeks
4. Gradually increase traffic to new provider
5. Decommission old provider once stable

---

## Security Checklist

Before deploying to production, verify:

- [ ] Serverless function runs in private subnet/network
- [ ] No public internet access required for object storage
- [ ] Security groups/firewall rules are restrictive (egress only)
- [ ] Object storage bucket blocks all public access
- [ ] Encryption at rest enabled (AES-256)
- [ ] Encryption in transit enforced (TLS 1.2+)
- [ ] Secrets stored in dedicated secrets service (not environment variables)
- [ ] IAM/RBAC follows least privilege principle
- [ ] Logging enabled for all API calls
- [ ] Alerts configured for errors and anomalies
- [ ] Backup and disaster recovery plan documented
- [ ] Compliance requirements verified (HIPAA, PCI, etc.)

---

## Next Steps

1. **Review Full Documentation:**
   - [INFRASTRUCTURE-COMPOSER.md](INFRASTRUCTURE-COMPOSER.md) - Detailed architecture
   - [COMPONENT-MAPPING-TABLE.md](COMPONENT-MAPPING-TABLE.md) - Service mappings
   - [VISUAL-DIAGRAMS.md](VISUAL-DIAGRAMS.md) - Visual architecture diagrams

2. **Choose Cloud Provider:**
   - Use the decision matrix above
   - Consider existing infrastructure and team expertise
   - Evaluate monthly costs for your use case

3. **Deploy to Staging:**
   - Follow the quick deploy steps for your chosen provider
   - Test with sample SFTP server and files
   - Monitor logs and metrics

4. **Production Deployment:**
   - Complete security checklist
   - Configure monitoring and alerts
   - Document runbooks and procedures
   - Deploy and monitor closely for first 48 hours

5. **Optimize:**
   - Review cost reports after 1 month
   - Adjust function memory/timeout based on actual usage
   - Implement lifecycle policies for storage
   - Fine-tune alerts to reduce noise

---

## Support and Resources

### Official Documentation
- **AWS:** [Lambda VPC](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html), [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- **GCP:** [Cloud Functions](https://cloud.google.com/functions/docs), [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
- **Azure:** [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/), [Service Endpoints](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)

### Community
- GitHub Issues: [Report bugs or request features](https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/issues)
- Stack Overflow: Tag with `aws-lambda`, `google-cloud-functions`, or `azure-functions`
- Cloud provider forums and support

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-21  
**For detailed architecture, see:** [INFRASTRUCTURE-COMPOSER.md](INFRASTRUCTURE-COMPOSER.md)
