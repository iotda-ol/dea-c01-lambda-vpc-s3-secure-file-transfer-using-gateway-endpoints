variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "secure-file-transfer"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones for subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "sftp_host" {
  description = "SFTP server hostname"
  type        = string
  default     = ""
}

variable "sftp_port" {
  description = "SFTP server port"
  type        = number
  default     = 22
}

variable "sftp_username" {
  description = "SFTP username"
  type        = string
  default     = ""
  sensitive   = true
}

variable "sftp_remote_path" {
  description = "Remote path on SFTP server"
  type        = string
  default     = "/uploads"
}

variable "lambda_schedule_expression" {
  description = "Schedule expression for Lambda function execution (e.g., 'rate(1 hour)' or 'cron(0 12 * * ? *)')"
  type        = string
  default     = "rate(1 hour)"
}

variable "lambda_schedule_enabled" {
  description = "Enable or disable the Lambda function schedule"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "SecureFileTransfer"
    ManagedBy   = "Terraform"
    CostCenter  = "DEA-C01"
  }
}
