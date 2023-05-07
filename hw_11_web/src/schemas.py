from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr
    phone_number: str
    birthdate: str
    extra_info: Optional[str] = None


class ContactResponse(ContactModel):
    id: int
    birthdate: date

    class Config:
        orm_mode = True
