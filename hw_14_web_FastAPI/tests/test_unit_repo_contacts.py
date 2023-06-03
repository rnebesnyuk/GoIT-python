import unittest
from datetime import date
from typing import List
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.repository.contacts import (
    search_contacts,
    create_contact,
    read_contacts,
    read_contact,
    update_contact,
    delete_contact,
    get_contact_by_email,
    get_contacts_by_birthday_range,
)

from src.schemas import ContactModel
from src.database.models import Contact, User


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = MagicMock(Session)

    def tearDown(self):
        self.db.reset_mock()

    async def test_search_contacts_admin(self):
        # Arrange
        first_name = ""
        last_name = "John"
        email = ""
        user = User(role="admin")

        contact = Contact()

        self.db.query.return_value.filter.return_value.filter.return_value.all.return_value = (
            contact
        )

        # Act
        result = await search_contacts(first_name, last_name, email, user, self.db)

        # Assert
        self.assertEqual(result, contact)

    async def test_search_contacts_non_admin(self):
        # Arrange
        first_name = "John"
        last_name = "hhh"
        email = ""
        user = User(role="user", id=1)

        contact = Contact()
        self.db.query.return_value.filter.return_value.filter.return_value.filter.return_value.all.return_value = (
            contact
        )

        # Act
        result = await search_contacts(first_name, last_name, email, user, self.db)

        # Assert
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        # Arrange
        body = ContactModel(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="0991112233",
            birthdate="13 June 1988",
        )
        user = User(id=1)
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        # Act
        result = await create_contact(body, user, self.db)

        # Assert
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.birthdate, body.birthdate)

    async def test_read_contacts_admin(self):
        # Arrange
        limit = 10
        offset = 0
        user = User(role="admin")

        contact_list = [Contact(), Contact()]
        self.db.query().filter().limit().offset().all.return_value = contact_list

        # Act
        result = await read_contacts(limit=10, offset=0, user=user, db=self.db)

        # Assert

        self.assertEqual(result, contact_list)

    async def test_read_contact_admin(self):
        contact_id = 1
        user = User(role="admin")

        contact = Contact()
        # Mock the query method of the database session
        self.db.query().filter().first.return_value = contact

        # Act
        result = await read_contact(contact_id, user, self.db)

        # Assert
        self.assertEqual(result, contact)

    async def test_update_contact(self):
        # Arrange
        contact_id = 1
        body = ContactModel(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="0991112233",
            birthdate="13 June 1988",
        )
        user = User(id=1)

        # Mock the read_contact function
        with patch("src.repository.contacts.read_contact") as mock_read_contact:
            mock_read_contact.return_value = body

            # Act
            result = await update_contact(contact_id, body, user, self.db)

            self.assertEqual(result, body)

            # Verify that the database session was committed and refreshed
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(body)


    async def test_delete_contact(self):
        # Arrange
        contact_id = 1
        user = User(id=1)
        db_contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")

        # Mock the read_contact function
        with patch("src.repository.contacts.read_contact") as mock_read_contact:
            mock_read_contact.return_value = db_contact

            # Act
            result = await delete_contact(contact_id, user, self.db)

            # Assert
            self.assertEqual(result, db_contact)

            # Verify that the database session was committed
            self.db.commit.assert_called_once()


    async def test_get_contact_by_email(self):
        # Arrange
        email = "john.doe@example.com"
        user = User(id=1)
        db_contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")

        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.first.return_value = db_contact

        # Act
        result = await get_contact_by_email(email, user, self.db)

        # Assert
        self.assertEqual(result, db_contact)


    async def test_get_contacts_by_birthday_range(self):
        # Arrange
        user = User(id=1)
        db_contacts = [
            Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com"),
            Contact(id=2, first_name="Jane", last_name="Smith", email="jane.smith@example.com"),
        ]

        # Mock the query method of the database session
        self.db.query.return_value.filter.return_value.all.return_value = db_contacts

        # Act
        result = await get_contacts_by_birthday_range(user, self.db)

        # Assert
        self.assertEqual(result, db_contacts)

if __name__ == "__main__":
    unittest.main()
