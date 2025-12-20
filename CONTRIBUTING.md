# Contributing to Secure File Transfer Project

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a detailed issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check if the feature has been suggested
2. Create an issue with:
   - Clear description
   - Use case
   - Expected behavior
   - Implementation ideas (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. Make your changes following our standards
4. Add tests for new functionality
5. Update documentation
6. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
8. Create a Pull Request

## Development Standards

### Python Code

- Follow PEP 8 style guide
- Use type hints
- Add docstrings to functions/classes
- Maximum line length: 100 characters
- Use meaningful variable names

Example:
```python
def upload_file(local_path: str, s3_key: str) -> Dict[str, Any]:
    """
    Upload file to S3.
    
    Args:
        local_path: Path to local file
        s3_key: S3 object key
    
    Returns:
        Upload result with metadata
    """
    pass
```

### Terraform Code

- Use consistent formatting (`terraform fmt`)
- Add comments for complex logic
- Use variables for configuration
- Follow naming conventions:
  - Resources: `resource_name`
  - Variables: `variable_name`
  - Modules: `module-name`

### Documentation

- Update README.md for significant changes
- Add architecture diagrams when needed
- Document new configuration options
- Update troubleshooting guide

### Testing

- Write unit tests for new functions
- Add integration tests for workflows
- Ensure existing tests pass
- Aim for >80% code coverage

## Commit Messages

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Add tests
- `chore`: Maintenance

Example:
```
feat: Add retry logic to S3 uploads

Implemented exponential backoff retry logic for S3 upload operations
to handle transient failures.

Closes #123
```

## Review Process

1. Automated checks must pass
2. Code review by maintainer
3. Address feedback
4. Merge when approved

## Questions?

Open an issue or discussion!

Thank you for contributing! 🎉
