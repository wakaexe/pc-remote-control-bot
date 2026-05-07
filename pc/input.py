"""
Input control module
Handles keyboard and mouse input
"""
from typing import Tuple, Optional
import pyautogui
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from PIL import ImageGrab
from utils.logger import logger

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# Controllers
keyboard = KeyboardController()
mouse = MouseController()

# Key mapping for special keys
KEY_MAPPING = {
    'enter': Key.enter,
    'return': Key.enter,
    'tab': Key.tab,
    'space': Key.space,
    'backspace': Key.backspace,
    'delete': Key.delete,
    'esc': Key.esc,
    'escape': Key.esc,
    'up': Key.up,
    'down': Key.down,
    'left': Key.left,
    'right': Key.right,
    'home': Key.home,
    'end': Key.end,
    'pageup': Key.page_up,
    'pagedown': Key.page_down,
    'shift': Key.shift,
    'ctrl': Key.ctrl,
    'control': Key.ctrl,
    'alt': Key.alt,
    'win': Key.cmd,
    'cmd': Key.cmd,
    'super': Key.cmd,
    'caps': Key.caps_lock,
    'capslock': Key.caps_lock,
}

# Function keys
for i in range(1, 13):
    KEY_MAPPING[f'f{i}'] = getattr(Key, f'f{i}')

def type_text(text: str) -> str:
    """
    Type text using keyboard

    Args:
        text: Text to type

    Returns:
        Status message
    """
    try:
        pyautogui.write(text, interval=0.05)
        logger.info(f"Typed text: {text[:50]}...")
        return f"⌨️ Typed: {text[:100]}{'...' if len(text) > 100 else ''}"

    except Exception as e:
        logger.error(f"Failed to type text: {e}")
        return f"❌ Error: {str(e)}"

def press_keys(key_combination: str) -> str:
    """
    Press key combination

    Args:
        key_combination: Keys to press (e.g., "Ctrl+C", "Win+R", "Alt+F4")

    Returns:
        Status message
    """
    try:
        keys = [k.strip().lower() for k in key_combination.split('+')]

        if len(keys) == 1:
            # Single key press
            key = keys[0]
            if key in KEY_MAPPING:
                keyboard.press(KEY_MAPPING[key])
                keyboard.release(KEY_MAPPING[key])
            else:
                pyautogui.press(key)

            logger.info(f"Pressed key: {key}")
            return f"⌨️ Pressed: {key}"

        else:
            # Key combination
            mapped_keys = []
            for key in keys:
                if key in KEY_MAPPING:
                    mapped_keys.append(KEY_MAPPING[key])
                else:
                    mapped_keys.append(key)

            # Press all keys
            for key in mapped_keys:
                if isinstance(key, Key):
                    keyboard.press(key)
                else:
                    keyboard.press(key)

            # Release in reverse order
            for key in reversed(mapped_keys):
                if isinstance(key, Key):
                    keyboard.release(key)
                else:
                    keyboard.release(key)

            logger.info(f"Pressed combination: {key_combination}")
            return f"⌨️ Pressed: {key_combination}"

    except Exception as e:
        logger.error(f"Failed to press keys {key_combination}: {e}")
        return f"❌ Error: {str(e)}"

def get_mouse_position() -> str:
    """
    Get current mouse position and pixel color

    Returns:
        Position and color information
    """
    try:
        x, y = pyautogui.position()

        # Get pixel color
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel = screenshot.getpixel((0, 0))
            color = f"RGB({pixel[0]}, {pixel[1]}, {pixel[2]})"
            hex_color = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
        except:
            color = "Unknown"
            hex_color = ""

        logger.info(f"Mouse position: ({x}, {y})")
        return f"🖱️ Mouse position: ({x}, {y})\n🎨 Pixel color: {color} {hex_color}"

    except Exception as e:
        logger.error(f"Failed to get mouse position: {e}")
        return f"❌ Error: {str(e)}"

def click_mouse(x: int, y: int, button: str = 'left') -> str:
    """
    Click mouse at coordinates

    Args:
        x: X coordinate
        y: Y coordinate
        button: Mouse button ('left', 'right', 'middle')

    Returns:
        Status message
    """
    try:
        button_map = {
            'left': Button.left,
            'right': Button.right,
            'middle': Button.middle
        }

        if button not in button_map:
            return f"❌ Invalid button: {button}"

        pyautogui.click(x, y, button=button)

        logger.info(f"Clicked {button} button at ({x}, {y})")
        return f"🖱️ Clicked {button} button at ({x}, {y})"

    except Exception as e:
        logger.error(f"Failed to click at ({x}, {y}): {e}")
        return f"❌ Error: {str(e)}"

def move_mouse(x: int, y: int, duration: float = 0.5) -> str:
    """
    Move mouse to coordinates

    Args:
        x: X coordinate
        y: Y coordinate
        duration: Movement duration in seconds

    Returns:
        Status message
    """
    try:
        pyautogui.moveTo(x, y, duration=duration)

        logger.info(f"Moved mouse to ({x}, {y})")
        return f"🖱️ Moved mouse to ({x}, {y})"

    except Exception as e:
        logger.error(f"Failed to move mouse to ({x}, {y}): {e}")
        return f"❌ Error: {str(e)}"

def scroll_mouse(amount: int) -> str:
    """
    Scroll mouse wheel

    Args:
        amount: Scroll amount (positive = up, negative = down)

    Returns:
        Status message
    """
    try:
        pyautogui.scroll(amount)

        direction = "up" if amount > 0 else "down"
        logger.info(f"Scrolled {direction} by {abs(amount)}")
        return f"🖱️ Scrolled {direction} by {abs(amount)}"

    except Exception as e:
        logger.error(f"Failed to scroll: {e}")
        return f"❌ Error: {str(e)}"

def drag_mouse(x1: int, y1: int, x2: int, y2: int, duration: float = 1.0) -> str:
    """
    Drag mouse from one point to another

    Args:
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate
        duration: Drag duration in seconds

    Returns:
        Status message
    """
    try:
        pyautogui.moveTo(x1, y1)
        pyautogui.drag(x2 - x1, y2 - y1, duration=duration)

        logger.info(f"Dragged from ({x1}, {y1}) to ({x2}, {y2})")
        return f"🖱️ Dragged from ({x1}, {y1}) to ({x2}, {y2})"

    except Exception as e:
        logger.error(f"Failed to drag: {e}")
        return f"❌ Error: {str(e)}"
