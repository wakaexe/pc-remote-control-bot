"""
Telegram bot handlers
Main command handlers for the bot
"""
import subprocess
import asyncio
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

import config
from utils.logger import logger, log_command, get_recent_logs
from utils.security import check_access, rate_limit, add_authorized_user
from utils.helpers import truncate_text
from bot.keyboards import (
    get_main_menu,
    get_confirmation_keyboard,
    get_system_control_keyboard,
    get_input_control_keyboard,
    get_ai_keyboard,
    get_camera_keyboard,
    get_audio_keyboard,
    get_network_keyboard
)
from bot.ai_assistant import AIAssistant
from user_service import UserService
from websocket_server import ws_server
import pc

# Initialize AI Assistant
ai_assistant = AIAssistant()

# Pending confirmations storage
pending_confirmations = {}

@check_access
@rate_limit
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/start")

    # Register or get user
    UserService.get_or_create_user(user.id, user.username, user.first_name, user.last_name)

    welcome_text = f"""
🤖 **Бот удалённого управления ПК**

Добро пожаловать, {user.first_name}!

Этот бот позволяет удалённо управлять вашим компьютером через Telegram.

**Управление ПК:**
• /register - Зарегистрировать новый ПК
• /mypcs - Список ваших ПК
• /selectpc <id> - Выбрать активный ПК

**Быстрые команды:**
• /info - Информация о системе
• /screen - Сделать скриншот
• /camera - Фото с веб-камеры
• /ps - Запущенные процессы
• /shell <команда> - Выполнить команду
• /ai <сообщение> - AI ассистент

**Категории:**
• 💻 Управление системой
• 📁 Управление файлами
• 📸 Скриншоты и камера
• ⌨️ Управление вводом
• 🔊 Управление звуком
• 🌐 Сетевые утилиты
• 🤖 AI-ассистент

Используйте /help для полного списка команд или меню ниже.
"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

@check_access
@rate_limit
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/help")

    help_text = """
📖 **Справочник команд**

**Системные команды:**
• /info - Информация о системе (CPU, RAM, диски, аптайм)
• /shell <команда> - Выполнить команду в терминале
• /ps - Список процессов
• /kill <PID> - Завершить процесс по ID
• /shutdown - Выключить ПК (задержка 60 сек)
• /reboot - Перезагрузить ПК (задержка 60 сек)
• /abort - Отменить выключение/перезагрузку
• /lock - Заблокировать ПК
• /sleep - Перевести ПК в режим сна

**Управление файлами:**
• /ls [путь] - Список содержимого папки
• /download <путь> - Скачать файл
• /upload - Ответить на файл для загрузки
• /mkdir <путь> - Создать папку
• /rm <путь> - Удалить файл/папку
• /tree [путь] - Древо папок

**Управление экраном:**
• /screen - Сделать скриншот
• /screen_full - Скриншот всех мониторов
• /camera - Фото с веб-камеры

**Управление вводом:**
• /type <текст> - Напечатать текст
• /press <клавиши> - Нажать комбинацию клавиш
• /mousepos - Получить позицию мыши
• /click <x> <y> [кнопка] - Кликнуть по координатам
• /move <x> <y> - Переместить мышь
• /scroll <количество> - Прокрутить колёсико мыши
• /drag <x1> <y1> <x2> <y2> - Перетащить мышью

**Буфер обмена:**
• /clip_get - Получить содержимое буфера
• /clip_set <текст> - Установить содержимое буфера

**Звук:**
• /volume [0-100] - Получить/установить громкость
• /mute - Выключить звук
• /unmute - Включить звук

**Сеть:**
• /netinfo - Информация о сети
• /ping <хост> - Пинг хоста
• /wifi - Список WiFi сетей

**AI-ассистент:**
• /ai <сообщение> - Отправить сообщение AI
• /exit_ai - Выйти из режима чата с AI

**Управление ботом:**
• /log - Получить последние логи
• /auth <ключ> - Авторизовать нового пользователя
• /restart_bot - Перезапустить бота

