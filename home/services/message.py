from home.services.service import Service
from home.services import UserService, ChannelService
from home.models import User, Token, Channel, Message, MessageType
from home.utils.secrets import hash_password, generate_token, check_password
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import overload, List

class MessageService(Service):
    
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.user_service = UserService(db)
        self.channel_service = ChannelService(db)
    
    def send(self, user_id: int, token: str, channel_id: int, content: str, msg_type: MessageType = MessageType.TEXT) -> Message:
        """Perform a user send a message to a channel"""
        # check if the user is in the channel
        user = self.user_service.get(user_id=user_id)
        channel = self.channel_service.get(channel_id=channel_id)
        
        if user not in channel.members:
            raise Exception
        
        # send message
        msg = Message(
            channel_id=channel_id,
            sender_id=user_id,
            content=content,
            message_type=msg_type
        )
        # channel.messages.append(msg)
        self.db.add(msg)
        self.db.commit()
        
        return msg
                
    def _get_user(self, user_id: int) -> User:
        """Get a user"""
        user = self.db.query(User).filter_by(user_id=user_id).first()
        
        if user is None:
            raise Exception
        
        return user