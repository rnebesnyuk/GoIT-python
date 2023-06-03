from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=EmailStr(settings.mail_from),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Your Contact Book",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three arguments:
            -email: the user's email address, which is used as a unique identifier for them.
            -username: the username of the user who is trying to sign up. 
            This will be displayed in their confirmation message so they know it was sent by us 
            and not some random person trying to phish them for information. 
            It also helps make sure that we're sending this message only when someone signs up, and not at any other time

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username to the email template
    :param host: str: Pass the host name to the template

    :return: A coroutine object
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)


async def send_reset_email(email: EmailStr, username: str, host: str):
    """
    The send_reset_email function sends an email to the user with a link to reset their password.
        Args:
            email (str): The user's email address.
            username (str): The user's username.
            host (str): The hostname of the server where this function is being called from.

    :param email: EmailStr: Validate the email address
    :param username: str: Get the username of the user who requested a password reset
    :param host: str: Pass the hostname of the application to the template
    :return: A coroutine object
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Reset your password",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password_template.html")
    except ConnectionErrors as err:
        print(err)
