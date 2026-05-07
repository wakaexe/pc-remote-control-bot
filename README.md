# 🤖 PC Remote Bot - Многопользовательская система

Мощная система удаленного управления компьютерами через Telegram с AI-ассистентом.

## 🚀 Быстрый деплой на Render.com

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/wakaexe/pc-remote-control-bot)

**Или используйте прямую ссылку:** https://render.com/deploy?repo=https://github.com/wakaexe/pc-remote-control-bot

---

## ✨ Возможности

### 🖥️ Управление системой
- Информация о системе (CPU, RAM, диски, аптайм)
- Выполнение shell команд
- Управление процессами
- Выключение/Перезагрузка/Блокировка/Сон
- Скриншоты и веб-камера

### 📁 Управление файлами
- Просмотр файлов и папок
- Скачивание файлов
- Загрузка файлов на ПК

### ⌨️ Управление вводом
- Печать текста
- Нажатие клавиш
- Управление мышью
- Буфер обмена

### 🔊 Управление звуком
- Регулировка громкости
- Mute/Unmute

### 🌐 Сетевые утилиты
- Информация о сети
- Ping
- Список WiFi сетей

### 🤖 AI-ассистент
- Groq AI (Llama 3.3 70B) - бесплатно навсегда
- Понимает контекст и выполняет команды
- Безлимитное использование

### 👥 Многопользовательская система
- Каждый пользователь управляет своими ПК
- Поддержка нескольких ПК на пользователя
- Переключение между ПК
- Админ-панель для управления

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка .env

```env
TELEGRAM_BOT_TOKEN=8668239227:AAEeCYk5v_s_PSkE7AXYv-koSEyeG5Uv8JM
ADMIN_ID=1384059886
GROQ_API_KEY=your_groq_api_key_here
WS_SERVER_URL=ws://localhost:8765
```

### 3. Запуск сервисов

```bash
# Терминал 1: WebSocket сервер
python websocket_server.py

# Терминал 2: Основной бот
python main.py

# Терминал 3: Админ бот
python admin_bot.py
```

### 4. Установка клиента на ПК

**Windows:**
```bash
install_client.bat
```

**Linux/Mac:**
```bash
chmod +x install_client.sh
./install_client.sh
```

## 📖 Команды для пользователей

### Управление ПК
- `/register [имя]` - Зарегистрировать новый ПК
- `/mypcs` - Список ваших ПК
- `/selectpc <id>` - Выбрать активный ПК
- `/renamepc <id> <имя>` - Переименовать ПК
- `/deletepc <id>` - Удалить ПК

### Системные команды
- `/info` - Информация о системе
- `/shell <команда>` - Выполнить команду
- `/ps` - Список процессов
- `/kill <PID>` - Завершить процесс
- `/shutdown` - Выключить ПК
- `/reboot` - Перезагрузить ПК
- `/lock` - Заблокировать ПК
- `/sleep` - Режим сна

### Скриншоты и камера
- `/screen` - Скриншот
- `/camera` - Фото с веб-камеры

### Файлы
- `/ls [путь]` - Список файлов
- `/download <путь>` - Скачать файл
- Отправьте файл боту для загрузки

### Управление вводом
- `/type <текст>` - Напечатать текст
- `/press <клавиши>` - Нажать клавиши
- `/click <x> <y>` - Кликнуть мышью
- `/mousepos` - Позиция мыши

### Звук
- `/volume [0-100]` - Громкость
- `/mute` - Выключить звук
- `/unmute` - Включить звук

### Сеть
- `/netinfo` - Информация о сети
- `/ping <хост>` - Пинг
- `/wifi` - Список WiFi

### AI-ассистент
- `/ai <сообщение>` - Отправить AI
- `/exit_ai` - Выйти из режима AI

## 🔐 Админ-панель

**Токен админ-бота:** 8740193873:AAEYa2Q4LT2bU-9sJvxPWTmhTfAnzPa5umQ

