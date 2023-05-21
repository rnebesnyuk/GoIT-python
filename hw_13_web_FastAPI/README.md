The simple Contacts FastAPI app.

Added in this version:

- email confirmation of the new created user
- possibility to request a new confirmation email
- possibility to reset password via email
- possibility to add avatar to the user profile (service on Cloudinary)
- current user is cached after authorization for 15 min

You need the .env file with environment variables to work with the app. Please create the file with the following variables and insert your values:

# Database PostgreSQL
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DOMAIN=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=

# JWT authentication
JWT_SECRET_KEY_ACCESS=
JWT_SECRET_KEY_REFRESH=
JWT_SECRET_KEY_EMAIL=
JWT_ALGORITHM_ACCESS=
JWT_ALGORITHM_REFRESH=
JWT_ALGORITHM_EMAIL=

# Email service
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

# Redis
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=


# Cloudinary Storage
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=


App start:

uvicorn main:app --reload

The app gives you the possibility to:

- signup/login(JWT based) in the app
- create/read/update/delete contacts only after authorization
- user can see or change only own contacts in DB
- admin user can read/update/delete contacts of any users (delete option available only for admins)


