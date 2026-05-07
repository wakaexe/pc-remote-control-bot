# 🚀 PC Remote Bot - Deployment Guide

## Деплой на Render.com (Бесплатно)

### Шаг 1: Подготовка репозитория

1. Создайте репозиторий на GitHub
2. Загрузите все файлы проекта

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### Шаг 2: Создание сервисов на Render.com

1. Зайдите на https://render.com
2. Нажмите "New +" → "Blueprint"
3. Подключите ваш GitHub репозиторий
4. Render автоматически создаст все сервисы из `render.yaml`:
   - **pc-remote-bot** - основной бот
   - **pc-remote-websocket** - WebSocket сервер
   - **pc-remote-admin** - админ бот
   - **pc-remote-db** - PostgreSQL база данных

### Шаг 3: Настройка переменных окружения

После создания сервисов, проверьте переменные окружения:

**Main Bot (pc-remote-bot):**
- `TELEGRAM_BOT_TOKEN`: YOUR_TELEGRAM_BOT_TOKEN
- `ADMIN_ID`: YOUR_ADMIN_ID
- `GROQ_API_KEY`: your_groq_api_key_here
- `WS_SERVER_URL`: wss://pc-remote-websocket.onrender.com (замените на ваш URL)

**WebSocket Server (pc-remote-websocket):**
- Автоматически получит DATABASE_URL

**Admin Bot (pc-remote-admin):**
- Автоматически получит DATABASE_URL и ADMIN_ID

### Шаг 4: Получение URL WebSocket сервера

1. После деплоя WebSocket сервера, скопируйте его URL
2. Обновите переменную `WS_SERVER_URL` в основном боте:
   - Формат: `wss://pc-remote-websocket.onrender.com`
   - Используйте `wss://` (не `ws://`) для безопасного соединения

### Шаг 5: Инициализация базы данных

База данных автоматически инициализируется при первом запуске.

### Шаг 6: Проверка работы

1. Напишите основному боту: `/start`
2. Зарегистрируйте ПК: `/register`
3. Проверьте админ-бота: `/stats`

## 📱 Установка клиента на ПК пользователя

### Windows:

1. Скачайте клиент с GitHub
2. Установите Python 3.11+
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте `.env` файл:
```env
WS_SERVER_URL=wss://pc-remote-websocket.onrender.com
PC_CLIENT_TOKEN=<ваш_токен_из_бота>
```

5. Запустите клиент:
```bash
python pc_client.py
```

### Автозапуск (Windows):

1. Создайте `.bat` файл:
```batch
@echo off
cd C:\path\to\pc_remote_bot
python pc_client.py
```

2. Добавьте в автозагрузку:
   - Win+R → `shell:startup`
   - Скопируйте `.bat` файл в открывшуюся папку

## 🔧 Troubleshooting

### Бот не отвечает:
- Проверьте логи на Render.com
- Убедитесь, что все сервисы запущены
- Проверьте переменные окружения

### Клиент не подключается:
- Проверьте URL WebSocket сервера
- Убедитесь, что токен правильный
- Проверьте интернет-соединение

### База данных не работает:
- Проверьте, что PostgreSQL сервис запущен
- Убедитесь, что DATABASE_URL правильный

## 💰 Бесплатные лимиты Render.com

- **Web Services**: 750 часов/месяц (достаточно для 3 сервисов 24/7)
- **PostgreSQL**: 1 GB хранилища, 90 дней хранения
- **Bandwidth**: 100 GB/месяц

**Важно:** Бесплатные сервисы засыпают после 15 минут неактивности. Первый запрос может занять ~30 секунд.

## 🎉 Готово!

Теперь ваша система работает на бесплатном хостинге!

**Основной бот:** @your_bot_name
**Админ бот:** @your_admin_bot_name

Пользователи могут регистрировать свои ПК и управлять ими через Telegram!
cd ~
git clone <your-repo> pc_remote_bot
cd pc_remote_bot
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
nano .env  # Add your credentials

