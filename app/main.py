from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.database import Base, engine
from app.product.category.router import router as category_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(category_router, prefix="/categories")
