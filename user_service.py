"""
User service for managing PC clients and user operations
"""
import secrets
from datetime import datetime
from typing import Optional, List
from database import SessionLocal, User, PCClient, Command
from utils.logger import logger

class UserService:
    """Service for user management"""

    @staticmethod
    def get_or_create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> User:
        """Get existing user or create new one"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()

            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True,
                    is_banned=False
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"New user created: {telegram_id} - {username}")
            else:
                # Update user info if changed
                if username and user.username != username:
                    user.username = username
                if first_name and user.first_name != first_name:
                    user.first_name = first_name
                if last_name and user.last_name != last_name:
                    user.last_name = last_name
                user.updated_at = datetime.utcnow()
                db.commit()

            return user
        finally:
            db.close()

    @staticmethod
    def get_user(telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            db.close()

    @staticmethod
    def generate_pc_token(telegram_id: int, pc_name: str = None) -> str:
        """Generate unique token for PC client"""
        db = SessionLocal()
        try:
            # Generate unique token
            token = secrets.token_urlsafe(32)

            # Create PC client entry
            pc_client = PCClient(
                user_id=telegram_id,
                token=token,
                pc_name=pc_name,
                is_online=False
            )
            db.add(pc_client)
            db.commit()

            logger.info(f"PC token generated for user {telegram_id}")
            return token
        finally:
            db.close()

    @staticmethod
    def get_user_pcs(telegram_id: int) -> List[PCClient]:
        """Get all PCs for a user"""
        db = SessionLocal()
        try:
            pcs = db.query(PCClient).filter(PCClient.user_id == telegram_id).all()
            return pcs
        finally:
            db.close()

    @staticmethod
    def get_active_pc(telegram_id: int) -> Optional[PCClient]:
        """Get user's active PC"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user or not user.active_pc_id:
                return None

            pc = db.query(PCClient).filter(PCClient.id == user.active_pc_id).first()
            return pc
        finally:
            db.close()

    @staticmethod
    def set_active_pc(telegram_id: int, pc_id: int) -> bool:
        """Set active PC for user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return False

            # Verify PC belongs to user
            pc = db.query(PCClient).filter(
                PCClient.id == pc_id,
                PCClient.user_id == telegram_id
            ).first()

            if not pc:
                return False

            user.active_pc_id = pc_id
            db.commit()
            logger.info(f"User {telegram_id} set active PC to {pc_id}")
            return True
        finally:
            db.close()

    @staticmethod
    def delete_pc(telegram_id: int, pc_id: int) -> bool:
        """Delete a PC client"""
        db = SessionLocal()
        try:
            pc = db.query(PCClient).filter(
                PCClient.id == pc_id,
                PCClient.user_id == telegram_id
            ).first()

            if not pc:
                return False

            # If this was active PC, clear it
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user and user.active_pc_id == pc_id:
                user.active_pc_id = None

            db.delete(pc)
            db.commit()
            logger.info(f"PC {pc_id} deleted by user {telegram_id}")
            return True
        finally:
            db.close()

    @staticmethod
    def rename_pc(telegram_id: int, pc_id: int, new_name: str) -> bool:
        """Rename a PC client"""
        db = SessionLocal()
        try:
            pc = db.query(PCClient).filter(
                PCClient.id == pc_id,
                PCClient.user_id == telegram_id
            ).first()

            if not pc:
                return False

            pc.pc_name = new_name
            db.commit()
            logger.info(f"PC {pc_id} renamed to '{new_name}' by user {telegram_id}")
            return True
        finally:
            db.close()

    @staticmethod
    def is_user_banned(telegram_id: int) -> bool:
        """Check if user is banned"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            return user.is_banned if user else False
        finally:
            db.close()

    @staticmethod
    def log_command(telegram_id: int, command: str, pc_id: int = None, success: bool = True, error: str = None):
        """Log command execution"""
        db = SessionLocal()
        try:
            cmd = Command(
                user_id=telegram_id,
                pc_id=pc_id,
                command=command,
                success=success,
                error_message=error
            )
            db.add(cmd)
            db.commit()
        except Exception as e:
            logger.error(f"Error logging command: {e}")
        finally:
            db.close()
