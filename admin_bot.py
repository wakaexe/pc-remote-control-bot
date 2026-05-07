"""
Admin Bot for PC Remote Control System
Manages users, monitors system, views statistics
"""
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode
from sqlalchemy import func
from database import SessionLocal, User, PCClient, Command
from utils.logger import logger
import config

# Admin configuration
ADMIN_BOT_TOKEN = "8740193873:AAEYa2Q4LT2bU-9sJvxPWTmhTfAnzPa5umQ"
ADMIN_IDS = [config.ADMIN_ID]  # List of admin Telegram IDs

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа к этому боту")
        return

    welcome_text = """🔐 Админ-панель PC Remote Bot

Добро пожаловать в панель управления!

Доступные команды:
• /stats - Общая статистика системы
• /users - Список всех пользователей
• /pcs - Список всех подключенных ПК
• /user ID - Информация о пользователе
• /ban ID - Заблокировать пользователя
• /unban ID - Разблокировать пользователя

Используйте кнопки ниже для быстрого доступа."""

    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("💻 ПК клиенты", callback_data="admin_pcs")]
    ]

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show system statistics"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    db = SessionLocal()
    try:
        # Get statistics
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        banned_users = db.query(User).filter(User.is_banned == True).count()

        total_pcs = db.query(PCClient).count()
        online_pcs = db.query(PCClient).filter(PCClient.is_online == True).count()

        # Commands statistics
        total_commands = db.query(Command).count()
        today_commands = db.query(Command).filter(
            Command.executed_at >= datetime.utcnow().date()
        ).count()

        # Recent registrations (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_users = db.query(User).filter(User.created_at >= week_ago).count()

        stats_text = f"""📊 Статистика системы

Пользователи:
• Всего: {total_users}
• Активных: {active_users}
• Заблокированных: {banned_users}
• Новых за неделю: {new_users}

ПК клиенты:
• Всего зарегистрировано: {total_pcs}
• Онлайн сейчас: {online_pcs}
• Оффлайн: {total_pcs - online_pcs}

Команды:
• Всего выполнено: {total_commands}
• Сегодня: {today_commands}

Система:
• Время работы: активна
• Статус: ✅ Работает нормально
"""

        keyboard = [[InlineKeyboardButton("🔄 Обновить", callback_data="admin_stats")]]

        await update.message.reply_text(
            stats_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all users"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).limit(20).all()

        if not users:
            await update.message.reply_text("📭 Пользователей пока нет")
            return

        users_text = "👥 Список пользователей (последние 20):\n\n"

        for u in users:
            status = "🟢" if u.is_active and not u.is_banned else "🔴"
            banned = " [БАН]" if u.is_banned else ""
            pc_count = db.query(PCClient).filter(PCClient.user_id == u.telegram_id).count()

            users_text += f"{status} {u.telegram_id} - @{u.username or 'нет'}{banned}\n"
            users_text += f"   ПК: {pc_count} | Регистрация: {u.created_at.strftime('%Y-%m-%d')}\n\n"

        await update.message.reply_text(users_text, )

    except Exception as e:
        logger.error(f"Error listing users: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def pcs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all PC clients"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    db = SessionLocal()
    try:
        pcs = db.query(PCClient).order_by(PCClient.last_heartbeat.desc()).limit(20).all()

        if not pcs:
            await update.message.reply_text("📭 ПК клиентов пока нет")
            return

        pcs_text = "💻 Список ПК клиентов (последние 20):\n\n"

        for pc in pcs:
            status = "🟢 Онлайн" if pc.is_online else "🔴 Оффлайн"
            last_seen = pc.last_heartbeat.strftime('%Y-%m-%d %H:%M') if pc.last_heartbeat else "никогда"

            pcs_text += f"{status} {pc.pc_name or pc.hostname}\n"
            pcs_text += f"   Пользователь: {pc.user_id}\n"
            pcs_text += f"   ОС: {pc.os_name} {pc.os_version}\n"
            pcs_text += f"   IP: {pc.ip_address}\n"
            pcs_text += f"   Последняя активность: {last_seen}\n\n"

        await update.message.reply_text(pcs_text, )

    except Exception as e:
        logger.error(f"Error listing PCs: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def user_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get detailed user info"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /user <telegram_id>")
        return

    telegram_id = int(context.args[0])

    db = SessionLocal()
    try:
        target_user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not target_user:
            await update.message.reply_text("❌ Пользователь не найден")
            return

        # Get user's PCs
        pcs = db.query(PCClient).filter(PCClient.user_id == telegram_id).all()

        # Get command statistics
        total_commands = db.query(Command).filter(Command.user_id == telegram_id).count()
        recent_commands = db.query(Command).filter(
            Command.user_id == telegram_id,
            Command.executed_at >= datetime.utcnow() - timedelta(days=7)
        ).count()

        info_text = f"""
👤 Информация о пользователе

Основное:
• ID: {target_user.telegram_id}
• Username: @{target_user.username or 'нет'}
• Имя: {target_user.first_name or 'нет'} {target_user.last_name or ''}
• Статус: {'✅ Активен' if target_user.is_active else '❌ Неактивен'}
• Бан: {'🔴 Да' if target_user.is_banned else '🟢 Нет'}

ПК клиенты: {len(pcs)}
"""

        for pc in pcs:
            status = "🟢" if pc.is_online else "🔴"
            info_text += f"\n{status} {pc.pc_name or pc.hostname} ({pc.os_name})"

        info_text += f"""

Активность:
• Всего команд: {total_commands}
• За последнюю неделю: {recent_commands}
• Регистрация: {target_user.created_at.strftime('%Y-%m-%d %H:%M')}
"""

        keyboard = [
            [
                InlineKeyboardButton("🚫 Забанить" if not target_user.is_banned else "✅ Разбанить",
                                   callback_data=f"admin_ban_{telegram_id}")
            ]
        ]

        await update.message.reply_text(
            info_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            
        )

    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /ban <telegram_id>")
        return

    telegram_id = int(context.args[0])

    db = SessionLocal()
    try:
        target_user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not target_user:
            await update.message.reply_text("❌ Пользователь не найден")
            return

        target_user.is_banned = True
        target_user.is_active = False
        db.commit()

        await update.message.reply_text(f"✅ Пользователь {telegram_id} заблокирован")
        logger.info(f"Admin {user.id} banned user {telegram_id}")

    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user"""
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ У вас нет доступа")
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Использование: /unban <telegram_id>")
        return

    telegram_id = int(context.args[0])

    db = SessionLocal()
    try:
        target_user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not target_user:
            await update.message.reply_text("❌ Пользователь не найден")
            return

        target_user.is_banned = False
        target_user.is_active = True
        db.commit()

        await update.message.reply_text(f"✅ Пользователь {telegram_id} разблокирован")
        logger.info(f"Admin {user.id} unbanned user {telegram_id}")

    except Exception as e:
        logger.error(f"Error unbanning user: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    if not is_admin(user.id):
        await query.edit_message_text("❌ У вас нет доступа")
        return

    data = query.data

    if data == "admin_stats":
        # Recreate stats message
        db = SessionLocal()
        try:
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            banned_users = db.query(User).filter(User.is_banned == True).count()
            total_pcs = db.query(PCClient).count()
            online_pcs = db.query(PCClient).filter(PCClient.is_online == True).count()
            total_commands = db.query(Command).count()
            today_commands = db.query(Command).filter(
                Command.executed_at >= datetime.utcnow().date()
            ).count()
            week_ago = datetime.utcnow() - timedelta(days=7)
            new_users = db.query(User).filter(User.created_at >= week_ago).count()

            stats_text = f"""
📊 Статистика системы

Пользователи:
• Всего: {total_users}
• Активных: {active_users}
• Заблокированных: {banned_users}
• Новых за неделю: {new_users}

ПК клиенты:
• Всего зарегистрировано: {total_pcs}
• Онлайн сейчас: {online_pcs}
• Оффлайн: {total_pcs - online_pcs}

Команды:
• Всего выполнено: {total_commands}
• Сегодня: {today_commands}

Система:
• Время работы: активна
• Статус: ✅ Работает нормально

Обновлено: {datetime.now().strftime('%H:%M:%S')}
"""

            keyboard = [[InlineKeyboardButton("🔄 Обновить", callback_data="admin_stats")]]
            await query.edit_message_text(stats_text, reply_markup=InlineKeyboardMarkup(keyboard), )
        finally:
            db.close()

    elif data.startswith("admin_ban_"):
        telegram_id = int(data.split("_")[2])
        db = SessionLocal()
        try:
            target_user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if target_user:
                target_user.is_banned = not target_user.is_banned
                target_user.is_active = not target_user.is_banned
                db.commit()
                status = "заблокирован" if target_user.is_banned else "разблокирован"
                await query.edit_message_text(f"✅ Пользователь {telegram_id} {status}")
        finally:
            db.close()

def main():
    """Start admin bot"""
    logger.info("Starting Admin Bot...")

    application = Application.builder().token(ADMIN_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("users", users_command))
    application.add_handler(CommandHandler("pcs", pcs_command))
    application.add_handler(CommandHandler("user", user_info_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Admin Bot started successfully")
    application.run_polling()

if __name__ == "__main__":
    main()

    print("✅ Admin Bot started successfully")

    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
