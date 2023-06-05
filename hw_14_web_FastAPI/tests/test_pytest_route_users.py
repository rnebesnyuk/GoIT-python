from unittest.mock import MagicMock, patch, AsyncMock, mock_open
import pytest
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, User
from src.schemas import UserResponse
from src.routes.users import router
from src.services.auth import auth_service
from main import app


@pytest.fixture()
def test_token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    current_user.role = "admin"
    session.commit()
    response = client.post(
        "/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def mock_update_avatar_user():
    # Provide the path to the test avatar file
    with patch('src.repository.users.update_avatar') as mock_update_avatar:
        yield mock_update_avatar


def test_read_users_me(client, test_token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        # Authenticate the user by setting the "Authorization" header
        headers = {"Authorization": f"Bearer {test_token}"}

        # Send a GET request to /users/me/ endpoint
        response = client.get("/users/me/", headers=headers)

        # Assert the response status code and data
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"


def test_update_avatar_user(client, test_token, user, session, monkeypatch, mock_update_avatar_user):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        # Authenticate the user by setting the "Authorization" header
        headers = {"Authorization": f"Bearer {test_token}"}

        # Create a test file
        test_file = ("test_avatar.jpg", b"dummy content")

        mock_update_avatar_user.return_value = {
            "username": "testuser",
            "avatar": "https://example.com/avatar.jpg",
        }

        # Send a PATCH request to /users/avatar endpoint with the test file
        response = client.patch("/users/avatar", headers=headers, files={"file": test_file})

        # Assert the response status code and data
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
        assert response.json()["avatar"] == "https://example.com/test_avatar.jpg"
