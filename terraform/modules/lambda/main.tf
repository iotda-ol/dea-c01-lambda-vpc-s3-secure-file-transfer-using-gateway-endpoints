# Lambda Module - Main Configuration
# Purpose: Create and configure Lambda function for file transfer

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Lambda Function
resource "aws_lambda_function" "main" {
  function_name = var.function_name
  description   = var.description
  role          = var.execution_role_arn
  handler       = var.handler
  runtime       = var.runtime
  timeout       = var.timeout
  memory_size   = var.memory_size

  filename         = var.source_code_path
  source_code_hash = filebase64sha256(var.source_code_path)

  # VPC Configuration
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }

  # Environment Variables
  environment {
    variables = merge(
      var.environment_variables,
      {
        LOG_LEVEL = var.log_level
      }
    )
  }

  # Tracing Configuration
  tracing_config {
    mode = var.enable_xray ? "Active" : "PassThrough"
  }

  # Dead Letter Queue
  dynamic "dead_letter_config" {
    for_each = var.dlq_target_arn != null ? [1] : []
    content {
      target_arn = var.dlq_target_arn
    }
  }

  # Reserved Concurrent Executions
  reserved_concurrent_executions = var.reserved_concurrent_executions

  tags = merge(
    var.tags,
    {
      Name = var.function_name
    }
  )
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = var.log_retention_days

  tags = merge(
    var.tags,
    {
      Name = "${var.function_name}-logs"
    }
  )
}

# Lambda Function Alias
resource "aws_lambda_alias" "main" {
  count = var.create_alias ? 1 : 0

  name             = var.alias_name
  description      = "Alias for ${var.function_name}"
  function_name    = aws_lambda_function.main.function_name
  function_version = var.alias_version

  routing_config {
    additional_version_weights = var.alias_routing_weights
  }
}

# EventBridge Rule (Optional)
resource "aws_cloudwatch_event_rule" "schedule" {
  count = var.schedule_expression != null ? 1 : 0

  name                = "${var.function_name}-schedule"
  description         = "Trigger ${var.function_name} on schedule"
  schedule_expression = var.schedule_expression

  tags = merge(
    var.tags,
    {
      Name = "${var.function_name}-schedule"
    }
  )
}

# EventBridge Target
resource "aws_cloudwatch_event_target" "lambda" {
  count = var.schedule_expression != null ? 1 : 0

  rule      = aws_cloudwatch_event_rule.schedule[0].name
  target_id = "LambdaTarget"
  arn       = aws_lambda_function.main.arn

  input = var.schedule_input
}

# Lambda Permission for EventBridge
resource "aws_lambda_permission" "eventbridge" {
  count = var.schedule_expression != null ? 1 : 0

  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule[0].arn
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "errors" {
  count = var.enable_error_alarm ? 1 : 0

  alarm_name          = "${var.function_name}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = var.error_alarm_threshold
  alarm_description   = "This metric monitors lambda errors"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "throttles" {
  count = var.enable_throttle_alarm ? 1 : 0

  alarm_name          = "${var.function_name}-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = var.throttle_alarm_threshold
  alarm_description   = "This metric monitors lambda throttles"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "duration" {
  count = var.enable_duration_alarm ? 1 : 0

  alarm_name          = "${var.function_name}-duration"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Average"
  threshold           = var.duration_alarm_threshold
  alarm_description   = "This metric monitors lambda duration"
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.main.function_name
  }

  tags = var.tags
}
