from unittest.mock import MagicMock, patch, AsyncMock
import pytest
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


# @pytest.fixture(scope="module")
# def avatar_file_path():
#     # Provide the path to the test avatar file
#     return "path/to/test_avatar.jpg"


def initialize_limiter():
    from fastapi_limiter import FastAPILimiter
    FastAPILimiter.init(auth_service.r)

initialize_limiter()


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



# def test_update_avatar_user(client):
#     # Authenticate the user by setting the "Authorization" header
#     headers = {"Authorization": f"Bearer {test_token}"}

#     # Create a test file
#     test_file = ("test_avatar.jpg", open("path/to/test_avatar.jpg", "rb"))

#     # Send a PATCH request to /users/avatar endpoint with the test file
#     response = client.patch("/users/avatar", headers=headers, files={"file": test_file})

#     # Assert the response status code and data
#     assert response.status_code == 200
#     assert response.json()["username"] == "testuser"
#     assert response.json()["avatar"] == "https://example.com/test_avatar.jpg"
