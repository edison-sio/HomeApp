from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime, timedelta
import enum
from home.models.association import MEMBER_CHANNEL_ASSOCIATION

class Channel(Base):
    """This model creates channel for users to chat"""
    __tablename__ = "channels"
    
    channel_id = Column(Integer, primary_key=True)
    title = Column(String)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())

    members = relationship("User", secondary=MEMBER_CHANNEL_ASSOCIATION, back_populates="channels")
    messages = relationship("Message", back_populates="channel")