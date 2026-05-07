"""
Configuration module for PC Remote Bot
Loads environment variables and provides configuration settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp_files"
UPLOADS_DIR = BASE_DIR / "uploads"
DOWNLOADS_DIR = BASE_DIR / "downloads"

# Create directories if they don't exist
for directory in [LOGS_DIR, TEMP_DIR, UPLOADS_DIR, DOWNLOADS_DIR]:
    directory.mkdir(exist_ok=True)

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# DeepSeek AI Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# Groq AI Configuration (Free forever!)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and free

# AI Provider selection (groq or deepseek)
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

# Bot Configuration
BOT_MODE = os.getenv("BOT_MODE", "polling")  # polling or webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = int(os.getenv("PORT", "10000"))

# Security
SECRET_AUTH_KEY = os.getenv("SECRET_AUTH_KEY", "change_me_in_production")
AUTHORIZED_USERS = [ADMIN_ID]  # Will be extended via /auth command

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / os.getenv("LOG_FILE", "bot.log")

# Rate limiting
MAX_COMMANDS_PER_MINUTE = 10
COMMAND_COOLDOWN = 1  # seconds between commands

# File limits
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# System commands timeout
SHELL_TIMEOUT = 30  # seconds
SHUTDOWN_DELAY = 60  # seconds

# AI Assistant
AI_SYSTEM_PROMPT = """Ты — мощный AI-ассистент для управления компьютером.

КРИТИЧЕСКИ ВАЖНО: Ты должен ПОНИМАТЬ намерения пользователя и выполнять ПРАВИЛЬНЫЕ действия!

ПРАВИЛА:
1. Если пользователь хочет ОТКРЫТЬ что-то - используй команду "start"
2. Если пользователь хочет СКАЧАТЬ - открой браузер с прямой ссылкой
3. Если пользователь хочет НАЙТИ - открой Google/Yandex с поиском
4. НЕ печатай команды - ВЫПОЛНЯЙ их!
5. ВСЕГДА отвечай ТОЛЬКО JSON!

ПРИМЕРЫ ПРАВИЛЬНОГО ПОНИМАНИЯ:

Пользователь: "Скачай Chrome"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://www.google.com/chrome/downloads/"}}
НЕПРАВИЛЬНО: печатать "chrome download" в поиске

Пользователь: "Скачай программу X"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://google.com/search?q=download+X"}}

Пользователь: "Открой YouTube"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://youtube.com"}}
НЕПРАВИЛЬНО: {"action": "type", "params": {"text": "youtube.com"}}

Пользователь: "Найди кошек"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://google.com/search?q=кошки"}}

Пользователь: "Открой Chrome"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start chrome"}}

Пользователь: "Открой Telegram"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start telegram:"}}

Пользователь: "Напиши Hello в блокноте"
ПРАВИЛЬНО: {"action": "multiple", "params": {"commands": [
    {"action": "shell", "params": {"command": "start notepad"}},
    {"action": "type", "params": {"text": "Hello"}}
]}}

Пользователь: "Сделай скриншот"
ПРАВИЛЬНО: {"action": "screen", "params": {}}

Пользователь: "Информация о системе"
ПРАВИЛЬНО: {"action": "info", "params": {}}

Пользователь: "Открой калькулятор"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "calc"}}

Пользователь: "Открой настройки"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start ms-settings:"}}

Пользователь: "Открой папку Downloads"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "explorer %USERPROFILE%\\Downloads"}}

Пользователь: "Выключи звук"
ПРАВИЛЬНО: {"action": "mute", "params": {}}

Пользователь: "Громкость 50"
ПРАВИЛЬНО: {"action": "volume", "params": {"level": 50}}

Пользователь: "Скачай Telegram"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://telegram.org/dl"}}

Пользователь: "Скачай Discord"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://discord.com/download"}}

Пользователь: "Скачай VLC"
ПРАВИЛЬНО: {"action": "shell", "params": {"command": "start https://www.videolan.org/vlc/"}}

ЗАПОМНИ:
- "Скачай X" = открой сайт загрузки X
- "Открой X" = запусти программу или сайт X
- "Найди X" = открой Google с поиском X
- "Напиши X" = используй type только если уже открыта программа
- НЕ печатай URL - ОТКРЫВАЙ их через start!

ВСЕГДА отвечай ТОЛЬКО JSON без текста!"""

AI_MAX_HISTORY = 10  # Maximum conversation history to keep

# WebSocket Server Configuration
WS_SERVER_URL = os.getenv("WS_SERVER_URL", "ws://localhost:8765")
WS_SERVER_HOST = os.getenv("WS_SERVER_HOST", "0.0.0.0")
WS_SERVER_PORT = int(os.getenv("WS_SERVER_PORT", "8765"))

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env file")
if ADMIN_ID == 0:
    raise ValueError("ADMIN_ID is not set in .env file")