Используйте меню для удобной навигации!
"""

    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /info command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/info")

    await update.message.reply_text("⏳ Получение информации о системе...")

    info = pc.get_system_info()

    info_text = "💻 **Информация о системе**\n\n"
    for key, value in info.items():
        info_text += f"**{key}:** {value}\n"

    await update.message.reply_text(truncate_text(info_text), parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def shell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shell command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /shell <команда>")
        return

    command = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/shell {command}")

    await update.message.reply_text(f"⏳ Выполнение: `{command}`", parse_mode=ParseMode.MARKDOWN)

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=config.SHELL_TIMEOUT
        )

        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "(Нет вывода)"

        response = f"**Команда:** `{command}`\n**Код выхода:** {result.returncode}\n\n**Вывод:**\n```\n{output}\n```"

        await update.message.reply_text(truncate_text(response), parse_mode=ParseMode.MARKDOWN)

    except subprocess.TimeoutExpired:
        await update.message.reply_text(f"❌ Превышено время ожидания ({config.SHELL_TIMEOUT} сек)")
    except Exception as e:
        logger.error(f"Shell command failed: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

@check_access
@rate_limit
async def ps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ps command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/ps")

    await update.message.reply_text("⏳ Получение списка процессов...")

    result = pc.get_process_list()
    await update.message.reply_text(f"```\n{result}\n```", parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def kill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kill command"""
    user = update.effective_user

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /kill <PID>")
        return

    pid = int(context.args[0])
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/kill {pid}")

    result = pc.kill_process(pid)
    await update.message.reply_text(result)

@check_access
@rate_limit
async def shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shutdown command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/shutdown")

    # Request confirmation
    pending_confirmations[user.id] = "shutdown"

    await update.message.reply_text(
        "⚠️ **Выключить ПК?**\n\nКомпьютер будет выключен через 60 секунд.",
        reply_markup=get_confirmation_keyboard("shutdown"),
        parse_mode=ParseMode.MARKDOWN
    )

@check_access
@rate_limit
async def reboot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reboot command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/reboot")

    # Request confirmation
    pending_confirmations[user.id] = "reboot"

    await update.message.reply_text(
        "⚠️ **Перезагрузить ПК?**\n\nКомпьютер будет перезагружен через 60 секунд.",
        reply_markup=get_confirmation_keyboard("reboot"),
        parse_mode=ParseMode.MARKDOWN
    )

@check_access
@rate_limit
async def abort_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /abort command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/abort")

    result = pc.abort_shutdown()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lock command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/lock")

    result = pc.lock_pc()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def sleep_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sleep command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/sleep")

    result = pc.sleep_pc()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def screen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /screen command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/screen")

    await update.message.reply_text("📸 Создание скриншота...")

    success, message, img_bytes = pc.take_screenshot()

    if success:
        await update.message.reply_photo(photo=img_bytes, caption=message)
    else:
        await update.message.reply_text(message)

@check_access
@rate_limit
async def screen_full_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /screen_full command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/screen_full")

    await update.message.reply_text("📸 Создание скриншота всех мониторов...")

    success, message, img_bytes = pc.take_screenshot_all_monitors()

    if success:
        await update.message.reply_photo(photo=img_bytes, caption=message)
    else:
        await update.message.reply_text(message)

@check_access
@rate_limit
async def ls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ls command"""
    user = update.effective_user

    path = " ".join(context.args) if context.args else None
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/ls {path or ''}")

    result, items = pc.list_directory(path)
    await update.message.reply_text(f"```\n{result}\n```", parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /download command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /download <путь_к_файлу>")
        return

    file_path = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/download {file_path}")

    success, message, path = pc.download_file(file_path)

    if success:
        await update.message.reply_text(message)
        try:
            await update.message.reply_document(document=open(path, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"❌ Не удалось отправить файл: {str(e)}")
    else:
        await update.message.reply_text(message)

@check_access
@rate_limit
async def upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads"""
    user = update.effective_user

    if not update.message.document:
        return

    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/upload {update.message.document.file_name}")

    await update.message.reply_text("⏳ Загрузка файла...")

    try:
        file = await context.bot.get_file(update.message.document.file_id)
        file_path = config.TEMP_DIR / update.message.document.file_name

        await file.download_to_drive(file_path)

        result = pc.upload_file(file_path)
        await update.message.reply_text(result)

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        await update.message.reply_text(f"❌ Загрузка не удалась: {str(e)}")

