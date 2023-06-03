from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

from fastapi_limiter.depends import RateLimiter


from src.database.db import get_db
from src.database.models import *
from src.schemas import *
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RolesAccess


router = APIRouter(prefix="/contacts", tags=["contacts"])

access_delete = RolesAccess([Role.admin])


# Create contact
@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=1, seconds=60))],
)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the contact information from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is currently logged in
    
    :return: A contactmodel object
    """
    contact = await repository_contacts.get_contact_by_email(
        body.email, current_user, db
    )
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with such email already exists!",
        )
    db_contact = await repository_contacts.create_contact(body, current_user, db)
    return db_contact


# Get all contacts
@router.get(
    "/",
    response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=3, seconds=60))],
)
async def read_contacts(
    limit: int = Query(10, le=50),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_contacts function returns a list of contacts.
        The limit and offset parameters are used to paginate the results.

    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned
    :param offset: int: Set the offset of the query
    :param db: Session: Pass the database session to the repository function
    :param current_user: User: Get the user id of the logged in user

    :return: A list of contacts
    """
    contacts = await repository_contacts.read_contacts(limit, offset, current_user, db)
    return contacts


# Get one contact by id
@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_contact function returns a contact by its id.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id from the token

    :return: A contact object
    """
    db_contact = await repository_contacts.read_contact(contact_id, current_user, db)
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return db_contact


# Update contact
@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(RateLimiter(times=2, seconds=60))],
)
async def update_contact(
    contact_id: int,
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated ContactModel object to be saved in the database.
            db (Session, optional): A SQLAlchemy Session object for interacting with a PostgreSQL database. Defaults to Depends(get_db).
            current_user (User, optional): A User object representing an authenticated user making this request. Defaults to Depends(auth_service.get_current_user).

    :param contact_id: int: Identify which contact is being updated
    :param body: ContactModel: Pass the data that will be used to update the contact
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the auth_service

    :return: A contactmodel object
    """
    db_contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return db_contact


# Delete contact
@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(access_delete)],
)
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for the user making this request. Defaults to Depends(auth_service.get_current_user).

    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database

    :return: None
    """
    db_contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return None


@router.get(
    "/search/",
    response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def search_contacts(
    first_name: str = Query(None),
    last_name: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The search_contacts function searches for contacts in the database.
        The search_contacts function takes three optional parameters: first_name, last_name, and email.
        If no parameters are provided, all contacts will be returned.

    :param first_name: str: Pass the first name of a contact to be searched for
    :param last_name: str: Search for a contact's last name
    :param email: str: Search for a contact by email
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current user

    :return: A list of contacts
    """
    result = await repository_contacts.search_contacts(
        first_name, last_name, email, current_user, db
    )
    return result


@router.get(
    "/birthdays/",
    response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=1, seconds=60))],
)
async def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.
        The function takes in the current user and database session as parameters, then calls the get_contacts_by_birthday_range function from repository/contacts.py to return a list of contacts with upcoming birthdays.

    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id from the token
    
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts_by_birthday_range(
        current_user, db
    )
    return contacts
