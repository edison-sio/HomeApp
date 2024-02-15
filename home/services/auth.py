from home.services.service import Service
from home.models import User, Token
from home.utils.secrets import hash_password, generate_token, check_password

class AuthService(Service):
    
    def register(self, username: str, password: str) -> Token:
        """Perform register process of a user"""

        existed_user = self.db.query(User).filter_by(username=username).first()
        if existed_user is not None:
            raise Exception

        user = User(
            username=username,
            hashed_password=hash_password(password)
        )
    
        self.db.add(user)
        self.db.commit()

        token = Token(
            user_id=user.user_id,
            token=generate_token(user.user_id)
        )

        self.db.add(token)
        self.db.commit()
        
        return token
    
    def login(self, username: str, password: str) -> Token:
        """Perform login by a user"""
        user = self.db.query(User).filter_by(username=username).first()
        if user is None:
            raise Exception
        
        if not check_password(password, user.hashed_password):
            raise Exception

        token = Token(
            user_id=user.user_id,
            token=generate_token(user.user_id)
        )
        self.db.add(token)
        self.db.commit()
        
        return token
    
    def logout(self, user_id: int, token: str) -> None:
        """Perform logout by a user"""
        token = self.db.query(Token).filter_by(user_id=user_id, token=token).first()
        
        if token is None:
            raise Exception
        self.db.delete(token)
        self.db.commit()
