# from home.services.auth import AuthService
from home.services import TaskService, AuthService, AdminService, ChannelService, UserService
from home.database import SessionLocal, engine
from home.models import User, Token, Task, Channel, Message
from sqlalchemy.orm import Session
db = SessionLocal()

def init_db() -> Session:
    """Initialise database"""
    global db
    User.metadata.create_all(engine)
    Token.metadata.create_all(engine)
    Task.metadata.create_all(engine)
    Channel.metadata.create_all(engine)
    Message.metadata.create_all(engine)

    return db

if __name__ == "__main__":
    db = init_db()
    userservice = UserService(db)
    adminservice = AdminService(db)
    authservice = AuthService(db)
    taskservice = TaskService(db)
    channelservice = ChannelService(db)