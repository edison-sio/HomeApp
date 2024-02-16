from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from home.database import Base
from datetime import datetime

MEMBER_CHANNEL_ASSOCIATION = Table(
    "member_channel_association",
    Base.metadata,
    Column("member_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("channel_id", Integer, ForeignKey("channels.channel_id"), primary_key=True)
)