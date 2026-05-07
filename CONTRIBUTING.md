# Contributing to PC Remote Bot

Thank you for considering contributing to PC Remote Bot! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** (if available)
3. **Include details**:
   - OS and version
   - Python version
   - Bot version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs
   - Screenshots (if applicable)

### Suggesting Features

1. **Check existing feature requests**
2. **Describe the feature clearly**:
   - What problem does it solve?
   - How should it work?
   - Any implementation ideas?
3. **Consider scope**: Does it fit the project goals?

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Open a pull request**

## 📝 Code Style

### Python Style Guide

Follow PEP 8 with these specifics:

```python
# Imports
import standard_library
from third_party import module
import local_module

# Function definitions
def function_name(param: str) -> str:
    """
    Brief description
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass

# Type hints
def process_data(data: List[Dict[str, Any]]) -> Optional[str]:
    pass

# Docstrings for all public functions
# Comments for complex logic only
# Descriptive variable names
```

### Project Conventions

1. **Error Handling**:
```python
try:
    result = operation()
    logger.info(f"Operation succeeded: {result}")
    return success_message
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return error_message
```

2. **Command Handlers**:
```python
@check_access
@rate_limit
async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_command(user.id, user.username, "/command")
    
    # Implementation
    result = do_something()
    
    await update.message.reply_text(result)
```

3. **Logging**:
```python
logger.info("Normal operation")
logger.warning("Potential issue")
logger.error("Error occurred", exc_info=True)
```

## 🧪 Testing

### Before Submitting

1. **Test all affected commands**
2. **Test on target OS** (Windows/Linux/Mac)
3. **Check for errors in logs**
4. **Verify security implications**
5. **Test edge cases**

### Manual Testing Checklist

- [ ] Bot starts without errors
- [ ] New command works as expected
- [ ] Existing commands still work
- [ ] Error handling works
- [ ] Logging is appropriate
- [ ] Security checks pass
- [ ] Documentation updated

## 📚 Documentation

### Update Documentation

When adding features:
1. **README.md**: Add command to usage section
2. **TECHNICAL.md**: Document implementation details
3. **CHANGELOG.md**: Add entry under [Unreleased]
4. **Docstrings**: Add/update function documentation
5. **Help command**: Update `/help` text

### Documentation Style

- Clear and concise
- Include examples
- Explain why, not just what
- Use proper markdown formatting

## 🔒 Security

### Security Considerations

1. **Input Validation**: Always validate user input
2. **Path Sanitization**: Use `sanitize_path()` for file operations
3. **Access Control**: Use `@check_access` decorator
4. **Logging**: Don't log sensitive data
5. **Error Messages**: Don't expose system details

### Security Review

Before submitting:
- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] No SQL injection vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] No path traversal vulnerabilities
- [ ] Sensitive data not logged
- [ ] Error messages are safe

## 🌳 Branch Strategy

- `main`: Stable releases
- `develop`: Development branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes

## 📋 Commit Messages

Use clear, descriptive commit messages:

```
feat: Add webcam capture command
fix: Resolve screenshot issue on multi-monitor setup
docs: Update installation instructions
refactor: Improve error handling in file operations
test: Add tests for clipboard operations
chore: Update dependencies
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

## 🎯 Priority Areas

### High Priority
- Bug fixes
- Security improvements
- Performance optimizations
- Documentation improvements

### Medium Priority
- New commands
- UI improvements
- Code refactoring
- Test coverage

### Low Priority
- Nice-to-have features
- Code style improvements
- Minor optimizations

## 🚀 Feature Roadmap

### Planned Features
1. Screen recording (video)
2. Audio recording
3. Webcam capture
4. Network monitoring
5. Scheduled tasks
6. Multi-user support
7. Encrypted transfers
8. Remote desktop viewer

### Help Wanted
- Cross-platform testing
- Documentation improvements
- Translation support
- UI/UX enhancements

## 💬 Communication

### Getting Help
- Open an issue for questions
- Check existing documentation
- Review closed issues

### Discussions
- Use GitHub Discussions for ideas
- Be respectful and constructive
- Stay on topic

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT or as specified).

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

## 📞 Contact

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: See SECURITY.md

---

Thank you for contributing to PC Remote Bot! 🎉
