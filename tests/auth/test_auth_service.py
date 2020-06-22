from sqlalchemy.orm import Session

from app.auth import security, service
from app.auth.models import UserRegister, UserLogin
from tests.utils import random_lower_string


def test_user_create(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    user = service.create(db=db, user_in=user_in)

    assert user.id
    assert user.email == user_email
    assert security.verify_password(user_password, user.password)


def test_user_get(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    user = service.create(db=db, user_in=user_in)

    user_stored = service.get(db=db, user_id=user.id)
    assert user_stored.id
    assert user_stored.email == user_email
    assert security.verify_password(user_password, user_stored.password)


def test_user_get_by_email(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)

    service.create(db=db, user_in=user_in)
    user_stored = service.get_by_email(db=db, email=user_email)
    assert user_stored.id
    assert user_stored.email == user_email
    assert security.verify_password(user_password, user_stored.password)


def test_authenticate(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    service.create(db=db, user_in=user_in)

    user_in = UserLogin(email=user_email, password=user_password)
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert logged_in


def test_authenticate_not_exists(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    service.create(db=db, user_in=user_in)

    user_in = UserLogin(email="RANDOM_USER@404.me", password=user_password)
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert not logged_in


def test_authenticate_bad_credentials(db: Session):
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)
    service.create(db=db, user_in=user_in)

    user_in = UserLogin(email=user_email, password="HACK_YOU")
    logged_in = service.authenticate(db=db, user_in=user_in)
    assert not logged_in
