import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import UUID4
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import ActivatedMixin, OrmBaseModel, TimeStampMixin

if TYPE_CHECKING:
    from app.product.models import Product  # noqa


class Category(Base, TimeStampMixin, ActivatedMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True)
    slug = Column(String, unique=True)
    parent_id = Column(UUID, ForeignKey("category.id"), nullable=True)

    parent = relationship("Category", back_populates="children", uselist=False)
    children = relationship("Category", back_populates="parent", remote_side=[id])
    products = relationship("Product", back_populates="category")


# Pydantic Models
class CategoryBase(OrmBaseModel):
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
    id: UUID4
    title: str
    slug: str


# Returned to Client
class CategoryResponse(CategoryInDBBase):
    pass
