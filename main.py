"""
Main entry point for PC Remote Bot
Supports both polling (local) and webhook (Render) modes
Multi-user support with database
"""
import asyncio
import sys
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
import config
from utils.logger import logger
from bot.handler import setup_handlers

# Initialize database
try:
    from database import init_db
    init_db()
    logger.info("✅ Database initialized")
except Exception as e:
    logger.warning(f"Database initialization failed: {e}. Running without DB.")

# Flask app for webhook mode
flask_app = Flask(__name__)

# Global bot application
bot_application: Application = None

@flask_app.route('/')
def index():
    """Health check endpoint"""
    return "PC Remote Bot is running!", 200

@flask_app.route(f'/{config.TELEGRAM_BOT_TOKEN}', methods=['POST'])
async def webhook():
    """Handle webhook updates"""
    try:
        update = Update.de_json(request.get_json(force=True), bot_application.bot)
        await bot_application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "Error", 500

async def setup_webhook(application: Application):
    """Setup webhook for Render deployment"""
    try:
        webhook_url = f"{config.WEBHOOK_URL}/{config.TELEGRAM_BOT_TOKEN}"
        await application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        raise

def run_polling():
    """Run bot in polling mode (for local development)"""
    logger.info("Starting bot in POLLING mode...")

    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Setup handlers
    setup_handlers(application)

    # Start polling
    logger.info("Bot started successfully in polling mode")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

def run_webhook():
    """Run bot in webhook mode (for Render deployment)"""
    global bot_application

    logger.info("Starting bot in WEBHOOK mode...")

    # Create application
    bot_application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Setup handlers
    setup_handlers(bot_application)

    # Setup webhook
    asyncio.run(setup_webhook(bot_application))

    # Start Flask server
    logger.info(f"Starting Flask server on port {config.PORT}")
    flask_app.run(host='0.0.0.0', port=config.PORT)

def main():
    """Main entry point"""
    try:
        logger.info("=" * 50)
        logger.info("PC Remote Bot Starting...")
        logger.info(f"Mode: {config.BOT_MODE}")
        logger.info(f"Admin ID: {config.ADMIN_ID}")
        logger.info("=" * 50)

        if config.BOT_MODE == "webhook":
            run_webhook()
        else:
            run_polling()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
