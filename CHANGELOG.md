# Changelog

All notable changes to PC Remote Bot will be documented in this file.

## [1.0.0] - 2026-05-05

### 🎉 Initial Release

#### Added
- **Core Bot Functionality**
  - Telegram bot with python-telegram-bot v20+
  - Support for polling (local) and webhook (cloud) modes
  - Flask server for webhook deployment
  - Comprehensive command handler system
  - Inline keyboard navigation

- **System Control**
  - System information (CPU, RAM, disk, uptime, IP)
  - Shutdown/reboot with confirmation and delay
  - Lock and sleep PC
  - Abort shutdown/reboot
  - Shell command execution with timeout

- **File Management**
  - Directory listing with navigation
  - File download (up to 50MB)
  - File upload to PC
  - Create/delete directories
  - Directory tree view
  - Path sanitization for security

- **Screen Control**
  - Screenshot capture
  - Multi-monitor support
  - Screenshot all monitors

- **Input Control**
  - Type text remotely
  - Press key combinations (Ctrl+C, Win+R, etc.)
  - Mouse position and pixel color
  - Mouse click, move, scroll, drag
  - Support for special keys (F1-F12, arrows, etc.)

- **Process Management**
  - List top processes by CPU/RAM
  - Kill process by PID
  - Process information display

- **Clipboard Operations**
  - Get clipboard content
  - Set clipboard content

- **AI Assistant (DeepSeek Integration)**
  - Natural language PC control
  - Conversation history (10 exchanges)
  - Action parsing and execution
  - Chat mode with /ai and /exit_ai

- **Security Features**
  - Single admin authorization
  - Access control decorators
  - Rate limiting (10 commands/minute)
  - Command logging with timestamps
  - Unauthorized access notifications
  - Confirmation for dangerous actions
  - Path sanitization
  - Safe deletion checks

- **Logging System**
  - Rotating file logs (10MB, 5 backups)
  - Console and file output
  - Command tracking
  - Error logging

- **Deployment Support**
  - Render.com configuration (render.yaml)
  - Windows autostart script
  - Linux systemd service
  - Environment variable configuration

- **Documentation**
  - Comprehensive README.md
  - Quick start guide (QUICKSTART.md)
  - Technical documentation (TECHNICAL.md)
  - Inline command help

#### Technical Details
- Python 3.10+ support
- Async/await architecture
- Modular design (bot, pc, utils)
- Cross-platform (Windows, Linux, macOS)
- 2,810 lines of code
- 18 Python modules

#### Dependencies
- python-telegram-bot 20.8
- pyautogui 0.9.54
- psutil 5.9.8
- flask 3.0.2
- requests 2.31.0
- aiofiles 23.2.1
- keyboard 0.13.5
- mouse 0.7.1
- pillow 10.2.0
- screeninfo 0.8.1
- python-dotenv 1.0.1
- pyperclip 1.8.2
- opencv-python 4.9.0.80
- numpy 1.26.4
- pynput 1.7.6

---

## [1.0.1] - 2026-05-07

### 🔧 Fixed

#### Critical Bugs
1. **Admin Bot - Markdown Parsing Errors**
   - Removed all `**` (bold) markdown symbols
   - Removed `<>` symbols from command descriptions
   - Removed `parse_mode=ParseMode.MARKDOWN` from all messages
   - Admin bot now runs without parsing errors

2. **UserService - Missing Methods**
   - Added `get_user(telegram_id)` method
   - Method now used in security.py for access checks

3. **Security.py - Incorrect Method Calls**
   - Fixed: `UserService.create_user()` → `UserService.get_or_create_user()`
   - Fixed: `UserService.is_user_active()` → `UserService.is_user_banned()`
   - All methods now called correctly

### 📚 Added

#### Documentation
1. **ИНСТРУКЦИЯ_ДЛЯ_ПОЛЬЗОВАТЕЛЕЙ.md**
   - Simple 3-step instruction in Russian
   - FAQ section with common questions
   - Autostart setup instructions
   - Troubleshooting guide

2. **ФИНАЛЬНЫЙ_СТАТУС.md**
   - Complete summary of all fixes
   - Project structure overview
   - Launch instructions
   - Tokens and configuration

#### Features
1. **Multi-user System**
   - Each user manages their own PCs
   - Data isolation between users
   - Unique tokens for each PC
   - Multiple PCs per user support

2. **AI Assistant (Groq Integration)**
   - Switched from DeepSeek to Groq API (free forever)
   - Llama 3.3 70B model
   - Natural language understanding
   - Command execution via AI

3. **Admin Panel**
   - Separate bot for administration
   - System statistics
   - User management
   - Ban/unban functionality

4. **WebSocket Architecture**
   - Real-time client-server communication
   - PC client agent (pc_client.py)
   - WebSocket server (websocket_server.py)
   - Token-based authentication

### ✅ Tested

- ✅ Main bot starts without errors
- ✅ Admin bot starts without errors
- ✅ Database initializes correctly
- ✅ UserService methods work properly
- ✅ Security checks function correctly

---

## [Unreleased]

### Planned Features
- Screen recording (video capture)
- Audio recording from microphone
- Webcam capture
- Network monitoring
- Scheduled tasks
- Multi-user support with roles
- Encrypted file transfers
- Remote desktop viewer

### Known Issues
- PyAutoGUI doesn't work over RDP without physical monitor
- Audio module is placeholder only
- Free Render tier sleeps after 15 minutes

---

## Version History

- **1.0.0** (2026-05-05) - Initial release with full feature set
