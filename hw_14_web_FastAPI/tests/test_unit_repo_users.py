import unittest
from datetime import date
from typing import List
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.repository.users import (
    get_user_by_email, 
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
    password_reset,
)

from src.schemas import UserModel, UserResponse
from src.database.models import User


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = MagicMock(Session)

    def tearDown(self):
        self.db.reset_mock()

    async def test_get_user_by_email(self):
        # Arrange
        email = "test@example.com"
        db_user = User(id=1, username="testuser", email=email)

        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = db_user

        # Act
        result = await get_user_by_email(email, self.db)

        # Assert
        self.assertEqual(result, db_user)

    async def test_create_user(self):
        # Arrange
        user = UserModel(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

        # Mock the Gravatar class and its methods
        with patch("src.repository.users.Gravatar") as mock_gravatar:
            mock_gravatar.return_value.get_image.return_value = "avatar_image"

            # Act
            result = await create_user(user, self.db)

            # Assert
            self.assertEqual(result.username, user.username)

            # Verify that the database session was committed
            self.db.commit.assert_called_once()


    async def test_update_token(self):
        # Arrange
        user = User(id=1, username="testuser", email="test@example.com")
        token = "refresh_token"

        # Act
        await update_token(user, token, self.db)

        # Assert
        self.assertEqual(user.refresh_token, token)
        self.db.commit.assert_called_once()


    async def test_confirmed_email(self):
        # Arrange
        email = "test@example.com"
        user = User(id=1, username="testuser", email=email, confirmed=True)

        # Mock the get_user_by_email function
        get_user_by_email = MagicMock()
        get_user_by_email.return_value = user

        # Act
        await confirmed_email(email, self.db)

        # Assert
        self.assertTrue(user.confirmed)
        self.db.commit.assert_called_once()


    async def test_update_avatar(self):
        # Arrange
        email = "test@example.com"
        url = "https://example.com/avatar.jpg"
        user = User()


        with patch("src.repository.users.get_user_by_email") as mock_get_user_by_email:
            mock_get_user_by_email.return_value = user
            # Act
            result = await update_avatar(email, url, self.db)

        # Assert
        self.assertEqual(result, user)
        self.assertEqual(user.avatar, url)
        self.db.commit.assert_called_once()


    async def test_password_reset(self):
        # Arrange
        email = "test@example.com"
        new_password = "newpassword"
        user = User(id=1, username="testuser", email=email,)

        # Mock the get_user_by_email function
        with patch("src.repository.users.get_user_by_email") as mock_get_user_by_email:
            mock_get_user_by_email.return_value = user
            # Act
            await password_reset(email, new_password, self.db)

        # Assert
        self.assertEqual(user.password, new_password)
        self.db.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()