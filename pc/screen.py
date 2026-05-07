"""
Screen capture module
Handles screenshots and screen recording
"""
import io
from pathlib import Path
from typing import Optional, Tuple
import pyautogui
from PIL import Image
from screeninfo import get_monitors
import config
from utils.logger import logger

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

def take_screenshot() -> Tuple[bool, str, Optional[io.BytesIO]]:
    """
    Take screenshot of primary monitor

    Returns:
        Tuple of (success, message, image_bytes)
    """
    try:
        screenshot = pyautogui.screenshot()

        # Convert to bytes
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        logger.info("Screenshot taken")
        return True, "📸 Screenshot captured", img_bytes

    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        return False, f"❌ Error: {str(e)}", None

def take_screenshot_area(x: int, y: int, width: int, height: int) -> Tuple[bool, str, Optional[io.BytesIO]]:
    """
    Take screenshot of specific area

    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of area
        height: Height of area

    Returns:
        Tuple of (success, message, image_bytes)
    """
    try:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Convert to bytes
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        logger.info(f"Screenshot taken of area: ({x}, {y}, {width}, {height})")
        return True, f"📸 Screenshot captured (area: {x},{y} {width}x{height})", img_bytes

    except Exception as e:
        logger.error(f"Failed to take screenshot of area: {e}")
        return False, f"❌ Error: {str(e)}", None

def take_screenshot_all_monitors() -> Tuple[bool, str, Optional[io.BytesIO]]:
    """
    Take screenshot of all monitors combined

    Returns:
        Tuple of (success, message, image_bytes)
    """
    try:
        monitors = get_monitors()

        if len(monitors) == 1:
            return take_screenshot()

        # Calculate total bounding box
        min_x = min(m.x for m in monitors)
        min_y = min(m.y for m in monitors)
        max_x = max(m.x + m.width for m in monitors)
        max_y = max(m.y + m.height for m in monitors)

        total_width = max_x - min_x
        total_height = max_y - min_y

        # Create combined image
        combined = Image.new('RGB', (total_width, total_height))

        for monitor in monitors:
            screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))
            combined.paste(screenshot, (monitor.x - min_x, monitor.y - min_y))

        # Convert to bytes
        img_bytes = io.BytesIO()
        combined.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        logger.info(f"Screenshot taken of all {len(monitors)} monitors")
        return True, f"📸 Screenshot captured ({len(monitors)} monitors)", img_bytes

    except Exception as e:
        logger.error(f"Failed to take screenshot of all monitors: {e}")
        return False, f"❌ Error: {str(e)}", None

def get_screen_size() -> Tuple[int, int]:
    """
    Get screen size

    Returns:
        Tuple of (width, height)
    """
    try:
        size = pyautogui.size()
        return size.width, size.height
    except Exception as e:
        logger.error(f"Failed to get screen size: {e}")
        return 1920, 1080  # Default fallback
