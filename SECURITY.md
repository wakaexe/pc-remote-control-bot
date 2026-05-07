# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Features

### Authentication
- Single admin ID verification
- Unauthorized access logging
- Admin notification on unauthorized attempts

### Rate Limiting
- 10 commands per minute per user
- Automatic cooldown enforcement
- Prevents abuse and DoS

### Input Validation
- Path sanitization (prevents directory traversal)
- Shell command logging
- File size limits (50MB)
- Safe deletion checks

### Data Protection
- Environment variables for sensitive data
- .env file excluded from git
- Logs contain no sensitive information
- Clipboard content truncated in logs

### Command Safety
- Confirmation required for dangerous actions (shutdown, reboot, delete)
- Critical system processes cannot be killed
- System directories cannot be deleted
- Shell timeout prevents hanging

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainer directly (if available)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work on a fix.

## Security Best Practices

### For Users

1. **Protect Your Bot Token**
   - Never commit `.env` to git
   - Never share your bot token
   - Regenerate token if compromised

2. **Secure Your Admin ID**
   - Only authorize trusted users
   - Review logs regularly
   - Use strong SECRET_AUTH_KEY

3. **Network Security**
   - Use HTTPS for webhooks
   - Keep dependencies updated
   - Monitor for suspicious activity

4. **System Security**
   - Run bot with minimal privileges
   - Don't run as root/administrator
   - Use firewall rules

5. **Data Security**
   - Don't send sensitive files through bot
   - Clear clipboard after sensitive operations
   - Review logs before sharing

### For Developers

1. **Code Security**
   - Validate all user input
   - Use parameterized commands
   - Escape special characters
   - Implement proper error handling

2. **Dependency Security**
   - Keep dependencies updated
   - Review dependency vulnerabilities
   - Use pinned versions

3. **API Security**
   - Validate API responses
   - Handle rate limits
   - Implement timeouts
   - Use secure connections (HTTPS)

## Known Security Considerations

### By Design
- Bot has full access to PC (intended functionality)
- Shell commands can execute any system command
- File operations can access any readable file
- No encryption for local storage

### Limitations
- Single admin model (no role-based access)
- No command audit trail beyond logs
- No encryption for file transfers
- Logs stored in plain text

### Mitigations
- Access control via Telegram ID
- Rate limiting prevents abuse
- Confirmations for dangerous actions
- Comprehensive logging

## Security Checklist

Before deploying:
- [ ] Changed SECRET_AUTH_KEY from default
- [ ] Verified ADMIN_ID is correct
- [ ] Bot token is kept secret
- [ ] .env file is not in git
- [ ] Logs directory has proper permissions
- [ ] Firewall configured (if needed)
- [ ] Dependencies are up to date
- [ ] Tested access control
- [ ] Reviewed logs for sensitive data

## Incident Response

If compromised:
1. Stop the bot immediately
2. Regenerate bot token via @BotFather
3. Change SECRET_AUTH_KEY
4. Review logs for unauthorized access
5. Check system for unauthorized changes
6. Update .env with new credentials
7. Restart bot

## Updates and Patches

- Security updates will be released as soon as possible
- Check CHANGELOG.md for security-related changes
- Subscribe to repository for notifications
- Test updates in development before production

## Contact

For security concerns:
- Open a private security advisory on GitHub
- Or contact maintainer directly

---

**Last Updated**: 2026-05-05  
**Version**: 1.0.0
