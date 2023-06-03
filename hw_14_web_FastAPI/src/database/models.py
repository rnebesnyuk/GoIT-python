import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, func, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    user: str = 'user'


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birthdate = Column(DateTime)
    extra_info = Column(String, default="")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column("crated_at", DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
