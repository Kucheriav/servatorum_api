import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.models.user_model import User
from app.database import connection


client = TestClient(app)


@connection
async def test_register_user(session):
    data = {"login": "test_user", "_password": "test_password", "_email": "test@mail.com", "phone": "+71234567890"}
    response = client.post("/users/create_user", json=data)
    assert response.status_code == 201
    assert response.json()["login"] == "test_user"
    user = await session.execute(select(User).filter(User.login == "test_user")).first()
    # user = User.get(User.login == "test_user")
    assert user is not None
    print('ok user')