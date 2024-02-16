from home.services.service import Service
from home.models import User, Token
from sqlalchemy import select
from fastapi import HTTPException
from typing import List, overload

class UserNotFoundError(HTTPException):
    pass


class UserService(Service):
    
    @overload
    def get(self) -> List[User]: ...
    
    @overload
    def get(self, user_id: int) -> User: ...
    
    @overload
    def get(self, is_active: bool) -> List[User]: ...
    
    def get(self,
        user_id: int | None = None,
        is_active: bool | None = None) -> User | List[User]:
        """Get users"""
        if user_id is None and is_active is None:
            return self._get_all_users()
        elif is_active is None:
            return self._get_user(user_id)
        elif user_id is None and is_active:
            return self._get_active_users()
        elif user_id is None and not is_active:
            return self._get_inactive_users()
        
    def _get_all_users(self) -> List[User]:
        """Get all users"""
        all_users = self.db.query(User).all()
        return all_users
    
    def _get_user(self, user_id: int) -> User:
        """Get a user by user_id"""
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user is None:
            raise UserNotFoundError(status_code=404, detail="User not found")
        
        return user
    
    def _get_active_users(self) -> List[User]:
        """Get all active users"""
        stmt = select(User).join(Token, onclause=(User.user_id == Token.user_id))
        active_users = self.db.scalars(stmt).all()
        
        return active_users
    
    def _get_inactive_users(self) -> List[User]:
        """Get all inactvie users"""
        stmt = select(User).join(Token, onclause=(User.user_id == Token.user_id), isouter=True).where(Token.user_id == None)
        inactive_users = self.db.scalars(stmt).all()
        
        return inactive_users
    
    def change_password(self, original_password: str, new_password: str) -> None:
        """Change password"""
        ...