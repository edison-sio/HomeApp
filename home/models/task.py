from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime, timedelta
import enum

class TaskStatus(enum.Enum):
    OPEN = "open"
    CLOSE = "close"
    ACCEPTED = "accepted"
    COMPLETED = "completed"

class Task(Base):
    """This model creates an object represents a task"""
    
    __tablename__ = "tasks"
    
    task_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    reward = Column(Float, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    