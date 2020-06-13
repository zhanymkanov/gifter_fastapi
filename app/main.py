from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(engine)

app = FastAPI()
