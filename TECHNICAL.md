# PC Remote Bot - Technical Documentation

## Architecture Overview

### Design Principles
- **Modular Architecture**: Separated concerns (bot, pc control, utilities)
- **Security First**: Access control, rate limiting, input sanitization
- **Error Handling**: Comprehensive try-catch blocks with logging
- **Scalability**: Supports both polling (local) and webhook (cloud) modes

### Component Breakdown

#### 1. Bot Layer (`bot/`)
- **handler.py**: Command handlers and callback processing
- **ai_assistant.py**: DeepSeek API integration with conversation history
- **keyboards.py**: Inline keyboard layouts for interactive UI

#### 2. PC Control Layer (`pc/`)
- **system.py**: OS-level operations (shutdown, reboot, lock, info)
- **files.py**: File system operations with path sanitization
- **screen.py**: Screenshot capture with multi-monitor support
- **input.py**: Keyboard and mouse automation via PyAutoGUI/pynput
- **processes.py**: Process management using psutil
- **clipboard.py**: Clipboard operations via pyperclip
- **audio.py**: Placeholder for future audio features

#### 3. Utilities Layer (`utils/`)
- **logger.py**: Rotating file logger with console output
- **security.py**: Access control decorators and rate limiting
- **helpers.py**: Common utilities (formatting, validation, etc.)

#### 4. Configuration (`config.py`)
- Environment variable loading
- Path management
- Constants and settings

#### 5. Entry Point (`main.py`)
- Flask server for webhook mode
- Polling loop for local mode
- Application initialization

## Security Model

### Authentication
- Single admin ID verification
- Decorator-based access control (`@check_access`)
- Unauthorized access logging and notification

### Rate Limiting
- 10 commands per minute per user
- Sliding window implementation
- Automatic cleanup of old timestamps

### Input Validation
- Path sanitization to prevent directory traversal
- Shell command logging (dangerous patterns detected)
- File size limits (50MB)
- Safe deletion checks (prevents system directory removal)

### Logging
- All commands logged with user ID, username, timestamp
- Rotating log files (10MB max, 5 backups)
- Separate success/failure tracking

## AI Assistant Implementation

### Conversation Flow
1. User sends `/ai <message>` or just text in AI mode
2. Message added to conversation history (max 10 exchanges)
3. History sent to DeepSeek API with system prompt
4. Response parsed for action commands (JSON format)
5. Actions executed automatically if detected

### Action Format
```json
{
  "action": "command_name",
  "params": {
    "key": "value"
  }
}
```

### Supported Actions
- `shell`: Execute terminal command
- `type`: Type text
- `press`: Press key combination
- `click`: Click mouse
- `screen`: Take screenshot
- `info`: Get system info
- `open`: Open application/URL

## Deployment Modes

### Polling Mode (Local)
- Continuous polling of Telegram API
- Best for: Local development, personal use
- Pros: Simple, no external dependencies
- Cons: Requires bot to run continuously

### Webhook Mode (Cloud)
- Telegram sends updates to webhook URL
- Best for: Cloud hosting (Render, Heroku, etc.)
- Pros: Efficient, scales better
- Cons: Requires HTTPS endpoint

## Performance Considerations

### Memory Management
- Conversation history limited to 10 exchanges per user
- Log rotation prevents unbounded growth
- Temporary files cleaned up after operations

### Network Optimization
- Async/await for non-blocking operations
- File size limits prevent bandwidth issues
- Screenshot compression (PNG format)

### CPU Usage
- PyAutoGUI operations are lightweight
- Process listing cached for 1 second
- Shell commands have 30-second timeout

## Error Handling Strategy

### Levels of Error Handling
1. **Function Level**: Try-catch in each operation
2. **Handler Level**: Graceful degradation in command handlers
3. **Application Level**: Global exception handler in main.py

### Error Response Pattern
```python
try:
    # Operation
    return success_message
except SpecificError as e:
    logger.error(f"Context: {e}")
    return user_friendly_message
```

## Testing Recommendations

### Unit Tests (Not Included)
- Mock Telegram API calls
- Test path sanitization
- Verify rate limiting logic
- Test AI response parsing

