from typing import Any, Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    title: str
    slug: str


class CategoryUpdate(CategoryBase):
    pass


# Base Properties for models stored in DB
class CategoryInDBBase(CategoryBase):
    id: Any
    title: str
    slug: str

    class Config:
        orm_mode = True


# Returned to Client
class Category(CategoryInDBBase):
    pass


# Stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
