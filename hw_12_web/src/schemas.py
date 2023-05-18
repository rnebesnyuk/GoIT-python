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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=15)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"