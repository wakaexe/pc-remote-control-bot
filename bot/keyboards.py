"""
Inline keyboards for Telegram bot
Provides interactive buttons for user interface
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict

def get_main_menu() -> InlineKeyboardMarkup:
    """
    Get main menu keyboard

    Returns:
        InlineKeyboardMarkup with main menu options
    """
    keyboard = [
        [
            InlineKeyboardButton("💻 Инфо о системе", callback_data="menu_info"),
            InlineKeyboardButton("📁 Файлы", callback_data="menu_files")
        ],
        [
            InlineKeyboardButton("📸 Скриншот", callback_data="menu_screen"),
            InlineKeyboardButton("🔄 Процессы", callback_data="menu_ps")
        ],
        [
            InlineKeyboardButton("⌨️ Ввод", callback_data="menu_input"),
            InlineKeyboardButton("📋 Буфер обмена", callback_data="menu_clip")
        ],
        [
            InlineKeyboardButton("📷 Камера", callback_data="menu_camera"),
            InlineKeyboardButton("🔊 Звук", callback_data="menu_audio")
        ],
        [
            InlineKeyboardButton("🌐 Сеть", callback_data="menu_network"),
            InlineKeyboardButton("⚙️ Система", callback_data="menu_system")
        ],
        [
            InlineKeyboardButton("🤖 AI-ассистент", callback_data="menu_ai")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
    """
    Get confirmation keyboard for dangerous actions

    Args:
        action: Action identifier

    Returns:
        InlineKeyboardMarkup with Yes/No buttons
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ Нет", callback_data=f"cancel_{action}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_file_navigation_keyboard(items: List[Dict], current_page: int = 0, items_per_page: int = 10) -> InlineKeyboardMarkup:
    """
    Get file navigation keyboard

    Args:
        items: List of file/directory items
        current_page: Current page number
        items_per_page: Items to show per page

    Returns:
        InlineKeyboardMarkup with file navigation
    """
    keyboard = []

    # Calculate pagination
    start_idx = current_page * items_per_page
    end_idx = min(start_idx + items_per_page, len(items))
    page_items = items[start_idx:end_idx]

    # Add file/directory buttons
    for item in page_items:
        icon = "📁" if item['is_dir'] else "📄"
        name = item['name'][:40]  # Truncate long names
        callback_data = f"nav_{item['path']}" if item['is_dir'] else f"file_{item['path']}"

        keyboard.append([InlineKeyboardButton(f"{icon} {name}", callback_data=callback_data)])

    # Add pagination buttons
    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{current_page-1}"))
    if end_idx < len(items):
        nav_buttons.append(InlineKeyboardButton("➡️ Вперёд", callback_data=f"page_{current_page+1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    # Add back button
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="menu_files")])

    return InlineKeyboardMarkup(keyboard)

def get_system_control_keyboard() -> InlineKeyboardMarkup:
    """
    Get system control keyboard

    Returns:
        InlineKeyboardMarkup with system control options
    """
    keyboard = [
        [
            InlineKeyboardButton("🔒 Блокировка", callback_data="sys_lock"),
            InlineKeyboardButton("😴 Сон", callback_data="sys_sleep")
        ],
        [
            InlineKeyboardButton("🔄 Перезагрузка", callback_data="sys_reboot_confirm"),
            InlineKeyboardButton("⚡ Выключение", callback_data="sys_shutdown_confirm")
        ],
        [
            InlineKeyboardButton("🔙 Главное меню", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_input_control_keyboard() -> InlineKeyboardMarkup:
    """
    Get input control keyboard

    Returns:
        InlineKeyboardMarkup with input control options
    """
    keyboard = [
        [
            InlineKeyboardButton("⌨️ Печать текста", callback_data="input_type"),
            InlineKeyboardButton("🔘 Нажать клавиши", callback_data="input_press")
        ],
        [
            InlineKeyboardButton("🖱️ Позиция мыши", callback_data="input_mousepos"),
            InlineKeyboardButton("👆 Клик", callback_data="input_click")
        ],
        [
            InlineKeyboardButton("🔙 Назад", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_keyboard() -> InlineKeyboardMarkup:
    """
    Get AI assistant keyboard

    Returns:
        InlineKeyboardMarkup with AI options
    """
    keyboard = [
        [
            InlineKeyboardButton("💬 Начать чат", callback_data="ai_start"),
            InlineKeyboardButton("🛑 Выйти из чата", callback_data="ai_exit")
        ],
        [
            InlineKeyboardButton("🔙 Назад", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_camera_keyboard() -> InlineKeyboardMarkup:
    """
    Get camera control keyboard

    Returns:
        InlineKeyboardMarkup with camera options
    """
    keyboard = [
        [
            InlineKeyboardButton("📷 Сделать фото", callback_data="camera_photo"),
            InlineKeyboardButton("📹 Список камер", callback_data="camera_list")
        ],
        [
            InlineKeyboardButton("🔙 Назад", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_audio_keyboard() -> InlineKeyboardMarkup:
    """
    Get audio control keyboard

    Returns:
        InlineKeyboardMarkup with audio options
    """
    keyboard = [
        [
            InlineKeyboardButton("🔊 Громкость", callback_data="audio_volume"),
            InlineKeyboardButton("🔇 Выключить", callback_data="audio_mute")
        ],
        [
            InlineKeyboardButton("🔉 Включить", callback_data="audio_unmute"),
            InlineKeyboardButton("➕ Громче", callback_data="audio_up")
        ],
        [
            InlineKeyboardButton("➖ Тише", callback_data="audio_down"),
            InlineKeyboardButton("🔙 Назад", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_network_keyboard() -> InlineKeyboardMarkup:
    """
    Get network utilities keyboard

    Returns:
        InlineKeyboardMarkup with network options
    """
    keyboard = [
        [
            InlineKeyboardButton("📡 Инфо о сети", callback_data="net_info"),
            InlineKeyboardButton("🔗 Соединения", callback_data="net_connections")
        ],
        [
            InlineKeyboardButton("📶 WiFi сети", callback_data="net_wifi"),
            InlineKeyboardButton("🔙 Назад", callback_data="menu_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
