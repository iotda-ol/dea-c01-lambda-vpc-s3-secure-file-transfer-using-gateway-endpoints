# Lambda Module - Outputs
# Purpose: Export Lambda function information

output "function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.main.arn
}

output "function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.main.function_name
}

output "function_version" {
  description = "Version of the Lambda function"
  value       = aws_lambda_function.main.version
}

output "function_invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = aws_lambda_function.main.invoke_arn
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda.name
}

output "alias_arn" {
  description = "ARN of the Lambda alias (if created)"
  value       = var.create_alias ? aws_lambda_alias.main[0].arn : null
}
