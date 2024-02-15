from home.models import User, Token
from home.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session

db = SessionLocal()

def init_db() -> Session:
    """Initialise database"""
    global db
    User.metadata.create_all(engine)
    Token.metadata.create_all(engine)

    return db

def hash_password(password: str) -> str:
    return password + ":hashed"

def generate_token(user_id: int) -> str:
    return f"faketoken.{user_id}"

def create_admin() -> User:
    user_kwargs = {
        # "user_id": 0,
        "username": "admin",
        "hashed_password": hash_password("password")
    }
    admin = User(**user_kwargs)
    db.add(admin)
    db.commit()
    return admin

def create_token(user_id: int) -> Token:
    token_kwargs = {
        # "token_id": 0,
        "user_id": user_id,
        "token": generate_token(user_id)
    }
    token = Token(**token_kwargs)
    db.add(token)
    db.commit()
    return token

def is_active(user_id: int) -> bool:
    token = db.query(Token).filter(Token.user_id == user_id).first()
    if token is None:
        return False
    return True

def logout(user_id: int, token: str) -> bool:
    token = db.query(Token).filter(Token.user_id == user_id and Token.token == token).first()
    
    db.delete(token)
    db.commit()
    
    return True

def login(username: str, password: str) -> Token:
    user = db.query(User).filter(User.username == username and User.hashed_password == hash_password(password)).first()
    if user is None:
        raise Exception
    token = Token(**{
        "user_id": user.user_id,
        "token": generate_token(user.user_id)
    })
    db.add(token)
    db.commit()
    
    return token