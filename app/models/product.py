import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base, TimeStampMixin
from app.models.order import OrderProducts

if TYPE_CHECKING:
    from .shop import Shop  # noqa
    from .users import Users  # noqa
    from .order import Order  # noqa


class Category(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    slug = Column(String, unique=True)
    parent_id = Column(UUID, ForeignKey("category.id"), nullable=True)

    parent = relationship("Category", back_populates="children", uselist=False)
    children = relationship("Category", back_populates="parent", remote_side=[id])
    products = relationship("Product", back_populates="category")


class Product(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    slug = Column(String, unique=True)
    price = Column(Float)
    description = Column(Text)
    specifications = Column(JSONB)
    is_active = Column(Boolean, default=True)
    category_id = Column(UUID, ForeignKey("category.id"))
    shop_id = Column(UUID, ForeignKey("shop.id"))
    available = Column(SmallInteger)

    shop = relationship("Shop", back_populates="products", uselist=False)
    category = relationship("Category", back_populates="products", uselist=False)
    images = relationship("Image", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    orders = relationship("Order", back_populates="products", secondary=OrderProducts)


class Review(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating = Column(SmallInteger, index=True)
    plus = Column(String)
    minus = Column(String)
    comment = Column(String)
    product_id = Column(UUID, ForeignKey("product.id"))
    user_id = Column(UUID, ForeignKey("users.id"))

    product = relationship("Product", back_populates="reviews", uselist=False)
    user = relationship("Users", back_populates="reviews", uselist=False)


class Image(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    order = Column(SmallInteger)
    product_id = Column(UUID, ForeignKey("product.id"))

    product = relationship("Product", back_populates="images", uselist=False)
