# Security Groups Module - Variables
# Purpose: Define input variables for security group configuration

variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "enable_sftp_egress" {
  description = "Enable SFTP egress rule"
  type        = bool
  default     = true
}

variable "custom_egress_rules" {
  description = "Map of custom egress rules"
  type = map(object({
    description = string
    protocol    = string
    from_port   = number
    to_port     = number
    cidr_ipv4   = string
  }))
  default = {}
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
