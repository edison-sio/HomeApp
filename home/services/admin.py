from home.services.service import Service
from home.models import User, Token
from home.utils.secrets import hash_password, generate_token, check_password
from home.services.user import UserNotFoundError
from fastapi import HTTPException

class UserAlreadyExistsError(HTTPException):
    pass

class AdminService(Service):
    
    def create_user(self, username: str, password: str, is_admin: bool = False) -> User:
        """Create a new user to the system"""
        # check if `username` is taken
        if self.db.query(User).filter_by(username=username).count() > 0:
            raise UserAlreadyExistsError(status_code=404, detail="Username has been used")
        user = User(
            username=username,
            hashed_password=hash_password(password),
            is_admin=is_admin
        )
        self.db.add(user)
        self.db.commit()
        return user
    
    def remove_user(self, user_id: str) -> None:
        """Remove a user from the system"""
        user = self.db.query(User).filter_by(user_id=user_id).first()
        if user is None:
            raise UserNotFoundError(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
    