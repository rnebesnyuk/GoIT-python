from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta


from src.database.db import get_db
from src.database.models import Contact
from src.schemas import *
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


# Create contact
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with such email already exists!",
        )
    db_contact = await repository_contacts.create_contact(body, db)
    return db_contact


# Get all contacts
@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    limit: int = Query(10, le=50), offset: int = 0, db: Session = Depends(get_db)
):
    contacts = await repository_contacts.read_contacts(limit, offset, db)
    return contacts


# Get one contact by id
@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await repository_contacts.read_contact(contact_id, db)
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
)
async def update_contact(
    contact_id: int, body: ContactModel, db: Session = Depends(get_db)
):
    db_contact = await repository_contacts.update_contact(contact_id, body, db)
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return db_contact


# Delete contact
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await repository_contacts.delete_contact(contact_id, db)
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return None


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    first_name: str = Query(None),
    last_name: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db),
):
    result = await repository_contacts.search_contacts(first_name, last_name, email, db)
    return result


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_birthday_range(db)
    return contacts