# 3. Run
python main.py
```

**Credentials needed**:
- Telegram Bot Token: [@BotFather](https://t.me/botfather)
- Your Telegram ID: [@userinfobot](https://t.me/userinfobot)

---

### Option 2: Windows Autostart

**Time**: 10 minutes

```cmd
# 1. Clone repository
cd C:\
git clone <your-repo> pc_remote_bot
cd pc_remote_bot

# 2. Run installer
cd autostart
install_windows.bat

# 3. Configure .env when prompted
# Bot will start automatically on Windows startup
```

**Features**:
- ✅ Starts with Windows
- ✅ Runs in background
- ✅ Auto-restart on failure

---

### Option 3: Linux Systemd Service

**Time**: 10 minutes

```bash
# 1. Clone repository
cd ~
git clone <your-repo> pc_remote_bot
cd pc_remote_bot

# 2. Run installer
cd autostart
chmod +x install_linux.sh
./install_linux.sh

# 3. Configure .env when prompted
# Service will start automatically
```

**Service commands**:
```bash
sudo systemctl start pc-remote-bot
sudo systemctl stop pc-remote-bot
sudo systemctl restart pc-remote-bot
sudo systemctl status pc-remote-bot
sudo journalctl -u pc-remote-bot -f  # View logs
```

**Features**:
- ✅ Starts on boot
- ✅ Auto-restart on crash
- ✅ System integration
- ✅ Log management

---

### Option 4: Render.com (Free Cloud Hosting)

**Time**: 15 minutes

#### Step 1: Prepare Repository

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

#### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

#### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your repository
3. Configure:
   - **Name**: `pc-remote-bot`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

#### Step 4: Environment Variables

Add these in Render dashboard (Environment tab):

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here
DEEPSEEK_API_KEY=your_deepseek_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
BOT_MODE=webhook
WEBHOOK_URL=https://your-app-name.onrender.com
PORT=10000
SECRET_AUTH_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

**Important**: Replace `your-app-name` with your actual Render app name!

#### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Check logs for "Bot started successfully"
4. Test by sending `/start` to your bot

#### Render Free Tier Notes

**Limitations**:
- Sleeps after 15 minutes of inactivity
- Wakes up when you send a message (30s delay)
- 750 hours/month free (enough for 24/7 if only one service)

**Upgrade to Paid** ($7/month):
- No sleep
- 24/7 uptime
- Faster response

**Keep-Alive Trick** (Free tier):
Use a service like [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes:
- URL to ping: `https://your-app.onrender.com/`
- Interval: 5 minutes
- This keeps the bot awake 24/7 on free tier!

---

### Option 5: Heroku (Alternative Cloud)

**Time**: 15 minutes

#### Prerequisites
```bash
# Install Heroku CLI
# Windows: Download from heroku.com
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

#### Deployment Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
cd ~/pc_remote_bot
heroku create your-app-name

# 3. Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ADMIN_ID=your_id
heroku config:set DEEPSEEK_API_KEY=your_key
heroku config:set BOT_MODE=webhook
heroku config:set WEBHOOK_URL=https://your-app-name.herokuapp.com
heroku config:set PORT=10000

# 4. Create Procfile
echo "web: python main.py" > Procfile

# 5. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 6. Scale
heroku ps:scale web=1

# 7. View logs
heroku logs --tail
```

**Heroku Free Tier**:
- 550-1000 hours/month free
- Sleeps after 30 minutes
- Similar to Render

---

### Option 6: VPS (DigitalOcean, Linode, etc.)

**Time**: 20 minutes

#### Setup on Ubuntu VPS

```bash
# 1. SSH into VPS
ssh root@your-vps-ip

# 2. Update system
apt update && apt upgrade -y

# 3. Install Python
apt install python3 python3-pip git -y

# 4. Clone repository
cd /opt
git clone <your-repo> pc_remote_bot
cd pc_remote_bot

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Configure
cp .env.example .env
nano .env  # Add credentials

# 7. Install as service
cd autostart
chmod +x install_linux.sh
./install_linux.sh

# 8. Check status
systemctl status pc-remote-bot
```

