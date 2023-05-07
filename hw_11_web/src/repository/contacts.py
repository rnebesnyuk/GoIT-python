from datetime import datetime, date, timedelta
from typing import List

from fastapi import Depends, Query, HTTPException, status
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def search_contacts(first_name: str, last_name: str, email: str, db: Session):
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()


async def create_contact(body: ContactModel, db: Session):
    db_contact = Contact(**body.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def read_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def read_contact(contact_id: int, db: Session):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    return db_contact


async def update_contact(
    contact_id: int, body: ContactModel, db: Session = Depends(get_db)
):
    db_contact = await read_contact(contact_id, db)
    if db_contact:
        for field, value in body:
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


async def delete_contact(contact_id: int, db: Session):
    db_contact = await read_contact(contact_id, db)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contacts_by_birthday_range(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)

    return (
        db.query(Contact)
        .filter(
            extract("month", Contact.birthdate) >= today.month,
            extract("day", Contact.birthdate) >= today.day,
            extract("month", Contact.birthdate) <= end_date.month,
            extract("day", Contact.birthdate) <= end_date.day,
        )
        .all()
    )
