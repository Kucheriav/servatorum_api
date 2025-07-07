import jwt
from datetime import datetime, timedelta
from app.config import settings

ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = 60
USER_ACCESS_TOKEN_EXPIRE_MINUTES = 15


def generate_user_access_token(user_id: int, expires_minutes=USER_ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
    return token

def generate_admin_access_token(admin_id: int, expires_minutes=ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = {
        "admin_id": admin_id,
        "exp": datetime.now() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
    return token


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.get_salt(), algorithms=["HS256"])
    return payload