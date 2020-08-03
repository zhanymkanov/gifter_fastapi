from starlette.config import Config

config = Config(".env")

JWT_EXP: int = 60 * 24 * 93  # 93 days while debug
JWT_ALG: str = config("ALGORITHM")
JWT_SECRET: str = config("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")
