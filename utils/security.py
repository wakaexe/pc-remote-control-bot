"""
Security utilities for PC Remote Bot
Handles access control and rate limiting with database support
"""
from functools import wraps
from typing import Callable, Dict
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
import config
from .logger import logger

# Import user service for DB operations
try:
    from user_service import UserService
    USE_DATABASE = True
except ImportError:
    USE_DATABASE = False

# Rate limiting storage
_rate_limit_storage: Dict[int, list] = {}

def check_access(func: Callable) -> Callable:
    """
    Decorator to check if user has access to bot commands
    Uses database if available, otherwise falls back to config

    Args:
        func: Handler function to wrap

    Returns:
        Wrapped function with access control
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user

        if not user:
            return

        # Check access using database
        if USE_DATABASE:
            # Auto-register new users
            db_user = UserService.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )

            # Check if user is banned
            if UserService.is_user_banned(user.id):
                await update.message.reply_text(
                    "⛔ Ваш аккаунт заблокирован. Обратитесь к администратору."
                )
                return

        else:
            # Fallback to old authorization system
            if user.id not in config.AUTHORIZED_USERS:
                logger.warning(f"Unauthorized access attempt from user {user.id} (@{user.username})")
                await update.message.reply_text(
                    "⛔ Доступ запрещён. Вы не авторизованы для использования этого бота."
                )

                # Notify admin about unauthorized access
                try:
                    await context.bot.send_message(
                        chat_id=config.ADMIN_ID,
                        text=f"⚠️ Попытка несанкционированного доступа:\n"
                             f"User ID: {user.id}\n"
                             f"Username: @{user.username or 'unknown'}\n"
                             f"Name: {user.full_name}\n"
                             f"Command: {update.message.text}"
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin: {e}")

                return

        return await func(update, context, *args, **kwargs)

    return wrapper

def rate_limit(func: Callable) -> Callable:
    """
    Decorator to implement rate limiting for commands

    Args:
        func: Handler function to wrap

    Returns:
        Wrapped function with rate limiting
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        now = datetime.now()

        # Initialize storage for user if not exists
        if user_id not in _rate_limit_storage:
            _rate_limit_storage[user_id] = []

        # Clean old timestamps (older than 1 minute)
        _rate_limit_storage[user_id] = [
            ts for ts in _rate_limit_storage[user_id]
            if now - ts < timedelta(minutes=1)
        ]

        # Check rate limit
        if len(_rate_limit_storage[user_id]) >= config.MAX_COMMANDS_PER_MINUTE:
            await update.message.reply_text(
                "⚠️ Rate limit exceeded. Please wait a moment before sending more commands."
            )
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return

        # Add current timestamp
        _rate_limit_storage[user_id].append(now)

        return await func(update, context, *args, **kwargs)

    return wrapper

def sanitize_command(command: str) -> str:
    """
    Sanitize shell command to prevent injection

    Args:
        command: Raw command string

    Returns:
        Sanitized command
    """
    # Remove dangerous characters and patterns
    dangerous_patterns = [';', '&&', '||', '|', '`', '$', '>', '<', '\n', '\r']

    sanitized = command
    for pattern in dangerous_patterns:
        if pattern in sanitized:
            logger.warning(f"Dangerous pattern '{pattern}' detected in command: {command}")

    return sanitized

def add_authorized_user(user_id: int) -> bool:
    """
    Add user to authorized list

    Args:
        user_id: Telegram user ID to authorize

    Returns:
        True if added successfully
    """
    if user_id not in config.AUTHORIZED_USERS:
        config.AUTHORIZED_USERS.append(user_id)
        logger.info(f"Added user {user_id} to authorized list")
        return True
    return False

def remove_authorized_user(user_id: int) -> bool:
    """
    Remove user from authorized list

    Args:
        user_id: Telegram user ID to remove

    Returns:
        True if removed successfully
    """
    if user_id in config.AUTHORIZED_USERS and user_id != config.ADMIN_ID:
        config.AUTHORIZED_USERS.remove(user_id)
        logger.info(f"Removed user {user_id} from authorized list")
        return True
    return False