@check_access
@rate_limit
async def type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /type command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /type <текст>")
        return

    text = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/type {text[:50]}...")

    result = pc.type_text(text)
    await update.message.reply_text(result)

@check_access
@rate_limit
async def press_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /press command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /press <комбинация_клавиш>")
        return

    keys = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/press {keys}")

    result = pc.press_keys(keys)
    await update.message.reply_text(result)

@check_access
@rate_limit
async def mousepos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mousepos command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/mousepos")

    result = pc.get_mouse_position()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def click_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /click command"""
    user = update.effective_user

    if len(context.args) < 2:
        await update.message.reply_text("❌ Использование: /click <x> <y> [left/right/middle]")
        return

    try:
        x = int(context.args[0])
        y = int(context.args[1])
        button = context.args[2] if len(context.args) > 2 else 'left'

        await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/click {x} {y} {button}")

        result = pc.click_mouse(x, y, button)
        await update.message.reply_text(result)

    except ValueError:
        await update.message.reply_text("❌ Неверные координаты")

@check_access
@rate_limit
async def clip_get_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clip_get command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/clip_get")

    result = pc.get_clipboard()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def clip_set_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clip_set command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /clip_set <текст>")
        return

    text = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/clip_set {text[:50]}...")

    result = pc.set_clipboard(text)
    await update.message.reply_text(result)

@check_access
@rate_limit
async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ai command"""
    user = update.effective_user

    if not context.args:
        # Start AI session
        result = ai_assistant.start_session(user.id)
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
        return

    message = " ".join(context.args)
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/ai {message[:50]}...")

    # Start session if not active
    if not ai_assistant.is_active(user.id):
        ai_assistant.start_session(user.id)

    await update.message.reply_text("🤖 Обработка...")

    response, action = await ai_assistant.process_message(user.id, message)

    # If action found, execute it WITHOUT showing JSON to user
    if action:
        action_type = action.get('action')
        params = action.get('params', {})

        try:
            # Handle multiple commands
            if action_type == 'multiple':
                commands = params.get('commands', [])
                await update.message.reply_text(f"⚙️ Выполняю {len(commands)} действий...")

                for cmd in commands:
                    cmd_type = cmd.get('action')
                    cmd_params = cmd.get('params', {})

                    # Execute each command
                    await asyncio.sleep(0.5)  # Small delay between commands

                    if cmd_type == 'shell':
                        subprocess.run(cmd_params.get('command', ''), shell=True)
                    elif cmd_type == 'type':
                        pc.type_text(cmd_params.get('text', ''))
                    elif cmd_type == 'press':
                        pc.press_keys(cmd_params.get('keys', ''))
                    elif cmd_type == 'click':
                        pc.click_mouse(cmd_params.get('x', 0), cmd_params.get('y', 0), cmd_params.get('button', 'left'))

                await update.message.reply_text("✅ Все действия выполнены!")

            elif action_type == 'shell':
                cmd = params.get('command', '')
                await update.message.reply_text(f"⚙️ Выполняю команду...")

                try:
                    # Execute command with proper encoding
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        encoding='utf-8',
                        errors='ignore'  # Ignore encoding errors
                    )

                    output = result.stdout if result.stdout else result.stderr

                    # Clean output from special characters
                    if output:
                        output = output.strip()
                        # Remove ANSI escape codes
                        import re
                        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                        output = ansi_escape.sub('', output)

                    if output and len(output) > 10:
                        await update.message.reply_text(f"✅ Готово!\n```\n{output[:1000]}\n```", parse_mode=ParseMode.MARKDOWN)
                    else:
                        await update.message.reply_text("✅ Команда выполнена!")

                except subprocess.TimeoutExpired:
                    await update.message.reply_text("⏱️ Команда выполняется слишком долго")
                except Exception as e:
                    await update.message.reply_text(f"✅ Команда запущена (фоновый режим)")

            elif action_type == 'screen':
                await update.message.reply_text("📸 Делаю скриншот...")
                success, msg, img_bytes = pc.take_screenshot()
                if success:
                    await update.message.reply_photo(photo=img_bytes, caption="✅ Скриншот готов")
                else:
                    await update.message.reply_text(msg)

            elif action_type == 'camera':
                await update.message.reply_text("📷 Захват с камеры...")
                success, msg, img_bytes = pc.take_photo()
                if success:
                    await update.message.reply_photo(photo=img_bytes, caption="✅ Фото готово")
                else:
                    await update.message.reply_text(msg)

            elif action_type == 'info':
                await update.message.reply_text("💻 Получаю информацию...")
                info = pc.get_system_info()
                info_text = "💻 **Информация о системе**\n\n"
                for key, value in info.items():
                    info_text += f"**{key}:** {value}\n"
                await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)

            elif action_type == 'type':
                text = params.get('text', '')
                await update.message.reply_text(f"⌨️ Печатаю текст...")
                result = pc.type_text(text)
                await update.message.reply_text(result)

            elif action_type == 'press':
                keys = params.get('keys', '')
                await update.message.reply_text(f"⌨️ Нажимаю клавиши...")
                result = pc.press_keys(keys)
                await update.message.reply_text(result)

            elif action_type == 'click':
                x = params.get('x', 0)
                y = params.get('y', 0)
                button = params.get('button', 'left')
                await update.message.reply_text(f"🖱️ Кликаю...")
                result = pc.click_mouse(x, y, button)
                await update.message.reply_text(result)

            elif action_type == 'volume':
                level = params.get('level', 50)
                result = pc.set_volume(level)
                await update.message.reply_text(result)

            elif action_type == 'mute':
                result = pc.mute()
                await update.message.reply_text(result)

        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка выполнения: {str(e)}")

    else:
        # No action found, send AI text response
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def exit_ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /exit_ai command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/exit_ai")

    result = ai_assistant.end_session(user.id)
    await update.message.reply_text(result)

