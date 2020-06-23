from sqlalchemy.orm import Session

from app.auth import security, users
from app.auth.models import UserRegister
from tests.utils import random_lower_string


def test_user_create(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    user = users.create(db=db, user_in=user_in)

    assert user.id
    assert user.email == user_email
    assert security.verify_password(user_password, user.password)


def test_user_get(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    user = users.create(db=db, user_in=user_in)

    user_stored = users.get(db=db, user_id=user.id)
    assert user_stored.id
    assert user_stored.email == user_email
    assert security.verify_password(user_password, user_stored.password)


def test_user_get_by_email(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)

    users.create(db=db, user_in=user_in)
    user_stored = users.get_by_email(db=db, email=user_email)  # noqa
    assert user_stored.id
    assert user_stored.email == user_email
    assert security.verify_password(user_password, user_stored.password)
