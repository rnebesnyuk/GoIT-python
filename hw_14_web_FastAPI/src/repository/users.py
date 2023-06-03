from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.
    
    :param email: str: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.
            db (Session): The SQLAlchemy Session object used to interact with the database.
        Returns:
            User: A newly created user from the database.
    
    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Identify the user in the database
    :param token: str | None: Update the refresh_token column in the database
    :param db: Session: Update the database
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str): The URL for the new avatar image.
        db (Session, optional): A database session object to use instead of creating one locally. Defaults to None.  # noQA: E501 line too long
    
    :param email: Get the user from the database
    :param url: str: Pass in the url of the avatar
    :param db: Session: Pass the database session to the function
    :return: A user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def password_reset(email: str, new_password: str, db: Session) -> None:
    """
    The password_reset function resets a user's password.
        Args:
            email (str): The email of the user whose password is to be reset.
            new_password (str): The new password for the user.
            db (Session): A database session object used to commit changes.
    
    :param email: str: Get the user's email address from the database
    :param new_password: str: Set the new password for the user
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.password = new_password
    db.commit()