import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin

if TYPE_CHECKING:
    from app.auth.models import User  # noqa
    from app.product.models import Product  # noqa


class Shop(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    slug = Column(String, unique=True)
    description = Column(Text)
    manager_id = Column(UUID, ForeignKey("users.id"))

    manager = relationship("Employee", back_populates="shop", uselist=False)
    employees = relationship("Employee", back_populates="shop")
    products = relationship("Product", back_populates="shop")


class Employee(Base, TimeStampMixin):
    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    shop_id = Column(UUID, ForeignKey("shop.id"))
    is_manager = Column(Boolean, default=False)

    user = relationship("User", backref="employees", uselist=False)
    shop = relationship("Shop", back_populates="employees", uselist=False)
    __table_args__ = (
        UniqueConstraint("user_id", "shop_id", name="employee_user_shop_key"),
    )
