from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import TEST_DATABASE_URI
from app.database import Base
from app.main import app

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
