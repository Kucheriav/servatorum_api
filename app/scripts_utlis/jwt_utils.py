import jwt
from datetime import datetime, timedelta
from app.config import settings

def generate_access_token(user_id: int, expires_minutes=15):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
    return token

def decode_access_token(token: str):
    payload = jwt.decode(token, settings.get_salt(), algorithms=["HS256"])
    return payload