from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime

class User(Base):
    """Define User model for creating `users` table database"""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
