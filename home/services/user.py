from home.services.service import Service
from home.models import User, Token
from sqlalchemy import select

class UserService(Service):
    
    def get_all_users(self) -> list[User]:
        """Get all users"""
        all_users = self.db.query(User).all()
        return all_users
    
    def get_user(self, user_id: int) -> User:
        """Get a user by user_id"""
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user is None:
            raise Exception
        
        return user
    
    def get_active_users(self) -> list[User]:
        """Get all active users"""
        stmt = select(User).join(Token).where(User.user_id == Token.user_id)
        active_users = self.db.scalars(stmt).all()
        
        return active_users
    
    def get_inactive_users(self) -> list[User]:
        """Get all inactvie users"""
        stmt = select(User).join(Token, isouter=True).where(User.user_id != Token.user_id)
        inactive_users = self.db.scalars(stmt).all()
        
        return inactive_users
            