#!/bin/bash
# Run all tests with coverage

echo "Running all tests..."

# Run unit tests
echo "Running unit tests..."
python -m pytest tests/unit/ -v --cov=src --cov-report=term-missing

# Run integration tests
echo "Running integration tests..."
python -m pytest tests/integration/ -v

# Generate HTML coverage report
echo "Generating coverage report..."
python -m pytest tests/ --cov=src --cov-report=html

echo "Coverage report generated: htmlcov/index.html"
