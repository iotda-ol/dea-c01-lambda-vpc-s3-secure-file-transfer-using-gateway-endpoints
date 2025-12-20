# S3 Module - Variables
# Purpose: Define input variables for S3 bucket configuration

variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "enable_versioning" {
  description = "Enable versioning for the bucket"
  type        = bool
  default     = true
}

variable "enable_lifecycle_rules" {
  description = "Enable lifecycle rules"
  type        = bool
  default     = true
}

variable "transition_to_ia_days" {
  description = "Days before transitioning to Infrequent Access"
  type        = number
  default     = 30
}

variable "transition_to_glacier_days" {
  description = "Days before transitioning to Glacier"
  type        = number
  default     = 90
}

variable "noncurrent_version_expiration_days" {
  description = "Days before deleting noncurrent versions"
  type        = number
  default     = 30
}

variable "kms_key_id" {
  description = "KMS key ID for encryption (if using SSE-KMS)"
  type        = string
  default     = null
}

variable "vpc_endpoint_id" {
  description = "VPC Endpoint ID for bucket policy"
  type        = string
  default     = null
}

variable "allowed_principal_arns" {
  description = "List of ARNs allowed to access the bucket"
  type        = list(string)
  default     = ["*"]
}

variable "enable_logging" {
  description = "Enable S3 access logging"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
