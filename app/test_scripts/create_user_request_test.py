import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User


client = TestClient(app)


def test_register_user():
    data = {"login": "test_user", "_password": "test_password", "_email": "test@mail.com", "phone": "+71234567890"}
    response = client.post("/users/create_user", json=data)
    assert response.status_code == 201
    assert response.json()["username"] == "test_user"
    user = User.get(User.username == "test_user")
    assert user is not None
    print('ok user')