### Integration Tests
- Test each command end-to-end
- Verify file operations
- Test screenshot capture
- Validate AI integration

### Security Tests
- Attempt directory traversal
- Test unauthorized access
- Verify rate limiting
- Test command injection prevention

## Extending the Bot

### Adding New Commands

1. **Create handler function**:
```python
@check_access
@rate_limit
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_command(user.id, user.username, "/mycommand")
    
    # Your logic here
    result = do_something()
    
    await update.message.reply_text(result)
```

2. **Register handler** in `setup_handlers()`:
```python
application.add_handler(CommandHandler("mycommand", my_command))
```

3. **Add to help text** in `help_command()`

### Adding New PC Operations

1. Create function in appropriate `pc/` module
2. Add to `pc/__init__.py` exports
3. Call from handler
4. Add error handling and logging

### Adding New AI Actions

1. Update `AI_SYSTEM_PROMPT` in `config.py`
2. Add action mapping in `get_action_command()`
3. Test with natural language queries

## Monitoring and Maintenance

### Log Analysis
```bash
# View recent logs
tail -f logs/bot.log

# Search for errors
grep ERROR logs/bot.log

# Count commands by type
grep "SUCCESS" logs/bot.log | awk '{print $8}' | sort | uniq -c
```

### Health Checks
- Monitor bot uptime
- Check log file size
- Verify webhook status (cloud mode)
- Test critical commands periodically

### Backup Strategy
- Backup `.env` file (encrypted)
- Backup logs directory
- Version control for code changes

## Known Limitations

1. **PyAutoGUI**: Requires active display (doesn't work over RDP without physical monitor)
2. **File Size**: 50MB limit due to Telegram API restrictions
3. **Shell Timeout**: 30 seconds max for command execution
4. **AI Context**: Limited to 10 message exchanges
5. **Render Free Tier**: Sleeps after 15 minutes of inactivity

## Future Enhancements

### Planned Features
- [ ] Screen recording (video capture)
- [ ] Audio recording from microphone
- [ ] Webcam capture
- [ ] Network monitoring
- [ ] Scheduled tasks/cron jobs
- [ ] Multi-user support with roles
- [ ] Encrypted file transfers
- [ ] Remote desktop viewer (VNC-like)

### Optimization Opportunities
- [ ] Redis for rate limiting (multi-instance support)
- [ ] Database for persistent storage
- [ ] Caching for frequently accessed data
- [ ] Compression for large file transfers
- [ ] Batch command execution

## Troubleshooting Guide

### Bot Not Starting
1. Check Python version: `python --version` (need 3.10+)
2. Verify dependencies: `pip install -r requirements.txt`
3. Check `.env` file exists and has correct values
4. Review logs: `cat logs/bot.log`

### Commands Not Working
1. Verify you're using correct admin ID
2. Check rate limiting (wait 1 minute)
3. Review command syntax in `/help`
4. Check logs for specific errors

### PyAutoGUI Issues
- **Windows**: Ensure logged in with display
- **Linux**: Install Xvfb: `sudo apt install xvfb`
- **Linux**: Run with: `xvfb-run python main.py`
- **Mac**: Grant accessibility permissions

### Webhook Issues (Render)
1. Verify `BOT_MODE=webhook` in environment
2. Check `WEBHOOK_URL` matches Render URL
3. View Render logs for errors
4. Test webhook: `curl https://your-app.onrender.com/`

## API Reference

### Environment Variables
See `config.py` for complete list and defaults.

### Command List
See `/help` command output or README.md.

### PC Module Functions
See docstrings in each `pc/*.py` file.

## Contributing Guidelines

1. Follow existing code style
2. Add docstrings to all functions
3. Include error handling
4. Update README.md for new features
5. Test thoroughly before committing
6. Add logging for important operations

## License and Legal

This software is provided as-is for educational and personal use. Users are responsible for:
- Securing their bot token
- Complying with local laws
- Protecting sensitive data
- Using responsibly

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-05  
**Python Version**: 3.10+  
**License**: MIT (or your choice)