@check_access
@rate_limit
async def log_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /log command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/log")

    logs = get_recent_logs(50)
    await update.message.reply_text(f"```\n{logs}\n```", parse_mode=ParseMode.MARKDOWN)

@check_access
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()

    data = query.data

    # Confirmation callbacks
    if data.startswith("confirm_"):
        action = data.replace("confirm_", "")

        if action == "shutdown":
            result = pc.shutdown_pc()
            await query.edit_message_text(result)
        elif action == "reboot":
            result = pc.reboot_pc()
            await query.edit_message_text(result)

    elif data.startswith("cancel_"):
        await query.edit_message_text("❌ Действие отменено")

    # Menu callbacks
    elif data == "menu_main":
        await query.edit_message_text("🏠 Главное меню", reply_markup=get_main_menu())

    elif data == "menu_info":
        info = pc.get_system_info()
        info_text = "💻 **Информация о системе**\n\n"
        for key, value in info.items():
            info_text += f"**{key}:** {value}\n"
        await query.edit_message_text(info_text, parse_mode=ParseMode.MARKDOWN)

    elif data == "menu_system":
        await query.edit_message_text("⚙️ Управление системой", reply_markup=get_system_control_keyboard())

    elif data == "sys_lock":
        result = pc.lock_pc()
        await query.edit_message_text(result)

    elif data == "sys_sleep":
        result = pc.sleep_pc()
        await query.edit_message_text(result)

    elif data == "sys_shutdown_confirm":
        await query.edit_message_text(
            "⚠️ **Выключить ПК?**\n\nКомпьютер будет выключен через 60 секунд.",
            reply_markup=get_confirmation_keyboard("shutdown"),
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "sys_reboot_confirm":
        await query.edit_message_text(
            "⚠️ **Перезагрузить ПК?**\n\nКомпьютер будет перезагружен через 60 секунд.",
            reply_markup=get_confirmation_keyboard("reboot"),
            parse_mode=ParseMode.MARKDOWN
        )

    # Camera callbacks
    elif data == "menu_camera":
        from bot.keyboards import get_camera_keyboard
        await query.edit_message_text("📷 Управление камерой", reply_markup=get_camera_keyboard())

    elif data == "camera_photo":
        await query.edit_message_text("📸 Захват изображения...")
        success, message, img_bytes = pc.take_photo()
        if success:
            await query.message.reply_photo(photo=img_bytes, caption=message)
        else:
            await query.edit_message_text(message)

    elif data == "camera_list":
        result = pc.list_cameras()
        await query.edit_message_text(result, parse_mode=ParseMode.MARKDOWN)

    # Audio callbacks
    elif data == "menu_audio":
        from bot.keyboards import get_audio_keyboard
        await query.edit_message_text("🔊 Управление звуком", reply_markup=get_audio_keyboard())

    elif data == "audio_volume":
        result = pc.get_volume()
        await query.edit_message_text(result)

    elif data == "audio_mute":
        result = pc.mute()
        await query.edit_message_text(result)

    elif data == "audio_unmute":
        result = pc.unmute()
        await query.edit_message_text(result)

    elif data == "audio_up":
        result = pc.set_volume(80)
        await query.edit_message_text(result)

    elif data == "audio_down":
        result = pc.set_volume(30)
        await query.edit_message_text(result)

    # Network callbacks
    elif data == "menu_network":
        from bot.keyboards import get_network_keyboard
        await query.edit_message_text("🌐 Сетевые утилиты", reply_markup=get_network_keyboard())

    elif data == "net_info":
        result = pc.get_network_info()
        await query.edit_message_text(result)

    elif data == "net_connections":
        result = pc.get_active_connections()
        await query.edit_message_text(result)

    elif data == "net_wifi":
        await query.edit_message_text("📶 Сканирование WiFi...")
        result = pc.get_wifi_networks()
        await query.edit_message_text(result)

    # Screen callbacks
    elif data == "menu_screen":
        await query.edit_message_text("📸 Делаю скриншот...")
        success, message, img_bytes = pc.take_screenshot()
        if success:
            await query.message.reply_photo(photo=img_bytes, caption=message)
            await query.message.reply_text("✅ Скриншот готов", reply_markup=get_main_menu())
        else:
            await query.edit_message_text(message)

    # Process callbacks
    elif data == "menu_ps":
        await query.edit_message_text("🔄 Получение списка процессов...")
        result = pc.get_process_list()
        await query.edit_message_text(f"**Процессы:**\n```\n{result[:3000]}\n```", parse_mode=ParseMode.MARKDOWN)

    # Clipboard callbacks
    elif data == "menu_clip":
        result = pc.get_clipboard()
        await query.edit_message_text(f"📋 **Буфер обмена:**\n{result}", parse_mode=ParseMode.MARKDOWN)

    # AI callbacks
    elif data == "menu_ai":
        await query.edit_message_text("🤖 **AI-ассистент**\n\nИспользуйте /ai <сообщение> для общения с AI", reply_markup=get_ai_keyboard())

    elif data == "ai_start":
        result = ai_assistant.start_session(query.from_user.id)
        await query.edit_message_text(result, parse_mode=ParseMode.MARKDOWN)

    elif data == "ai_exit":
        result = ai_assistant.end_session(query.from_user.id)
        await query.edit_message_text(result)

    # Files callbacks
    elif data == "menu_files":
        result, items = pc.list_directory()
        await query.edit_message_text(f"📁 **Файлы:**\n```\n{result[:3000]}\n```", parse_mode=ParseMode.MARKDOWN)

    # Input callbacks
    elif data == "menu_input":
        await query.edit_message_text("⌨️ **Управление вводом**\n\nИспользуйте команды:\n/type <текст>\n/press <клавиши>\n/click <x> <y>", reply_markup=get_input_control_keyboard())

    elif data == "input_type":
        await query.edit_message_text("⌨️ Используйте: /type <текст>")

    elif data == "input_press":
        await query.edit_message_text("🔘 Используйте: /press <клавиши>")

    elif data == "input_mousepos":
        result = pc.get_mouse_position()
        await query.edit_message_text(result)

    elif data == "input_click":
        await query.edit_message_text("👆 Используйте: /click <x> <y>")

@check_access
@rate_limit
async def camera_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /camera command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/camera")

    await update.message.reply_text("📸 Захват изображения с веб-камеры...")

    success, message, img_bytes = pc.take_photo()

    if success:
        await update.message.reply_photo(photo=img_bytes, caption=message)
    else:
        await update.message.reply_text(message)

@check_access
@rate_limit
async def volume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /volume command"""
    user = update.effective_user

    if not context.args:
        result = pc.get_volume()
        await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/volume")
    else:
        try:
            level = int(context.args[0])
            result = pc.set_volume(level)
            await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/volume {level}")
        except ValueError:
            result = "❌ Использование: /volume [0-100]"

    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mute command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/mute")

    result = pc.mute()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unmute command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/unmute")

    result = pc.unmute()
    await update.message.reply_text(result)

@check_access
@rate_limit
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    user = update.effective_user

    if not context.args:
        await update.message.reply_text("❌ Использование: /ping <хост>")
        return

    host = context.args[0]
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/ping {host}")

    await update.message.reply_text(f"🌐 Пинг {host}...")

    result = pc.ping(host)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def netinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /netinfo command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/netinfo")

    await update.message.reply_text("📡 Получение информации о сети...")

    result = pc.get_network_info()
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def wifi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /wifi command"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/wifi")

    await update.message.reply_text("📶 Сканирование WiFi сетей...")

    result = pc.get_wifi_networks()
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

@check_access
@rate_limit
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /register command - generate token for new PC"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/register")

    # Get PC name from args
    pc_name = " ".join(context.args) if context.args else None

    try:
        token = UserService.generate_pc_token(user.id, pc_name)

        register_text = f"""
✅ **ПК успешно зарегистрирован!**

🔑 **Ваш токен:**
`{token}`

**Инструкция по установке:**

1. Скачайте клиент: [GitHub Release]
2. Установите зависимости: `pip install -r requirements.txt`
3. Создайте файл `.env` со следующим содержимым:

```
WS_SERVER_URL={config.WS_SERVER_URL or 'ws://localhost:8765'}
PC_CLIENT_TOKEN={token}
```

4. Запустите клиент: `python pc_client.py`

**Важно:** Сохраните токен в безопасном месте!

После запуска клиента используйте /mypcs для просмотра ваших ПК.
"""

        await update.message.reply_text(register_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f"Error registering PC: {e}")
        await update.message.reply_text(f"❌ Ошибка регистрации: {str(e)}")

@check_access
@rate_limit
async def mypcs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mypcs command - list user's PCs"""
    user = update.effective_user
    await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, "/mypcs")

    try:
        pcs = UserService.get_user_pcs(user.id)
        active_pc = UserService.get_active_pc(user.id)

        if not pcs:
            await update.message.reply_text(
                "📭 У вас пока нет зарегистрированных ПК.\n\n"
                "Используйте /register для регистрации нового ПК."
            )
            return

        pcs_text = "💻 **Ваши ПК:**\n\n"

        for pc in pcs:
            status = "🟢 Онлайн" if pc.is_online else "🔴 Оффлайн"
            active = " ⭐ **АКТИВНЫЙ**" if active_pc and active_pc.id == pc.id else ""
            name = pc.pc_name or pc.hostname or f"ПК #{pc.id}"

            pcs_text += f"{status} **{name}**{active}\n"
            pcs_text += f"   ID: `{pc.id}`\n"
            pcs_text += f"   ОС: {pc.os_name or 'N/A'}\n"
            pcs_text += f"   IP: {pc.ip_address or 'N/A'}\n"

            if pc.last_heartbeat:
                pcs_text += f"   Последняя активность: {pc.last_heartbeat.strftime('%Y-%m-%d %H:%M')}\n"

            pcs_text += "\n"

        pcs_text += "\n**Команды:**\n"
        pcs_text += "• /selectpc <id> - Выбрать активный ПК\n"
        pcs_text += "• /renamepc <id> <name> - Переименовать ПК\n"
        pcs_text += "• /deletepc <id> - Удалить ПК"

        await update.message.reply_text(pcs_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f"Error listing PCs: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

@check_access
@rate_limit
async def selectpc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /selectpc command - select active PC"""
    user = update.effective_user

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /selectpc <id>\n\nИспользуйте /mypcs для просмотра списка ПК.")
        return

    pc_id = int(context.args[0])

    try:
        if UserService.set_active_pc(user.id, pc_id):
            await update.message.reply_text(f"✅ ПК #{pc_id} выбран как активный")
            await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/selectpc {pc_id}")
        else:
            await update.message.reply_text("❌ ПК не найден или не принадлежит вам")

    except Exception as e:
        logger.error(f"Error selecting PC: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

@check_access
@rate_limit
async def renamepc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /renamepc command - rename PC"""
    user = update.effective_user

    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /renamepc <id> <новое_имя>")
        return

    pc_id = int(context.args[0])
    new_name = " ".join(context.args[1:])

    try:
        if UserService.rename_pc(user.id, pc_id, new_name):
            await update.message.reply_text(f"✅ ПК #{pc_id} переименован в '{new_name}'")
            await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/renamepc {pc_id} {new_name}")
        else:
            await update.message.reply_text("❌ ПК не найден или не принадлежит вам")

    except Exception as e:
        logger.error(f"Error renaming PC: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

@check_access
@rate_limit
async def deletepc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deletepc command - delete PC"""
    user = update.effective_user

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /deletepc <id>")
        return

    pc_id = int(context.args[0])

    try:
        if UserService.delete_pc(user.id, pc_id):
            await update.message.reply_text(f"✅ ПК #{pc_id} удален")
            await asyncio.get_event_loop().run_in_executor(None, log_command, user.id, user.username, f"/deletepc {pc_id}")
        else:
            await update.message.reply_text("❌ ПК не найден или не принадлежит вам")

    except Exception as e:
        logger.error(f"Error deleting PC: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def setup_handlers(application: Application):
    """Setup all command handlers"""

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # PC management commands
    application.add_handler(CommandHandler("register", register_command))
    application.add_handler(CommandHandler("mypcs", mypcs_command))
    application.add_handler(CommandHandler("selectpc", selectpc_command))
    application.add_handler(CommandHandler("renamepc", renamepc_command))
    application.add_handler(CommandHandler("deletepc", deletepc_command))

    # System commands
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("shell", shell_command))
    application.add_handler(CommandHandler("ps", ps_command))
    application.add_handler(CommandHandler("kill", kill_command))
    application.add_handler(CommandHandler("shutdown", shutdown_command))
    application.add_handler(CommandHandler("reboot", reboot_command))
    application.add_handler(CommandHandler("abort", abort_command))
    application.add_handler(CommandHandler("lock", lock_command))
    application.add_handler(CommandHandler("sleep", sleep_command))
    application.add_handler(CommandHandler("screen", screen_command))
    application.add_handler(CommandHandler("screen_full", screen_full_command))
    application.add_handler(CommandHandler("ls", ls_command))
    application.add_handler(CommandHandler("download", download_command))
    application.add_handler(CommandHandler("type", type_command))
    application.add_handler(CommandHandler("press", press_command))
    application.add_handler(CommandHandler("mousepos", mousepos_command))
    application.add_handler(CommandHandler("click", click_command))
    application.add_handler(CommandHandler("clip_get", clip_get_command))
    application.add_handler(CommandHandler("clip_set", clip_set_command))
    application.add_handler(CommandHandler("ai", ai_command))
    application.add_handler(CommandHandler("exit_ai", exit_ai_command))
    application.add_handler(CommandHandler("log", log_command_handler))

    # New commands
    application.add_handler(CommandHandler("camera", camera_command))
    application.add_handler(CommandHandler("volume", volume_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("netinfo", netinfo_command))
    application.add_handler(CommandHandler("wifi", wifi_command))

    # Message handlers
    application.add_handler(MessageHandler(filters.Document.ALL, upload_handler))

    # Callback handler
    application.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("All handlers registered")
