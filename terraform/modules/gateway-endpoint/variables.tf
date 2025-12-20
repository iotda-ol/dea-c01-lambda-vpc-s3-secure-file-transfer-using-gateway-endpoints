# Gateway Endpoint Module - Variables
# Purpose: Define input variables for VPC Gateway Endpoints

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "route_table_ids" {
  description = "List of route table IDs to associate with endpoints"
  type        = list(string)
}

variable "allowed_buckets" {
  description = "List of S3 bucket names to allow access to"
  type        = list(string)
  default     = ["*"]
}

variable "custom_policy" {
  description = "Custom endpoint policy (JSON string)"
  type        = string
  default     = null
}

variable "enable_dynamodb_endpoint" {
  description = "Enable DynamoDB gateway endpoint"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
