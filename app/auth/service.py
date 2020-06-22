from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .constants import ErrorCode
from .models import User, UserLogin, UserRegister
from .security import hash_password, verify_password


def get(db: Session, user_id: Any):
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create(*, db: Session, user_in: UserRegister) -> User:
    user = get_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    plain_password = user_in.password.get_secret_value()
    hashed_password = hash_password(plain_password)
    user = User(**user_in.dict(exclude={"password"}), password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(*, db: Session, user_in: UserLogin):
    user_db = get_by_email(db, user_in.email)
    if not user_db:
        return False

    if not verify_password(user_in.password, user_db.password):
        return False

    return True
