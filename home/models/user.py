from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime
from home.models.association import MEMBER_CHANNEL_ASSOCIATION

class User(Base):
    """Define User model for creating `users` table database"""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    is_admin = Column(Boolean, default=False)
    
    channels = relationship("Channel", secondary=MEMBER_CHANNEL_ASSOCIATION, back_populates="members")
