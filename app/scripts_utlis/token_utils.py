import uuid
from datetime import datetime, timedelta

LIMIT = 30
def generate_refresh_token():
    return str(uuid.uuid4())

def get_refresh_token_expiry(days=LIMIT):
    return datetime.now() + timedelta(days=days)