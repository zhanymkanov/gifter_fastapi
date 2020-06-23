from sqlalchemy.orm import Session

from app.auth import service, users
from app.auth.models import UserLogin, UserRegister
from tests.utils import random_lower_string


def test_authenticate(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    users.create(db=db, user_in=user_in)

    user_in = UserLogin(email=user_email, password=user_password)
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert logged_in


def test_authenticate_not_exists(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    users.create(db=db, user_in=user_in)

    user_in = UserLogin(email="RANDOM_USER@404.me", password=user_password)
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert not logged_in


def test_authenticate_bad_credentials(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    users.create(db=db, user_in=user_in)

    user_in = UserLogin(email=user_email, password="HACK_YOU")
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert not logged_in
