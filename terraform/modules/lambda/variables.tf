# Lambda Module - Variables
# Purpose: Define input variables for Lambda function configuration

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "description" {
  description = "Description of the Lambda function"
  type        = string
  default     = ""
}

variable "execution_role_arn" {
  description = "ARN of the IAM role for Lambda execution"
  type        = string
}

variable "handler" {
  description = "Function entrypoint in your code"
  type        = string
  default     = "main.handler"
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "timeout" {
  description = "Function timeout in seconds"
  type        = number
  default     = 300

  validation {
    condition     = var.timeout >= 1 && var.timeout <= 900
    error_message = "Timeout must be between 1 and 900 seconds."
  }
}

variable "memory_size" {
  description = "Amount of memory in MB"
  type        = number
  default     = 512

  validation {
    condition     = var.memory_size >= 128 && var.memory_size <= 10240
    error_message = "Memory size must be between 128 MB and 10240 MB."
  }
}

variable "source_code_path" {
  description = "Path to the Lambda deployment package"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for VPC configuration"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security group IDs for VPC configuration"
  type        = list(string)
}

variable "environment_variables" {
  description = "Map of environment variables"
  type        = map(string)
  default     = {}
}

variable "log_level" {
  description = "Logging level"
  type        = string
  default     = "INFO"

  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], var.log_level)
    error_message = "Log level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL."
  }
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 7
}

variable "enable_xray" {
  description = "Enable AWS X-Ray tracing"
  type        = bool
  default     = false
}

variable "dlq_target_arn" {
  description = "ARN of the dead letter queue"
  type        = string
  default     = null
}

variable "reserved_concurrent_executions" {
  description = "Number of concurrent executions to reserve"
  type        = number
  default     = -1
}

variable "create_alias" {
  description = "Create a Lambda alias"
  type        = bool
  default     = false
}

variable "alias_name" {
  description = "Name of the alias"
  type        = string
  default     = "live"
}

variable "alias_version" {
  description = "Function version for the alias"
  type        = string
  default     = "$LATEST"
}

variable "alias_routing_weights" {
  description = "Map of additional version weights for routing"
  type        = map(number)
  default     = {}
}

variable "schedule_expression" {
  description = "Schedule expression for EventBridge (e.g., 'rate(5 minutes)')"
  type        = string
  default     = null
}

variable "schedule_input" {
  description = "Input for scheduled invocations"
  type        = string
  default     = null
}

variable "enable_error_alarm" {
  description = "Enable CloudWatch alarm for errors"
  type        = bool
  default     = true
}

variable "error_alarm_threshold" {
  description = "Threshold for error alarm"
  type        = number
  default     = 1
}

variable "enable_throttle_alarm" {
  description = "Enable CloudWatch alarm for throttles"
  type        = bool
  default     = true
}

variable "throttle_alarm_threshold" {
  description = "Threshold for throttle alarm"
  type        = number
  default     = 1
}

variable "enable_duration_alarm" {
  description = "Enable CloudWatch alarm for duration"
  type        = bool
  default     = false
}

variable "duration_alarm_threshold" {
  description = "Threshold for duration alarm (milliseconds)"
  type        = number
  default     = 60000
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
