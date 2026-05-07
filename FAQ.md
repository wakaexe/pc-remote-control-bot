# ❓ Frequently Asked Questions (FAQ)

## General Questions

### What is PC Remote Bot?
A Telegram bot that allows you to remotely control your computer from anywhere using Telegram messages. It includes an AI assistant powered by DeepSeek for natural language control.

### Is it free?
Yes, the bot is completely free and open source. You only need:
- Free Telegram account
- Free bot token from @BotFather
- Optional: DeepSeek API key (has free tier)

### What platforms are supported?
- **Windows** 10/11
- **Linux** (Ubuntu, Debian, Fedora, etc.)
- **macOS** (limited testing)

### Is it safe?
Yes, when configured properly:
- Only your Telegram ID can access the bot
- All commands are logged
- Dangerous actions require confirmation
- Path sanitization prevents attacks
- Rate limiting prevents abuse

---

## Installation Questions

### Q: Do I need programming knowledge?
**A:** No! Just follow the QUICKSTART.md guide. Basic command line knowledge helps but isn't required.

### Q: Can I run it on multiple computers?
**A:** Yes! Install the bot on each computer with the same bot token. Each instance will respond to your commands.

### Q: How do I get a bot token?
**A:** 
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot`
4. Follow instructions
5. Copy the token

### Q: How do I find my Telegram user ID?
**A:**
1. Open Telegram
2. Search for @userinfobot
3. Send `/start`
4. Copy the number shown

### Q: Installation fails with "Python not found"
**A:** Install Python 3.10+ from python.org. Make sure to check "Add Python to PATH" during installation.

---

## Configuration Questions

### Q: Where do I put my credentials?
**A:** In the `.env` file in the project root directory. Copy `.env.example` to `.env` and edit it.

### Q: What's the difference between polling and webhook mode?
**A:**
- **Polling** (local): Bot continuously checks for messages. Use for local/home computers.
- **Webhook** (cloud): Telegram sends messages to your server. Use for cloud hosting (Render, Heroku).

### Q: Do I need DeepSeek API key?
**A:** No, it's optional. Without it, all commands work except `/ai` (AI assistant).

---

## Usage Questions

### Q: Bot doesn't respond to my commands
**A:** Check:
1. Bot is running
2. You're using the correct admin ID
3. No typos in commands
4. Check logs: `cat logs/bot.log`

### Q: "Access denied" error
**A:** Your Telegram user ID doesn't match `ADMIN_ID` in `.env`. Get your ID from @userinfobot.

### Q: How do I add more users?
**A:** Send `/auth <SECRET_AUTH_KEY>` from the new user's account. The key is in your `.env` file.

---

## Feature Questions

### Q: Can I take screenshots?
**A:** Yes! Use `/screen` for primary monitor or `/screen_full` for all monitors.

### Q: Can I transfer files?
**A:** Yes! 
- Download: `/download <path>`
- Upload: Send file to bot
- Limit: 50MB (Telegram restriction)

### Q: Can I type in other languages?
**A:** Yes! `/type` supports Unicode, including Cyrillic, Chinese, Arabic, etc.

---

## AI Assistant Questions

### Q: How does the AI assistant work?
**A:** It uses DeepSeek API to understand natural language and convert it to bot commands.

### Q: What can I ask the AI?
**A:** Examples:
- "Take a screenshot"
- "What's my CPU usage?"
- "Type Hello World"
- "Open Chrome"

---

## Deployment Questions

### Q: Should I use local or cloud hosting?
**A:**
- **Local**: Best for home PC, always accessible, no sleep
- **Cloud**: Best for remote server, accessible from anywhere, may sleep on free tier

### Q: Render.com bot sleeps after 15 minutes
**A:** Free tier limitation. Solutions:
1. Upgrade to paid ($7/month)
2. Use UptimeRobot to ping every 5 minutes
3. Accept 30s wake-up delay

---

## Security Questions

### Q: Is my data safe?
**A:** 
- Bot runs on YOUR computer/server
- No data sent to third parties (except DeepSeek for AI)
- Logs stored locally
- Bot token should be kept secret

### Q: Can someone hack my PC through the bot?
**A:** Only if they get your bot token or Telegram account. Keep them secure!

---

## Troubleshooting Questions

### Q: "PyAutoGUI not working"
**A:**
- **Windows**: Make sure you're logged in with display
- **Linux**: Install Xvfb: `sudo apt install xvfb`, run with `xvfb-run python main.py`

### Q: "Permission denied" on Linux
**A:** Some commands need sudo. Configure sudoers carefully.

### Q: Bot crashes randomly
**A:** Check logs: `tail -f logs/bot.log`

---

## Still Have Questions?

- 📖 Read the full documentation: README.md
- 🚀 Quick setup: QUICKSTART.md
- 🔧 Technical details: TECHNICAL.md
- 🐛 Check logs: `logs/bot.log`

---

**Last Updated**: 2026-05-05
