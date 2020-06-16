import secrets
from typing import Optional

from decouple import config
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    HASH_ALGORITHM: str = config("ALGORITHM")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = config("DATABASE_URL")
    TEST_DATABASE_URI: Optional[PostgresDsn] = config("TEST_DATABASE_URL")

    class Config:
        case_sensitive = True


settings = Settings()
