import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Тесты для create_legal_entity
def test_create_legal_entity():
    legal_entity = {
        "name": "Test Legal Entity",
        "email": "test@example.com",
        # другие поля
    }
    response = client.post("/create_legal_entity", json=legal_entity)
    assert response.status_code == 201
    assert response.json()["name"] == legal_entity["name"]
    assert response.json()["email"] == legal_entity["email"]

def test_create_legal_entity_invalid_data():
    legal_entity = {
        "name": "Test Legal Entity",
        # отсутствует обязательное поле email
    }
    response = client.post("/create_legal_entity", json=legal_entity)
    assert response.status_code == 422
    assert "Ошибка в поле 'email'" in response.json()["detail"][0]

def test_create_legal_entity_duplicate_email():
    legal_entity = {
        "name": "Test Legal Entity",
        "email": "existing@example.com",
    }
    response = client.post("/create_legal_entity", json=legal_entity)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

# Тесты для get_legal_entity
def test_get_legal_entity():
    legal_entity_id = 1
    response = client.get(f"/get_legal_entity/{legal_entity_id}")
    assert response.status_code == 200
    assert response.json()["id"] == legal_entity_id

def test_get_legal_entity_not_found():
    legal_entity_id = 999
    response = client.get(f"/get_legal_entity/{legal_entity_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Legal entity not found"

# Тесты для patch_legal_entity
def test_patch_legal_entity():
    legal_entity_id = 1
    patch_data = {
        "name": "Updated Test Legal Entity",
    }
    response = client.patch(f"/patch_legal_entity/{legal_entity_id}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["name"] == patch_data["name"]

def test_patch_legal_entity_not_found():
    legal_entity_id = 999
    patch_data = {
        "name": "Updated Test Legal Entity",
    }
    response = client.patch(f"/patch_legal_entity/{legal_entity_id}", json=patch_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Legal entity not found"

# Тесты для delete_legal_entity
def test_delete_legal_entity():
    legal_entity_id = 1
    response = client.delete(f"/delete_legal_entity/{legal_entity_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Legal entity deleted"

def test_delete_legal_entity_not_found():
    legal_entity_id = 999
    response = client.delete(f"/delete_legal_entity/{legal_entity_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Legal entity not found"
