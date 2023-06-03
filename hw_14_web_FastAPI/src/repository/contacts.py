from datetime import datetime, date, timedelta
from typing import List

from fastapi import Depends, Query, HTTPException, status
from sqlalchemy import extract, and_
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import * 
from src.schemas import ContactModel


async def search_contacts(
    first_name: str, last_name: str, email: str, user: User, db: Session
):
    """
    The search_contacts function searches for contacts in the database.
    
    :param first_name: str: Filter the contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :param user: User: Check if the user is an admin or not
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    if user.role == Role.admin:
        query = db.query(Contact)
    else:
        query = db.query(Contact).filter(Contact.user_id == user.id)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        
    :param body: ContactModel: Create a new contact
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: A contact object
    """
    db_contact = Contact(**body.dict(), user=user)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def read_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The read_contacts function returns a list of contacts.
    If the user is an admin, all contacts are returned. If the user is not an admin, only their own contacts are returned.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param user: User: Check if the user is an admin or not
    :param db: Session: Pass in a database session
    :return: A list of contact objects
    """
    if user.role == Role.admin:
        contacts = (
            db.query(Contact)
            .limit(limit)
            .offset(offset)
            .all()
        )
    else:
        contacts = (
            db.query(Contact)
            .filter(Contact.user_id == user.id)
            .limit(limit)
            .offset(offset)
            .all()
        )
    return contacts


async def read_contact(contact_id: int, user: User, db: Session):
    """
    The read_contact function returns a contact from the database.
        If the user is an admin, it will return any contact in the database.
        If not, it will only return contacts that belong to that user.
    
    :param contact_id: int: Get the contact id from the database
    :param user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: A single contact
    """
    if user.role == Role.admin:
        db_contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id)
        .first()
    )
    else:
        db_contact = (
            db.query(Contact)
            .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
            .first()
        )
    return db_contact


async def update_contact(
    contact_id: int, body: ContactModel, user: User, db: Session = Depends(get_db)
):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated ContactModel object with new values for each field.
            user (User): The User object that is currently logged in and making this request.
        Returns:
            db_contact(ContactModel) or None: If successful, returns an updated ContactModel object; otherwise, returns None.
    
    :param contact_id: int: Identify the contact to update
    :param body: ContactModel: Define the type of data that is expected to be passed in
    :param user: User: Ensure that the user is authenticated
    :param db: Session: Get the database session
    :return: The updated contact
    """
    db_contact = await read_contact(contact_id, user, db)
    if db_contact:
        for field, value in body:
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


async def delete_contact(contact_id: int, user: User, db: Session):
    """
    The delete_contact function deletes a contact from the database.
    
    Args:
        contact_id (int): The id of the contact to delete.
        user (User): The user who is deleting this contact. This is used for authorization purposes, so that only contacts belonging to a particular user can be deleted by that same user. 
        db (Session): A database session object which will be used to perform the deletion operation on our SQLAlchemy ORM model objects.
    
    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Ensure that the user is authorized to delete the contact
    :param db: Session: Pass the database session to the function
    :return: The deleted contact
    """
    db_contact = await read_contact(contact_id, user, db)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


async def get_contact_by_email(email: str, user: User, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on an email address.
        Args:
            email (str): The email address of the contact to be retrieved.
            user (User): The user who is making this request.
            db (Session): A connection to the database for querying and updating data.
    
    :param email: str: Filter the database by email
    :param user: User: Get the user from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = (
        db.query(Contact)
        .filter(Contact.email == email)
        .first()
    )
    return contact


async def get_contacts_by_birthday_range(user: User, db: Session):
    """
    The get_contacts_by_birthday_range function returns a list of contacts whose birthdays fall within the next 7 days.
    
    :param user: User: Get the user's id
    :param db: Session: Pass the database session to the function
    :return: A list of contact objects
    """
    today = date.today()
    end_date = today + timedelta(days=7)

    return (
        db.query(Contact)
        .filter(
            and_(
                Contact.user_id == user.id,
                extract("month", Contact.birthdate) >= today.month,
                extract("day", Contact.birthdate) >= today.day,
                extract("month", Contact.birthdate) <= end_date.month,
                extract("day", Contact.birthdate) <= end_date.day,
            )
        )
        .all()
    )
