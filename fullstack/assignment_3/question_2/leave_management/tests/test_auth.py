import pytest
from app.models.user import Role
from datetime import date, timedelta

def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": Role.EMPLOYEE.value
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user(client):
    # Register first
    client.post("/auth/register", json={
        "name": "Test User 2",
        "email": "test2@example.com",
        "password": "password123",
        "role": Role.EMPLOYEE.value
    })
    
    # Then login
    response = client.post("/auth/login", data={
        "username": "test2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login(client):
    response = client.post("/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
