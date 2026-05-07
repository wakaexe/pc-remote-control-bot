# Git Commands - Quick Reference

## Первая загрузка на GitHub

### 1. Инициализация репозитория (если еще не сделано)

```bash
cd C:/Users/krugl/pc_remote_bot
git init
```

### 2. Добавление всех файлов

```bash
git add .
```

### 3. Первый коммит

```bash
git commit -m "Initial commit - PC Remote Bot v1.0.1 Production Ready

- Multi-user system with WebSocket architecture
- Groq AI assistant integration (free forever)
- Admin panel for user management
- Complete documentation in Russian and English
- Ready for Render.com deployment
- All bugs fixed and tested"
```

### 4. Создание репозитория на GitHub

1. Откройте https://github.com
2. Нажмите **New repository**
3. Название: `pc-remote-bot`
4. Описание: `Multi-user Telegram bot for remote PC control with AI assistant`
5. Выберите **Public** или **Private**
6. **НЕ** добавляйте README, .gitignore, license (у нас уже есть)
7. Нажмите **Create repository**

### 5. Подключение к GitHub

```bash
# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/pc-remote-bot.git
git branch -M main
git push -u origin main
```

### 6. Проверка

```bash
# Откройте в браузере
https://github.com/YOUR_USERNAME/pc-remote-bot
```

---

## Обновление кода (после изменений)

```bash
# Добавить измененные файлы
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```

---

## Полезные команды

```bash
# Проверить статус
git status

# Посмотреть историю
git log --oneline

# Посмотреть изменения
git diff

# Отменить изменения в файле
git checkout -- filename

# Создать новую ветку
git checkout -b feature-name

# Переключиться на ветку
git checkout main
```

---

## Если возникли проблемы

### Ошибка: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/pc-remote-bot.git
```

### Ошибка: "failed to push some refs"

```bash
git pull origin main --rebase
git push origin main
```

### Забыли добавить файл в .gitignore

```bash
# Удалить из git, но оставить на диске
git rm --cached filename

# Добавить в .gitignore
echo "filename" >> .gitignore

# Закоммитить
git add .gitignore
git commit -m "Update .gitignore"
git push
```

---

## Важно: Не загружайте секретные данные!

Убедитесь, что `.gitignore` содержит:

```
.env
*.log
__pycache__/
*.pyc
.vscode/
.idea/
bot.db
```

Проверьте перед первым push:

```bash
git status
```

Если видите `.env` или `bot.db` в списке - добавьте их в `.gitignore`!

---

## После загрузки на GitHub

Переходите к деплою на Render.com (см. `READY_TO_DEPLOY.md`)
