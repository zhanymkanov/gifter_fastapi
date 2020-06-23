from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth import users
from app.auth.models import User, UserRegister
from app.config import TEST_DATABASE_URI
from app.database import Base
from app.main import app
from tests.utils import random_lower_string

engine = create_engine(TEST_DATABASE_URI)
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user(db: Session) -> User:
    user_email = f"{random_lower_string()}@mail.net"
    user_password = random_lower_string()
    user_in = UserRegister(email=user_email, password=user_password)

    user = users.create(db=db, user_in=user_in)
    return user
