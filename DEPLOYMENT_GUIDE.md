# 🚀 Развёртывание на Render.com (Бесплатно)

## Что вы получите:

✅ **Бесплатный хостинг** - навсегда
✅ **Бесплатная PostgreSQL БД** - 1GB
✅ **HTTPS** - автоматически
✅ **Автоматические деплои** - при push в GitHub
✅ **Мультипользовательская система** - каждый управляет своим ПК

## Шаг 1: Подготовка GitHub репозитория

### 1.1 Создайте репозиторий на GitHub

1. Перейдите на https://github.com
2. Нажмите **New repository**
3. Название: `pc-remote-bot`
4. Сделайте **Private** (приватный)
5. Нажмите **Create repository**

### 1.2 Загрузите код в GitHub

```bash
cd C:\Users\krugl\pc_remote_bot

# Инициализация git
git init
git add .
git commit -m "Initial commit"

# Добавьте remote
git remote add origin https://github.com/ваш-username/pc-remote-bot.git

# Загрузите код
git branch -M main
git push -u origin main
```

## Шаг 2: Регистрация на Render.com

1. Перейдите на https://render.com
2. Нажмите **Get Started**
3. Зарегистрируйтесь через **GitHub**
4. Разрешите доступ к вашему репозиторию

## Шаг 3: Создание PostgreSQL базы данных

1. В Render Dashboard нажмите **New +**
2. Выберите **PostgreSQL**
3. Настройки:
   - **Name**: `pc-remote-db`
   - **Database**: `pc_remote_bot`
   - **User**: `pc_remote_user`
   - **Region**: `Frankfurt` (ближе к России)
   - **Plan**: **Free**
4. Нажмите **Create Database**
5. **Скопируйте Internal Database URL** (понадобится позже)

## Шаг 4: Создание Web Service

1. Нажмите **New +**
2. Выберите **Web Service**
3. Подключите ваш GitHub репозиторий
4. Настройки:
   - **Name**: `pc-remote-bot`
   - **Region**: `Frankfurt`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: **Free**

## Шаг 5: Настройка переменных окружения

В разделе **Environment Variables** добавьте:

```
TELEGRAM_BOT_TOKEN = ваш_токен_бота
ADMIN_ID = ваш_telegram_id
GROQ_API_KEY = ваш_groq_ключ
AI_PROVIDER = groq
BOT_MODE = webhook
WEBHOOK_URL = https://pc-remote-bot.onrender.com
DATABASE_URL = (скопируйте из PostgreSQL Internal URL)
SECRET_AUTH_KEY = любой_случайный_ключ
LOG_LEVEL = INFO
```

## Шаг 6: Деплой

1. Нажмите **Create Web Service**
2. Подождите 5-10 минут (первый деплой)
3. Статус должен стать **Live** 🟢

## Готово! 🎉

Ваш бот теперь работает 24/7 в облаке бесплатно!
