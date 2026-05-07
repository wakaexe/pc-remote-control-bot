# PC Remote Bot - Многопользовательская система

## 🎯 Архитектура

Система состоит из 3 компонентов:

1. **Telegram Bot** (основной бот) - интерфейс для пользователей
2. **WebSocket Server** - сервер для связи бота с клиентами
3. **PC Client Agent** - программа на ПК пользователя
4. **Admin Bot** - панель администратора

## 📦 Установка

### 1. Сервер (Render.com или VPS)

```bash
git clone <your-repo>
cd pc_remote_bot
pip install -r requirements.txt

# Настройте .env файл
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
GROQ_API_KEY=your_groq_key
DATABASE_URL=postgresql://user:pass@host/db
WS_SERVER_URL=ws://your-server:8765

# Запустите сервисы
python websocket_server.py &  # WebSocket сервер
python main.py &               # Telegram бот
python admin_bot.py &          # Админ бот
```

### 2. Клиент на ПК пользователя

```bash
# Скачайте клиент
git clone <your-repo>
cd pc_remote_bot

# Установите зависимости
pip install -r requirements.txt

# Получите токен через бота командой /register
# Создайте .env файл
WS_SERVER_URL=ws://your-server:8765
PC_CLIENT_TOKEN=your_token_from_bot

# Запустите клиент
python pc_client.py
```

## 🚀 Использование

### Для пользователей:

1. **Регистрация ПК:**
   - Напишите боту `/start`
   - Используйте `/register` для получения токена
   - Установите клиент на ПК и введите токен

2. **Управление несколькими ПК:**
   - `/mypcs` - список ваших ПК
   - `/selectpc <id>` - выбрать активный ПК
   - `/renamepc <id> <name>` - переименовать ПК
   - `/deletepc <id>` - удалить ПК

3. **Команды управления:**
   - Все команды работают с выбранным активным ПК
   - `/info`, `/screen`, `/shell`, `/ai` и т.д.

### Для администратора:

**Админ бот** (отдельный бот):
- `/stats` - статистика системы
- `/users` - список пользователей
- `/pcs` - список всех ПК
- `/user <id>` - информация о пользователе
- `/ban <id>` - заблокировать
- `/unban <id>` - разблокировать

## 🔧 Конфигурация

### Переменные окружения (.env):

```env
# Основной бот
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_ID=1384059886

# AI
GROQ_API_KEY=your_groq_api_key_here
AI_PROVIDER=groq

# База данных
DATABASE_URL=sqlite:///bot_database.db  # Локально
# DATABASE_URL=postgresql://user:pass@host/db  # Продакшн

# WebSocket
WS_SERVER_URL=ws://localhost:8765  # Локально
# WS_SERVER_URL=ws://your-server.com:8765  # Продакшн

# Клиент (на ПК пользователя)
PC_CLIENT_TOKEN=получить_через_бота
```

## 📊 База данных

### Таблицы:

- **users** - пользователи Telegram
- **pc_clients** - зарегистрированные ПК
- **commands** - история команд

### Миграция:

```bash
python -c "from database import init_db; init_db()"
```

## 🌐 Деплой на Render.com

1. Создайте PostgreSQL базу (бесплатно)
2. Создайте Web Service для бота
3. Создайте Web Service для WebSocket сервера
4. Настройте переменные окружения
5. Деплой!

## 🔐 Безопасность

- Каждый пользователь управляет только своими ПК
- Токены уникальны и безопасны
- Админ может банить пользователей
- Все команды логируются

## 📝 Токены

**Основной бот:** YOUR_TELEGRAM_BOT_TOKEN
**Админ бот:** YOUR_ADMIN_BOT_TOKEN
**Admin ID:** 1384059886

## 🎉 Готово!

Теперь каждый пользователь может:
- Зарегистрировать несколько ПК
- Управлять ими через Telegram
- Переключаться между ПК
- Использовать AI ассистента

Администратор может:
- Видеть всех пользователей
- Управлять доступом
- Просматривать статистику
