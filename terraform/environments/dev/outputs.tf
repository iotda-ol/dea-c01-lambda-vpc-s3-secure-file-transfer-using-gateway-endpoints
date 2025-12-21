# Development Environment - Outputs
# Purpose: Export important values from deployment

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = module.vpc.private_subnet_ids
}

output "s3_bucket_name" {
  description = "Name of S3 bucket"
  value       = module.s3.bucket_id
}

output "s3_bucket_arn" {
  description = "ARN of S3 bucket"
  value       = module.s3.bucket_arn
}

output "s3_endpoint_id" {
  description = "ID of S3 VPC endpoint"
  value       = module.gateway_endpoint.s3_endpoint_id
}

output "lambda_function_arn" {
  description = "ARN of Lambda function"
  value       = module.lambda.function_arn
}

output "lambda_function_name" {
  description = "Name of Lambda function"
  value       = module.lambda.function_name
}

output "lambda_log_group_name" {
  description = "CloudWatch log group for Lambda"
  value       = module.lambda.log_group_name
}

output "lambda_execution_role_arn" {
  description = "ARN of Lambda execution role"
  value       = module.iam.lambda_execution_role_arn
}
