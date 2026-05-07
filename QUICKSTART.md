# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Get Your Credentials

**Telegram Bot Token:**
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Your Telegram ID:**
1. Search for [@userinfobot](https://t.me/userinfobot)
2. Send `/start`
3. Copy your ID (a number like: `123456789`)

**DeepSeek API Key (Optional):**
1. Go to [platform.deepseek.com](https://platform.deepseek.com)
2. Sign up and get API key
3. Copy the key

### 2. Install

**Windows:**
```cmd
cd C:\
git clone <your-repo> pc_remote_bot
cd pc_remote_bot
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

**Linux/Mac:**
```bash
cd ~
git clone <your-repo> pc_remote_bot
cd pc_remote_bot
pip3 install -r requirements.txt
cp .env.example .env
nano .env
```

### 3. Configure .env

Edit `.env` file:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
BOT_MODE=polling
```

### 4. Run

```bash
python main.py
```

### 5. Test

Open Telegram, find your bot, send:
```
/start
```

You should see the welcome message! 🎉

## 🔥 Common Issues

**"TELEGRAM_BOT_TOKEN is not set"**
- Make sure `.env` file exists in project root
- Check that values don't have quotes or spaces

**"Access denied"**
- Verify `ADMIN_ID` matches your Telegram user ID
- Get your ID from [@userinfobot](https://t.me/userinfobot)

**PyAutoGUI not working**
- Windows: Make sure you're logged in with a display
- Linux: Install `xvfb` and run with `xvfb-run python main.py`

**Bot not responding**
- Check bot is running: `ps aux | grep python`
- Check logs: `cat logs/bot.log`
- Restart: `Ctrl+C` then `python main.py`

## 📱 First Commands to Try

```
/info          # See your PC specs
/screen        # Take a screenshot
/ps            # See running processes
/type Hello!   # Type text
/press Win+R   # Press Windows key + R
/ls            # List files in home directory
/ai Take a screenshot  # Use AI assistant
```

## 🌐 Deploy to Render (Free 24/7 Hosting)

1. Push code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Create new "Web Service"
4. Connect your GitHub repo
5. Add environment variables (same as .env)
6. Set `BOT_MODE=webhook`
7. Set `WEBHOOK_URL=https://your-app.onrender.com`
8. Deploy!

**Note:** Free tier sleeps after 15 min inactivity. Bot wakes up when you message it (30s delay).

## 🎯 Pro Tips

1. **Autostart on Windows:** Run `autostart/install_windows.bat`
2. **Autostart on Linux:** Run `autostart/install_linux.sh`
3. **View logs:** Check `logs/bot.log` for debugging
4. **Multiple admins:** Use `/auth <SECRET_AUTH_KEY>` to add users
5. **AI mode:** Send `/ai` to start chat, then just type naturally

## 🆘 Need Help?

1. Read full README.md
2. Check logs: `logs/bot.log`
3. Test with simple commands first (`/info`, `/screen`)
4. Make sure firewall isn't blocking Python
5. Verify internet connection

---

**Ready to control your PC from anywhere! 🚀**
