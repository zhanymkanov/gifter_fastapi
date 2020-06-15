from typing import TYPE_CHECKING

from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer,
                        SmallInteger, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.order import OrderProducts

if TYPE_CHECKING:
    from .shop import Shop  # noqa
    from .user import User  # noqa
    from .order import Order  # noqa


class Category(Base):
    id = Column(UUID, primary_key=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    parent_id = Column(UUID, ForeignKey("category.id"))

    parent = relationship("Category", back_populates="children", uselist=False)
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")


class Product(Base):
    id = Column(UUID, primary_key=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    specifications = Column(JSONB)
    is_active = Column(Boolean, default=True)
    category_id = Column(UUID, ForeignKey("category.id"))
    shop_id = Column(UUID, ForeignKey("shop.id"))
    available = Column(SmallInteger)

    shop = relationship("Shop", back_populates="products", uselist=False)
    category = relationship("Category", back_populates="products", uselist=False)
    images = relationship("Shop", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    orders = relationship("Order", back_populates="products", secondary=OrderProducts)


class Review(Base):
    id = Column(UUID, primary_key=True)
    rating = Column(SmallInteger, index=True, nullable=False)
    plus = Column(String)
    minus = Column(String)
    comment = Column(String)
    product_id = Column(UUID, ForeignKey("product.id"))
    user_id = Column(UUID, ForeignKey("user.id"))

    product = relationship("Product", back_populates="reviews", uselist=False)
    user = relationship("User", back_populates="reviews", uselist=False)


class Image(Base):
    id = Column(Integer, primary_key=True)
    order = Column(SmallInteger)
    product_id = Column(UUID, ForeignKey("product.id"))

    product = relationship("Product", back_populates="images", uselist=False)
