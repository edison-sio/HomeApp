import jwt
from datetime import datetime, timedelta
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password"""
    password_bytes = password.encode()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_password = hashed_password_bytes.decode()
    
    return hashed_password

def check_password(password: str, hashed_password: str) -> bool:
    """Check if the password and the hashed one matched"""
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def generate_token(user_id: int) -> str:
    """Generate a JWT"""
    secret_key = "Baymax"
    payload = {
        "user_id": user_id
    }
    token = jwt.encode(payload, secret_key)
    return token