import uuid
from datetime import datetime, timedelta

def generate_refresh_token():
    return str(uuid.uuid4())

def get_refresh_token_expiry(days=30):
    return datetime.utcnow() + timedelta(days=days)