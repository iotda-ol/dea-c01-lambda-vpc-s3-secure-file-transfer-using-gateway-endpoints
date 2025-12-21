# Development Environment - Variables
# Purpose: Define input variables for dev environment

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
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
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "enable_flow_logs" {
  description = "Enable VPC flow logs"
  type        = bool
  default     = false
}

variable "s3_bucket_name" {
  description = "Name of S3 bucket (must be globally unique)"
  type        = string
}

variable "s3_prefix" {
  description = "S3 object key prefix"
  type        = string
  default     = "uploads/"
}

variable "sftp_host" {
  description = "SFTP server hostname"
  type        = string
}

variable "sftp_port" {
  description = "SFTP server port"
  type        = number
  default     = 22
}

variable "sftp_username" {
  description = "SFTP username"
  type        = string
}

variable "sftp_secret_name" {
  description = "Name of Secrets Manager secret containing SFTP credentials"
  type        = string
}

variable "sftp_secret_arn" {
  description = "ARN of Secrets Manager secret"
  type        = string
}

variable "lambda_source_path" {
  description = "Path to Lambda deployment package"
  type        = string
  default     = "../../../lambda/lambda_function.zip"
}

variable "max_file_size_mb" {
  description = "Maximum file size in MB"
  type        = number
  default     = 100
}

variable "log_level" {
  description = "Lambda log level"
  type        = string
  default     = "INFO"
}

variable "enable_xray" {
  description = "Enable X-Ray tracing"
  type        = bool
  default     = false
}
