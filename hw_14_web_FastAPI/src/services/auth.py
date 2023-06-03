import pickle
from typing import Optional

import redis
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY_ACCESS = settings.jwt_secret_key_access
    SECRET_KEY_REFRESH = settings.jwt_secret_key_refresh
    SECRET_KEY_EMAIL = settings.jwt_secret_key_email
    ALGORITHM_ACCESS = settings.jwt_algorithm_access
    ALGORITHM_REFRESH = settings.jwt_algorithm_refresh
    ALGORITHM_EMAIL = settings.jwt_algorithm_email
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise. This is used to verify that the user's login
            credentials are correct.
        
        :param self: Represent the instance of the class
        :param plain_password: Pass the password that is entered by the user
        :param hashed_password: Check if the password is correct
        :return: A boolean value
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.
        
        :param self: Represent the instance of the class
        :param password: str: Get the password from the user
        :return: A hash of the password
        """
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_access_token function creates a new access token for the user.
            
        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded in the token
        :param expires_delta: Optional[float]: Set the expiration time of the access token
        :return: A string of encoded data
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY_ACCESS, algorithm=self.ALGORITHM_ACCESS)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): The data to be encoded in the JWT. This should include at least a username and an id, but can also include other information such as roles or permissions.
                expires_delta (Optional[float]): The number of seconds until this token expires, defaults to 7 days if not specified.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass in the user's id
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A string
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY_REFRESH, algorithm=self.ALGORITHM_REFRESH)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function decodes the refresh token and returns the email of the user.
            If it fails to decode, it raises an HTTPException with a 401 status code.
        
        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to be decoded
        :return: The email of the user who has requested a new access token
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY_REFRESH, algorithms=[self.ALGORITHM_REFRESH])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be called by the FastAPI framework to retrieve the current user.
        It uses the token in the Authorization header of each request to decode it and get its payload, which contains information about
        the user. It then retrieves this user from Redis or PostgreSQL if it's not cached yet.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :param db: Session: Pass the database session to the function
        :return: A user object
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY_ACCESS, algorithms=[self.ALGORITHM_ACCESS])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user
    
    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token expires, and will no longer be valid. This is set to 3 days from now by default.
                - scope: What this JWT can be used for, in this case it's an email_token which means it can only be used for verifying emails.
        
        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded
        :return: A token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=3)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, self.SECRET_KEY_EMAIL, algorithm=self.ALGORITHM_EMAIL)
        return token
    
    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
            If the scope of the token is not 'email_token', then it raises an HTTPException.
            If there is a JWTError, then it also raises an HTTPException.
        
        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email address associated with the token
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY_EMAIL, algorithms=[self.ALGORITHM_EMAIL])
            if payload['scope'] == 'email_token':
                email = payload["sub"]
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()