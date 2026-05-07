"""
Audio control module
Handles volume control and audio management
"""
import platform
import subprocess
from typing import Optional
from utils.logger import logger

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import cast, POINTER
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

def get_volume() -> str:
    """
    Get current system volume

    Returns:
        Volume level message
    """
    try:
        system = platform.system()

        if system == "Windows" and PYCAW_AVAILABLE:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
            mute = volume.GetMute()

            status = "🔇 Выключен" if mute else f"🔊 {current_volume}%"
            return f"**Громкость:** {status}"

        elif system == "Linux":
            result = subprocess.run(
                ["amixer", "get", "Master"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'Playback' in line and '%' in line:
                    return f"🔊 **Громкость:** {line.strip()}"

        return "❌ Не удалось получить уровень громкости"

    except Exception as e:
        logger.error(f"Failed to get volume: {e}")
        return f"❌ Ошибка: {str(e)}"

def set_volume(level: int) -> str:
    """
    Set system volume

    Args:
        level: Volume level (0-100)

    Returns:
        Status message
    """
    try:
        if level < 0 or level > 100:
            return "❌ Уровень громкости должен быть от 0 до 100"

        system = platform.system()

        if system == "Windows":
            # Use nircmd for Windows (simpler than pycaw)
            subprocess.run(["nircmd.exe", "setsysvolume", str(int(level * 655.35))], check=False)
            logger.info(f"Volume set to {level}%")
            return f"🔊 Громкость установлена на {level}%"

        elif system == "Linux":
            subprocess.run(["amixer", "set", "Master", f"{level}%"], check=True)
            return f"🔊 Громкость установлена на {level}%"

        return "❌ Управление громкостью не поддерживается"

    except Exception as e:
        logger.error(f"Failed to set volume: {e}")
        return f"❌ Ошибка: {str(e)}"

def mute() -> str:
    """
    Mute system audio

    Returns:
        Status message
    """
    try:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["nircmd.exe", "mutesysvolume", "1"], check=False)
            logger.info("Audio muted")
            return "🔇 Звук выключен"

        elif system == "Linux":
            subprocess.run(["amixer", "set", "Master", "mute"], check=True)
            return "🔇 Звук выключен"

        return "❌ Управление звуком не поддерживается"

    except Exception as e:
        logger.error(f"Failed to mute: {e}")
        return f"❌ Ошибка: {str(e)}"

def unmute() -> str:
    """
    Unmute system audio

    Returns:
        Status message
    """
    try:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["nircmd.exe", "mutesysvolume", "0"], check=False)
            logger.info("Audio unmuted")
            return "🔊 Звук включен"

        elif system == "Linux":
            subprocess.run(["amixer", "set", "Master", "unmute"], check=True)
            return "🔊 Звук включен"

        return "❌ Управление звуком не поддерживается"

    except Exception as e:
        logger.error(f"Failed to unmute: {e}")
        return f"❌ Ошибка: {str(e)}"
