"""
Helper utilities for PC Remote Bot
Common utility functions used across the application
"""
import os
import requests
from pathlib import Path
from typing import Optional
from .logger import logger

def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable format

    Args:
        bytes_value: Number of bytes

    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def get_external_ip() -> str:
    """
    Get external IP address

    Returns:
        External IP address or error message
    """
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except Exception as e:
        logger.error(f"Failed to get external IP: {e}")
        return "Unable to fetch"

def sanitize_path(path: str, base_path: Optional[Path] = None) -> Path:
    """
    Sanitize and validate file path to prevent directory traversal

    Args:
        path: Path to sanitize
        base_path: Base directory to restrict access to

    Returns:
        Sanitized Path object

    Raises:
        ValueError: If path is invalid or outside base_path
    """
    try:
        # Convert to Path object
        target_path = Path(path).resolve()

        # If base_path specified, ensure target is within it
        if base_path:
            base_path = base_path.resolve()
            if not str(target_path).startswith(str(base_path)):
                raise ValueError(f"Path {path} is outside allowed directory")

        return target_path
    except Exception as e:
        logger.error(f"Path sanitization failed for {path}: {e}")
        raise ValueError(f"Invalid path: {path}")

def truncate_text(text: str, max_length: int = 4000) -> str:
    """
    Truncate text to fit Telegram message limits

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text with indicator if truncated
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - 50] + "\n\n... (truncated, output too long)"

def escape_markdown(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def get_file_icon(filename: str) -> str:
    """
    Get emoji icon for file type

    Args:
        filename: Name of the file

    Returns:
        Emoji representing file type
    """
    ext = Path(filename).suffix.lower()

    icons = {
        '.txt': '📄',
        '.pdf': '📕',
        '.doc': '📘', '.docx': '📘',
        '.xls': '📗', '.xlsx': '📗',
        '.ppt': '📙', '.pptx': '📙',
        '.zip': '🗜️', '.rar': '🗜️', '.7z': '🗜️',
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
        '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬',
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
        '.py': '🐍',
        '.js': '📜',
        '.html': '🌐',
        '.css': '🎨',
        '.exe': '⚙️',
    }

    return icons.get(ext, '📄')

def is_safe_to_delete(path: Path) -> bool:
    """
    Check if path is safe to delete (not system directory)

    Args:
        path: Path to check

    Returns:
        True if safe to delete
    """
    dangerous_paths = [
        Path.home(),
        Path('/'),
        Path('C:\\'),
        Path('C:\\Windows'),
        Path('C:\\Program Files'),
        Path('C:\\Program Files (x86)'),
        Path('/bin'),
        Path('/usr'),
        Path('/etc'),
        Path('/sys'),
    ]

    path = path.resolve()

    for dangerous in dangerous_paths:
        try:
            dangerous = dangerous.resolve()
            if path == dangerous or str(path).startswith(str(dangerous) + os.sep):
                return False
        except:
            continue

    return True