### Команды администратора
- `/stats` - Статистика системы
- `/users` - Список пользователей
- `/pcs` - Список всех ПК
- `/user <id>` - Информация о пользователе
- `/ban <id>` - Заблокировать
- `/unban <id>` - Разблокировать

## 🌐 Деплой на Render.com

### Автоматический деплой

1. Создайте репозиторий на GitHub
2. Загрузите все файлы
3. Зайдите на https://render.com
4. New + → Blueprint
5. Подключите репозиторий
6. Render создаст все сервисы автоматически

### Что будет создано:
- **pc-remote-bot** - основной бот
- **pc-remote-websocket** - WebSocket сервер
- **pc-remote-admin** - админ бот
- **pc-remote-db** - PostgreSQL база

### После деплоя:
1. Скопируйте URL WebSocket: `wss://pc-remote-websocket.onrender.com`
2. Обновите `WS_SERVER_URL` в основном боте
3. Перезапустите бот

## 📊 Архитектура

```
┌─────────────┐
│   User PC   │
│  (Client)   │
└──────┬──────┘
       │ WebSocket
       ↓
┌─────────────┐
│  WebSocket  │
│   Server    │
└──────┬──────┘
       │
       ↓
┌─────────────┐     ┌──────────────┐
│ Telegram    │────→│  PostgreSQL  │
│    Bot      │     │   Database   │
└─────────────┘     └──────────────┘
       ↑
       │
┌─────────────┐
│   Admin     │
│    Bot      │
└─────────────┘
```

## 🛠️ Технологии

- **Python 3.11+**
- **python-telegram-bot 22.7**
- **WebSockets 16.0**
- **SQLAlchemy 2.0**
- **PostgreSQL / SQLite**
- **Groq AI (Llama 3.3 70B)**

## 📝 Структура проекта

```
pc_remote_bot/
├── bot/
│   ├── handler.py          # Обработчики команд
│   ├── keyboards.py        # Клавиатуры
│   └── ai_assistant.py     # AI ассистент
├── pc/
│   ├── system.py           # Системные функции
│   ├── camera.py           # Камера
│   ├── audio.py            # Звук
│   └── network.py          # Сеть
├── utils/
│   ├── logger.py           # Логирование
│   ├── security.py         # Безопасность
│   └── helpers.py          # Вспомогательные функции
├── database.py             # Модели БД
├── user_service.py         # Сервис пользователей
├── websocket_server.py     # WebSocket сервер
├── pc_client.py            # Клиент для ПК
├── admin_bot.py            # Админ бот
├── main.py                 # Основной бот
├── config.py               # Конфигурация
├── requirements.txt        # Зависимости
├── render.yaml             # Конфиг Render.com
├── Procfile                # Процессы
├── install_client.bat      # Установщик Windows
└── install_client.sh       # Установщик Linux/Mac
```

## 🔒 Безопасность

- Уникальные токены для каждого ПК
- Изоляция пользователей
- Логирование всех команд
- Система бана
- Проверка доступа

## 💰 Бесплатные лимиты

**Render.com:**
- 750 часов/месяц (достаточно для 3 сервисов 24/7)
- PostgreSQL: 1 GB хранилища
- Bandwidth: 100 GB/месяц

**Groq AI:**
- Безлимитное использование
- Бесплатно навсегда

## 🐛 Troubleshooting

### Бот не отвечает
- Проверьте токен
- Проверьте логи
- Убедитесь, что сервисы запущены

### Клиент не подключается
- Проверьте WS_SERVER_URL
- Проверьте токен клиента
- Проверьте firewall

### Команды не выполняются
- Выберите активный ПК: `/selectpc <id>`
- Проверьте статус ПК: `/mypcs`
- Проверьте логи клиента

## 📄 Лицензия

MIT License

## 🤝 Поддержка

Если возникли проблемы - создайте Issue на GitHub.

---

**Создано для удобного управления ПК через Telegram** 🚀
- Process management (list, kill)

### 📁 File Management
- Browse directories with inline navigation
- Download files from PC (up to 50MB)
- Upload files to PC
- Create/delete directories
- Directory tree view

