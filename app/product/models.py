import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin
from app.order.models import OrderProducts

if TYPE_CHECKING:
    from app.auth.models import User  # noqa
    from app.order.models import Order  # noqa
    from app.product.category.models import Category  # noqa
    from app.product.review.models import Review  # noqa
    from app.shop.models import Shop  # noqa


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
