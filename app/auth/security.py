from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.config import JWT_ALG, JWT_EXP, JWT_SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = None):
    expires_delta = expires_delta or timedelta(minutes=JWT_EXP)
    expire = datetime.utcnow() + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password):
    return pwd_context.hash(plain_password)
