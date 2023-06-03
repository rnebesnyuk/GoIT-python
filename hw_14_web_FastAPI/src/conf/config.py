from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql+psycopg2://postgres:56234@localhost:5432/postgres"
    jwt_secret_key_access: str = "secret"
    jwt_secret_key_refresh: str = "secret" 
    jwt_secret_key_email: str = "secret"
    jwt_algorithm_access: str = "HS256"
    jwt_algorithm_refresh: str = "HS256"
    jwt_algorithm_email: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 456
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = "567234"
    cloudinary_name: str = "cloudinary_name"
    cloudinary_api_key: str = "api_key"
    cloudinary_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()