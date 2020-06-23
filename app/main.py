from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
