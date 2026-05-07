"""
Logging utilities for PC Remote Bot
Handles all logging operations with rotation and formatting
"""
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Optional
import config

def setup_logger(name: str = "pc_remote_bot") -> logging.Logger:
    """
    Setup logger with file and console handlers

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # File handler with rotation (10 MB max, 5 backups)
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Global logger instance
logger = setup_logger()

def log_command(
    user_id: int,
    username: Optional[str],
    command: str,
    success: bool = True,
    error: Optional[str] = None
) -> None:
    """
    Log command execution with user details

    Args:
        user_id: Telegram user ID
        username: Telegram username
        command: Command that was executed
        success: Whether command succeeded
        error: Error message if failed
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "SUCCESS" if success else "FAILED"

    log_message = f"[{timestamp}] User {user_id} (@{username or 'unknown'}) - {command} - {status}"

    if error:
        log_message += f" - Error: {error}"

    if success:
        logger.info(log_message)
    else:
        logger.error(log_message)

def get_recent_logs(lines: int = 50) -> str:
    """
    Get recent log entries

    Args:
        lines: Number of lines to retrieve

    Returns:
        Recent log content
    """
    try:
        with open(config.LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return ''.join(recent)
    except FileNotFoundError:
        return "Log file not found"
    except Exception as e:
        return f"Error reading logs: {str(e)}"
