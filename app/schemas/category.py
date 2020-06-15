from typing import Any, Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    title: str
    slug: str
    parent_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    title: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[str] = None


# Base Properties for models stored in DB
class CategoryInDBBase(CategoryBase):
    id: Any

    class Config:
        orm_mode = True


# Returned to Client
class Category(CategoryBase):
    pass


# Stored in DB
class CategoryInDB(CategoryBase):
    pass
