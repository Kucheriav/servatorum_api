import jwt
import uuid
from datetime import datetime, timedelta
from app.config import settings
import logging



logger = logging.getLogger("app.scripts_utils.jwt_utils")



ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES = 60
USER_ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

def generate_user_access_token(user_id: int, expires_minutes=USER_ACCESS_TOKEN_EXPIRE_MINUTES):
    logger.info(f'start gen token at {datetime.now()}')
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(minutes=expires_minutes)
    }
    logger.info(f'exp time token at {datetime.now() + timedelta(minutes=expires_minutes)}')
    token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
    return token

def generate_admin_access_token(admin_id: int, is_superadmin: bool, expires_minutes=ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = {
        "admin_id": admin_id,
        "is_superadmin": is_superadmin,
        "exp": datetime.now() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
    return token


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.get_salt(), algorithms=["HS256"])
    return payload


def generate_refresh_token():
    return str(uuid.uuid4())

def get_refresh_token_expiry(days=REFRESH_TOKEN_EXPIRE_DAYS):
    return datetime.now() + timedelta(days=days)