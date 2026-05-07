# ✅ Installation Checklist

Use this checklist to ensure proper installation and configuration.

## 📋 Pre-Installation

- [ ] Python 3.10+ installed
  ```bash
  python --version
  ```

- [ ] Git installed (if cloning from repository)
  ```bash
  git --version
  ```

- [ ] Internet connection available

- [ ] Telegram account active

---

## 🔑 Credentials Preparation

### 1. Telegram Bot Token
- [ ] Opened [@BotFather](https://t.me/botfather) in Telegram
- [ ] Sent `/newbot` command
- [ ] Followed instructions to create bot
- [ ] Copied bot token (format: `1234567890:ABCdefGHI...`)
- [ ] Saved token securely

### 2. Your Telegram User ID
- [ ] Opened [@userinfobot](https://t.me/userinfobot) in Telegram
- [ ] Sent `/start` command
- [ ] Copied your user ID (format: `123456789`)
- [ ] Saved user ID

### 3. DeepSeek API Key (Optional)
- [ ] Visited [platform.deepseek.com](https://platform.deepseek.com)
- [ ] Created account
- [ ] Generated API key
- [ ] Copied API key (format: `sk-...`)
- [ ] Saved API key

---

## 📦 Installation Steps

### Local Installation

- [ ] Cloned/downloaded repository
  ```bash
  git clone <repo-url> pc_remote_bot
  cd pc_remote_bot
  ```

- [ ] Installed dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Created `.env` file
  ```bash
  cp .env.example .env
  ```

- [ ] Edited `.env` with credentials
  ```bash
  nano .env  # or notepad .env on Windows
  ```

- [ ] Verified `.env` configuration:
  - [ ] `TELEGRAM_BOT_TOKEN` is set
  - [ ] `ADMIN_ID` is set
  - [ ] `BOT_MODE=polling` for local
  - [ ] No extra spaces or quotes

---

## 🚀 First Run

- [ ] Started bot
  ```bash
  python main.py
  ```

- [ ] Checked for errors in console
- [ ] Saw "Bot started successfully" message
- [ ] No error messages in output

---

## 🧪 Testing

### Basic Tests

- [ ] Opened Telegram
- [ ] Found your bot by username
- [ ] Sent `/start` command
- [ ] Received welcome message with menu
- [ ] Sent `/help` command
- [ ] Received command list

### Feature Tests

- [ ] Tested `/info` - received system information
- [ ] Tested `/screen` - received screenshot
- [ ] Tested `/ps` - received process list
- [ ] Tested `/type Hello` - text was typed
- [ ] Tested `/mousepos` - received mouse position
- [ ] Tested `/clip_get` - received clipboard content

### Security Tests

- [ ] Verified only your account can use bot
- [ ] Tested with another account (should be denied)
- [ ] Checked logs for command history
  ```bash
  cat logs/bot.log
  ```

---

## 🔧 Optional: Autostart Setup

### Windows Autostart

- [ ] Ran `autostart/install_windows.bat`
- [ ] Verified bot added to startup folder
- [ ] Restarted computer to test
- [ ] Confirmed bot starts automatically

### Linux Systemd

- [ ] Ran `autostart/install_linux.sh`
- [ ] Checked service status
  ```bash
  systemctl status pc-remote-bot
  ```
- [ ] Verified service is active
- [ ] Restarted computer to test
- [ ] Confirmed bot starts on boot

---

## 🌐 Optional: Cloud Deployment

### Render.com

- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Created new Web Service
- [ ] Connected GitHub repository
- [ ] Set environment variables:
  - [ ] `TELEGRAM_BOT_TOKEN`
  - [ ] `ADMIN_ID`
  - [ ] `DEEPSEEK_API_KEY`
  - [ ] `BOT_MODE=webhook`
  - [ ] `WEBHOOK_URL=https://your-app.onrender.com`
  - [ ] `PORT=10000`
- [ ] Deployed successfully
- [ ] Checked logs for errors
- [ ] Tested bot responds in Telegram

---

## 📝 Post-Installation

### Documentation Review

- [ ] Read README.md
- [ ] Reviewed QUICKSTART.md
- [ ] Checked SECURITY.md
- [ ] Bookmarked DEPLOYMENT.md for reference

### Security Configuration

- [ ] Changed `SECRET_AUTH_KEY` from default
- [ ] Verified `.env` is in `.gitignore`
- [ ] Confirmed bot token is not exposed
- [ ] Set up log monitoring

### Backup

- [ ] Backed up `.env` file (encrypted)
- [ ] Saved credentials in password manager
- [ ] Documented custom configurations

---

## 🐛 Troubleshooting

If something doesn't work:

- [ ] Checked Python version (3.10+)
- [ ] Verified all dependencies installed
- [ ] Confirmed `.env` file exists and is configured
- [ ] Reviewed `logs/bot.log` for errors
- [ ] Tested internet connection
- [ ] Verified bot token is valid
- [ ] Confirmed admin ID is correct
- [ ] Checked firewall settings

---

## ✅ Installation Complete!

When all items are checked:

- ✅ Bot is installed
- ✅ Bot is running
- ✅ Bot responds to commands
- ✅ Security is configured
- ✅ Documentation reviewed

**You're ready to control your PC remotely!** 🎉

---

## 📞 Need Help?

- Check logs: `logs/bot.log`
- Review README.md troubleshooting section
- Check TECHNICAL.md for details
- Verify all checklist items completed

---

**Installation Date**: _____________

**Bot Username**: @_____________

**Notes**:
_________________________________
_________________________________
_________________________________
