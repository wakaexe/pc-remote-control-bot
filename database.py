"""
Database models for multi-user system
Uses SQLAlchemy ORM with SQLite (local) or PostgreSQL (production)
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """User model - each user can have multiple PCs"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    # User status
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    # Active PC selection
    active_pc_id = Column(Integer, ForeignKey('pc_clients.id'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    pcs = relationship("PCClient", back_populates="user", foreign_keys="PCClient.user_id")

    def __repr__(self):
        return f"<User {self.telegram_id} - {self.username}>"


class Command(Base):
    """Command history for analytics"""
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False, index=True)
    pc_id = Column(Integer, ForeignKey('pc_clients.id'), nullable=True)
    command = Column(String(255), nullable=False)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    executed_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Command {self.command} by {self.user_id}>"


class PCClient(Base):
    """PC Client connections - each user can have multiple PCs"""
    __tablename__ = 'pc_clients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)

    # PC Info
    pc_name = Column(String(255))  # User-friendly name
    hostname = Column(String(255))
    os_name = Column(String(255))
    os_version = Column(String(255))
    ip_address = Column(String(50))

    # WebSocket connection
    ws_session_id = Column(String(255), unique=True, nullable=True)

    # Status
    is_online = Column(Boolean, default=False)
    last_heartbeat = Column(DateTime)

    # Timestamps
    registered_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="pcs", foreign_keys=[user_id])

    def __repr__(self):
        return f"<PCClient {self.pc_name or self.hostname} - User {self.user_id}>"


# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_database.db')

# Fix for Heroku PostgreSQL URL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(engine)
    print("Database initialized successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, let caller handle it