### 📸 Screen Control
- Take screenshots
- Multi-monitor support
- Screenshot specific areas

### ⌨️ Input Control
- Type text remotely
- Press key combinations (Ctrl+C, Win+R, etc.)
- Mouse control (click, move, scroll, drag)
- Get mouse position and pixel color

### 📋 Clipboard
- Get clipboard content
- Set clipboard content

### 🤖 AI Assistant (DeepSeek)
- Natural language PC control
- Execute commands via voice/text
- Conversational interface
- Context-aware responses

### 🔒 Security
- Single admin authorization
- Command logging
- Rate limiting
- Confirmation for dangerous actions
- Path sanitization

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Your Telegram User ID (from [@userinfobot](https://t.me/userinfobot))
- DeepSeek API Key (optional, for AI features)

### Local Installation

1. **Clone or download this repository**
```bash
cd ~/
git clone <your-repo-url> pc_remote_bot
cd pc_remote_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Required variables:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_user_id_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here  # Optional
BOT_MODE=polling  # Use 'polling' for local
```

4. **Run the bot**
```bash
python main.py
```

### Windows Autostart

Run the installation script:
```cmd
cd autostart
install_windows.bat
```

This will:
- Install dependencies
- Create startup script
- Add bot to Windows startup folder

### Linux Autostart (systemd)

Run the installation script:
```bash
cd autostart
chmod +x install_linux.sh
./install_linux.sh
```

This will:
- Install dependencies
- Create systemd service
- Enable autostart on boot

Service commands:
```bash
sudo systemctl start pc-remote-bot
sudo systemctl stop pc-remote-bot
sudo systemctl restart pc-remote-bot
sudo systemctl status pc-remote-bot
sudo journalctl -u pc-remote-bot -f  # View logs
```

## 🌐 Render.com Deployment (Free Hosting)

### Step 1: Prepare Repository
1. Push this code to GitHub/GitLab
2. Make sure `.env` is in `.gitignore` (already configured)

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub/GitLab

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - **Name**: pc-remote-bot
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### Step 4: Set Environment Variables
Add these in Render dashboard:
```
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
DEEPSEEK_API_KEY=your_api_key
BOT_MODE=webhook
WEBHOOK_URL=https://your-app.onrender.com
PORT=10000
```

### Step 5: Deploy
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Bot will start automatically

### Important Notes for Render:
- Free tier sleeps after 15 minutes of inactivity
- Bot will wake up when you send a message (may take 30 seconds)
- For 24/7 uptime, upgrade to paid tier ($7/month)

## 📱 Usage

### Basic Commands

```
/start - Welcome message and main menu
/help - Detailed command reference
/info - System information
/screen - Take screenshot
/ps - List running processes
```

### System Control

```
/shutdown - Shutdown PC (60s delay, with confirmation)
/reboot - Reboot PC (60s delay, with confirmation)
/abort - Cancel shutdown/reboot
/lock - Lock PC
/sleep - Put PC to sleep
```

### Shell Commands

```
/shell <command> - Execute terminal command
Example: /shell dir
Example: /shell ipconfig
```

### File Management

```
/ls [path] - List directory contents
/download <path> - Download file
/upload - Reply to a file to upload it
/mkdir <path> - Create directory
/rm <path> - Delete file/folder
/tree [path] - Show directory tree
```

### Input Control

```
/type <text> - Type text
Example: /type Hello World

/press <keys> - Press key combination
Examples:
  /press Ctrl+C
  /press Win+R
  /press Alt+F4
  /press Enter

/mousepos - Get mouse position
/click <x> <y> [button] - Click at coordinates
/move <x> <y> - Move mouse
/scroll <amount> - Scroll wheel
/drag <x1> <y1> <x2> <y2> - Drag mouse
```

### Clipboard

```
/clip_get - Get clipboard content
/clip_set <text> - Set clipboard content
```

### AI Assistant

```
/ai <message> - Send message to AI
/exit_ai - Exit AI chat mode

Examples:
  /ai Take a screenshot and show me
  /ai What's my CPU usage?
  /ai Open Chrome and go to youtube.com
  /ai Type "Hello World" in notepad
```

### Bot Management

```
/log - Get recent logs
/auth <secret_key> - Authorize new user
/restart_bot - Restart bot
```

## 🎯 AI Assistant Examples

The AI assistant can understand natural language and execute commands:

**User**: "Take a screenshot"
**Bot**: *Takes screenshot and sends it*

**User**: "How much RAM do I have?"
**Bot**: *Checks system info and responds*

**User**: "Open notepad and type Hello World"
**Bot**: *Opens notepad and types the text*

**User**: "What processes are using the most CPU?"
**Bot**: *Lists top processes*

## 🔒 Security Features

- **Single Admin**: Only authorized Telegram ID can use the bot
- **Command Logging**: All actions are logged with timestamps
- **Rate Limiting**: Max 10 commands per minute
- **Confirmations**: Dangerous actions require confirmation
- **Path Sanitization**: Prevents directory traversal attacks
- **Shell Safety**: Dangerous patterns are logged
- **File Size Limits**: 50MB max for uploads/downloads

## 🛠️ Troubleshooting

### Bot not responding
- Check if bot is running: `ps aux | grep python`
- Check logs: `tail -f logs/bot.log`
- Verify `.env` configuration
- Check internet connection

### PyAutoGUI not working
- **Windows**: Make sure you're logged in (not RDP without display)
- **Linux**: Install virtual display: `sudo apt install xvfb`
- Run with virtual display: `xvfb-run python main.py`

### Permission errors (Linux)
- Some commands need sudo (shutdown, reboot)
- Add to sudoers: `sudo visudo`
- Add line: `your_username ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot`

### Webhook not working on Render
- Check environment variables are set
- Verify `BOT_MODE=webhook`
- Check `WEBHOOK_URL` matches your Render URL
- View logs in Render dashboard

## 📁 Project Structure

```
pc_remote_bot/
├── main.py              # Entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── bot/
│   ├── handler.py       # Command handlers
│   ├── ai_assistant.py  # AI integration
│   └── keyboards.py     # Inline keyboards
├── pc/
│   ├── system.py        # System control
│   ├── files.py         # File management
│   ├── screen.py        # Screenshots
│   ├── input.py         # Keyboard/mouse
│   ├── processes.py     # Process management
│   ├── clipboard.py     # Clipboard operations
│   └── audio.py         # Audio (placeholder)
├── utils/
│   ├── logger.py        # Logging
│   ├── security.py      # Access control
│   └── helpers.py       # Utilities
└── autostart/
    ├── install_windows.bat
    └── install_linux.sh
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | Yes | - |
| `ADMIN_ID` | Your Telegram user ID | Yes | - |
| `DEEPSEEK_API_KEY` | DeepSeek API key | No | - |
| `DEEPSEEK_API_URL` | DeepSeek API endpoint | No | https://api.deepseek.com/v1/chat/completions |
| `BOT_MODE` | `polling` or `webhook` | No | polling |
| `WEBHOOK_URL` | Webhook URL (for Render) | No | - |
| `PORT` | Server port (for webhook) | No | 10000 |
| `SECRET_AUTH_KEY` | Key for /auth command | No | change_me |
| `LOG_LEVEL` | Logging level | No | INFO |

## 📝 License

This project is provided as-is for educational and personal use.

## ⚠️ Disclaimer

This bot provides full control over your PC. Use responsibly and ensure:
- Keep your bot token secret
- Only authorize trusted users
- Review logs regularly
- Use strong authentication
- Don't expose sensitive information

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs: `logs/bot.log`
3. Open an issue on GitHub

## 🎉 Credits

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [psutil](https://github.com/giampaolo/psutil)
- [DeepSeek AI](https://www.deepseek.com/)

---

**Made with ❤️ for remote PC control**
