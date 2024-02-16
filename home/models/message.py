from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime, timedelta
import enum

class MessageType(enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(String, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)
    sent_at = Column(DateTime, default=datetime.now())
    
    channel = relationship("Channel", back_populates="messages")