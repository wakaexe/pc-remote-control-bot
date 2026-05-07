"""
Clipboard management module
Handles clipboard operations
"""
import pyperclip
from utils.logger import logger

def get_clipboard() -> str:
    """
    Get current clipboard content

    Returns:
        Clipboard text or error message
    """
    try:
        content = pyperclip.paste()

        if not content:
            return "📋 Clipboard is empty"

        # Truncate if too long
        if len(content) > 4000:
            content = content[:4000] + "\n\n... (truncated)"

        logger.info("Retrieved clipboard content")
        return f"📋 **Clipboard content:**\n\n{content}"

    except Exception as e:
        logger.error(f"Failed to get clipboard: {e}")
        return f"❌ Error: {str(e)}"

def set_clipboard(text: str) -> str:
    """
    Set clipboard content

    Args:
        text: Text to set in clipboard

    Returns:
        Status message
    """
    try:
        pyperclip.copy(text)

        logger.info(f"Set clipboard content: {text[:50]}...")
        return f"✅ Clipboard set to: {text[:100]}{'...' if len(text) > 100 else ''}"

    except Exception as e:
        logger.error(f"Failed to set clipboard: {e}")
        return f"❌ Error: {str(e)}"
