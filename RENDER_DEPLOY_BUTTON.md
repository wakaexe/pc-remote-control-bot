# Автоматический деплой на Render.com

## Ссылка для быстрого деплоя

Нажмите на эту кнопку для автоматического деплоя:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/wakaexe/pc-remote-control-bot)

## Или используйте прямую ссылку:

```
https://render.com/deploy?repo=https://github.com/wakaexe/pc-remote-control-bot
```

## Что произойдет:

1. Render откроет страницу деплоя
2. Автоматически обнаружит `render.yaml`
3. Создаст 4 сервиса:
   - PostgreSQL база данных
   - WebSocket сервер
   - Main bot
   - Admin bot
4. Попросит ввести недостающие переменные окружения

## Переменные, которые нужно будет ввести:

### GROQ_API_KEY
```
Используйте ваш ключ из .env файла
```

Все остальные переменные уже настроены в `render.yaml`!

## После деплоя:

1. Дождитесь запуска всех сервисов (5-10 минут)
2. Скопируйте URL WebSocket сервиса
3. Обновите `WS_SERVER_URL` в настройках Main Bot и Admin Bot
4. Перезапустите боты

Готово! 🚀
