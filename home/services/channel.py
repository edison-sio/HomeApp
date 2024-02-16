from home.services.service import Service
from home.models import User, Token, Channel, Message
from home.utils.secrets import hash_password, generate_token, check_password
from sqlalchemy import select, func
from typing import overload, List

class ChannelService(Service):
    
    def create(self, user_id: int, token: str, title: str) -> Channel:
        """Create a channel"""
        token_check = self.db.query(Token).filter_by(user_id=user_id).first()
        if token_check is None or token_check.token != token:
            raise Exception # TODO: Change to HTTPException
        
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user is None:
            raise Exception

        channel = Channel(
            title=title,
            created_by=user_id,
        )
        channel.members.append(user)
        self.db.add(channel)
        self.db.commit()
        
        return channel
    
    @overload
    def get(self) -> List[Channel]: ...
    
    @overload
    def get(self, channel_id: int) -> Channel: ...
    
    def get(self, channel_id: int | None = None) -> Channel | List[Channel]:
        """Get channels depends on the given arguments"""
        if channel_id is None:
            return self.db.query(Channel).all()
        
        channel = self.db.query(Channel).filter_by(channel_id=channel_id).first()
        if channel is None:
            raise Exception
        return channel
    
    def invite(self, user_id: int, token: str, channel_id: int, to_invite: int) -> None:
        """Invite a user into a channel"""
        if not self._check_authentication(user_id, token):
            raise Exception
        
        member = self._get_user(user_id)
        to_invite_member = self._get_user(to_invite)
        channel = self.get(channel_id=channel_id)
        if member not in channel.members:
            raise Exception
        channel.members.append(to_invite_member)
        self.db.commit()
    
    def kick(self, user_id: int, token: str, channel_id: int, to_kick: int) -> None:
        """Kick a user from a channel"""
        if not self._check_authentication(user_id, token):
            raise Exception
        
        member = self._get_user(user_id=user_id)
        channel = self.get(channel_id=channel_id)
        # Only the creator of the channel can kick member
        if channel.created_by != member.user_id:
            raise Exception
        kickee = self._get_user(user_id=to_kick)
        # The kickee is not a member of the channel
        if kickee not in channel.members:
            raise Exception
        
        channel.members.remove(kickee)
        self.db.commit()
        
        
    
    def _is_user_active(self, user_id: int) -> bool:
        """Check if the user active"""
        session = self.db.query(Token).filter_by(user_id=user_id).first()
        
        return session is not None

    def _check_authentication(self, user_id: int, token: str) -> bool:
        """Check authentication"""
        session = self.db.query(Token).filter_by(user_id=user_id, token=token).first()
        
        return session is not None
    
    def _get_user(self, user_id: int) -> User:
        """Get a user by user_id"""
        user = self.db.query(User).filter_by(user_id=user_id).first()
        
        if user is None:
            raise Exception
        
        return user