from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime, timedelta

class Token(Base):
    """This model creates tokens table to handle user authentication"""
    __tablename__ = "tokens"
    
    token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    expires_at = Column(DateTime, default=datetime.now() + timedelta(hours=1))