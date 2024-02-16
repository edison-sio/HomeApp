# from home.services.auth import AuthService
from home.services import TaskService, AuthService, AdminService
from home.database import SessionLocal, engine
from home.models import User, Token, Task
from sqlalchemy.orm import Session
db = SessionLocal()

def init_db() -> Session:
    """Initialise database"""
    global db
    User.metadata.create_all(engine)
    Token.metadata.create_all(engine)
    Task.metadata.create_all(engine)

    return db

if __name__ == "__main__":
    db = init_db()
    adminservice = AdminService(db)
    authservice = AuthService(db)
    taskservice = TaskService(db)
    
    