import secrets

from starlette.config import Config

config = Config(".env")

JWT_EXP: int = 60 * 24 * 7  # 7 days
JWT_ALG: str = config("ALGORITHM")
JWT_SECRET: str = secrets.token_urlsafe(32)

SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")
TEST_DATABASE_URI = config("TEST_DATABASE_URL")
