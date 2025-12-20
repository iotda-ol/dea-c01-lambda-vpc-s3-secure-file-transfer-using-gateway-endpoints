# IAM Module - Variables
# Purpose: Define input variables for IAM configuration

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "s3_bucket_arns" {
  description = "List of S3 bucket ARNs to grant access to"
  type        = list(string)
}

variable "enable_secrets_manager" {
  description = "Enable Secrets Manager access"
  type        = bool
  default     = false
}

variable "secrets_arns" {
  description = "List of Secrets Manager ARNs"
  type        = list(string)
  default     = []
}

variable "enable_kms" {
  description = "Enable KMS access"
  type        = bool
  default     = false
}

variable "kms_key_arns" {
  description = "List of KMS key ARNs"
  type        = list(string)
  default     = []
}

variable "enable_xray" {
  description = "Enable X-Ray tracing"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
