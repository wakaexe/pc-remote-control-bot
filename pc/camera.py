"""
Camera control module
Handles webcam capture
"""
import cv2
import io
from PIL import Image
from typing import Tuple, Optional
from utils.logger import logger

def take_photo() -> Tuple[bool, str, Optional[bytes]]:
    """
    Take photo from webcam

    Returns:
        Tuple of (success, message, image_bytes)
    """
    try:
        # Try to open webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return False, "❌ Не удалось открыть веб-камеру", None

        # Read frame
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return False, "❌ Не удалось захватить изображение", None

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        img = Image.fromarray(frame_rgb)

        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)

        logger.info("Webcam photo taken")
        return True, "📷 Фото с веб-камеры", img_bytes.getvalue()

    except Exception as e:
        logger.error(f"Failed to take photo: {e}")
        return False, f"❌ Ошибка: {str(e)}", None

def list_cameras() -> str:
    """
    List available cameras

    Returns:
        List of cameras
    """
    try:
        available = []
        for i in range(5):  # Check first 5 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(f"📷 Камера {i}")
                cap.release()

        if not available:
            return "❌ Веб-камеры не найдены"

        return "**Доступные камеры:**\n" + "\n".join(available)

    except Exception as e:
        logger.error(f"Failed to list cameras: {e}")
        return f"❌ Ошибка: {str(e)}"