**VPS Advantages**:
- Full control
- No sleep
- Better performance
- Can run other services

**Cost**: $5-10/month

---

## 🔧 Configuration Guide

### Required Environment Variables

```env
# REQUIRED
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789

# OPTIONAL (but recommended for AI features)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# MODE SPECIFIC
BOT_MODE=polling          # For local
BOT_MODE=webhook          # For cloud

# WEBHOOK ONLY
WEBHOOK_URL=https://your-app.onrender.com
PORT=10000
```

### Getting Credentials

#### 1. Telegram Bot Token
```
1. Open Telegram
2. Search: @BotFather
3. Send: /newbot
4. Follow instructions
5. Copy token
```

#### 2. Your Telegram ID
```
1. Open Telegram
2. Search: @userinfobot
3. Send: /start
4. Copy your ID (number)
```

#### 3. DeepSeek API Key
```
1. Go to: platform.deepseek.com
2. Sign up
3. Go to API Keys
4. Create new key
5. Copy key
```

---

## 🧪 Testing Your Deployment

### 1. Check Bot is Running

**Local**:
```bash
ps aux | grep python
# Should show: python main.py
```

**Systemd**:
```bash
systemctl status pc-remote-bot
# Should show: active (running)
```

**Cloud**:
Check logs in Render/Heroku dashboard

### 2. Test Commands

Send to your bot in Telegram:
```
/start          # Should show welcome message
/info           # Should show system info
/screen         # Should send screenshot
/help           # Should show command list
```

### 3. Check Logs

**Local**:
```bash
tail -f logs/bot.log
```

**Systemd**:
```bash
sudo journalctl -u pc-remote-bot -f
```

**Cloud**:
View in dashboard

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check Python version**:
```bash
python --version  # Need 3.10+
```

**Check dependencies**:
```bash
pip install -r requirements.txt
```

**Check .env file**:
```bash
cat .env  # Verify all values are set
```

### Bot Not Responding

**Check bot is running**:
```bash
ps aux | grep python
```

**Check logs**:
```bash
tail -f logs/bot.log
```

**Verify credentials**:
- Bot token is correct
- Admin ID is correct
- No extra spaces in .env

### PyAutoGUI Not Working

**Windows**: Make sure you're logged in with display

**Linux**: Install virtual display
```bash
sudo apt install xvfb
xvfb-run python main.py
```

### Webhook Not Working (Cloud)

**Check environment variables**:
- `BOT_MODE=webhook`
- `WEBHOOK_URL` matches your app URL
- `PORT=10000`

**Check webhook status**:
```python
# Add to main.py temporarily
print(await application.bot.get_webhook_info())
```

---

## 📊 Monitoring

### Check Bot Health

```bash
# CPU usage
top -p $(pgrep -f "python main.py")

# Memory usage
ps aux | grep python

# Disk usage
du -sh ~/pc_remote_bot

# Log size
du -sh ~/pc_remote_bot/logs
```

### Log Rotation

Logs automatically rotate at 10MB (5 backups kept).

Manual cleanup:
```bash
rm ~/pc_remote_bot/logs/bot.log.*
```

---

## 🔒 Security Checklist

Before going live:

- [ ] Changed `SECRET_AUTH_KEY` from default
- [ ] Verified `ADMIN_ID` is correct
- [ ] Bot token is kept secret
- [ ] `.env` file is not in git
- [ ] Firewall configured (if needed)
- [ ] Tested access control
- [ ] Reviewed logs for sensitive data

---

## 🎉 You're Ready!

Choose your deployment method and follow the steps above. Your bot will be controlling your PC remotely in minutes!

**Need help?** Check:
1. README.md - Full documentation
2. QUICKSTART.md - Quick setup
3. TECHNICAL.md - Technical details
4. logs/bot.log - Error logs

---

**Happy remote controlling! 🚀**
