from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail, ResetPasswordModel
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email, send_reset_email

from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It also sends an confirmation email to the user.
        The function returns a UserModel object containing all of the information about that user.
    
    :param body: UserModel: Get the user's email and password
    :param background_tasks: BackgroundTasks: Add tasks to the background task queue
    :param request: Request: Get the base url of the server
    :param db: Session: Pass the database session to the repository function
    :return: A usermodel object
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The login function is used to authenticate a user.
    
    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Pass the database session to the function
    :return: A dictionary with the access_token, refresh_token and token type
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials. Please contact the administrator")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials. Please contact the administrator")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
        The function will check if the refresh token is valid and return a new access_token.
        If the refresh token is invalid, it will raise an HTTPException with status code 401 (UNAUTHORIZED).
    
    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Pass the database session to the function
    :return: A dictionary with the access_token, refresh_token and token type
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    return {"access_token": access_token, "refresh_token": token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it checks if that user exists in our database, and if they do not exist, 
        an HTTP 400 error is raised. If they do exist but their account has already been confirmed,
        then a message saying so will be returned. Otherwise (if they are found in our database 
        but have not yet confirmed their account), we call repository_users' confirmed_email function 
        with that email as its argument
    
    :param token: str: Get the token from the url
    :param db: Session: Get the database session
    :return: A message
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their email address. The function takes in a RequestEmail object, which contains the
    user's email address. It then checks if there is already a user with that email in the database, and if so, 
    sends an asynchronous task to send_email() using FastAPI's BackgroundTasks class.
    
    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add tasks to the background task queue
    :param request: Request: Get the base url of the server
    :param db: Session: Get the database session
    :return: A message
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.post('/reset_password')
async def reset_password(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    The reset_password function is used to reset a user's password.
        It takes in the email of the user and sends an email with instructions on how to reset their password.
        If there is no user with such an email, it returns a message saying so.
    
    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the application
    :param db: Session: Create a database session, which is used to query the database
    :return: A message
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user:
        background_tasks.add_task(send_reset_email, user.email, user.username, request.base_url)
        return {"message": "An email with instructions to reset your password has been sent to your email"}
    return {"message": "There is no user with such email"}  


@router.post('/reset_password_confirmation/{token}')
async def reset_password_confirmation(body:ResetPasswordModel, token: str, db: Session = Depends(get_db)):
    """
    The reset_password_confirmation function is used to reset a user's password.
        It takes in the token and body as parameters, which are then passed into the auth_service.get_email_from_token function
        to get the email of the user who requested a password reset. The repository users function is then called with that email 
        address to retrieve that user from our database, and if no such user exists an HTTPException is raised with status code 400
        (Bad Request) and detail &quot;Process error&quot;. If there was a valid request for this endpoint, we hash their new password using 
        auth service
    
    :param body:ResetPasswordModel: Get the password from the body of the request
    :param token: str: Get the email from the token
    :param db: Session: Get the database session
    :return: A message
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Process error")
    body.password = auth_service.get_password_hash(body.password)
    await repository_users.password_reset(email, body.password, db)
    return {"message": "Password was reset"}
