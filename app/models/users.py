import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .shop import Shop  # noqa
    from .order import Order  # noqa
    from .product import Review  # noqa


class Users(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    profiles = relationship("Profile", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    city = Column(String)
    address = Column(String)
    user_id = Column(UUID, ForeignKey("users.id"))

    user = relationship("Users", back_populates="profiles", uselist=False)


class Employee(Base):
    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    shop_id = Column(UUID, ForeignKey("shop.id"))
    is_manager = Column(Boolean, default=False)

    user = relationship("Users", backref="employees", uselist=False)
    shop = relationship("Shop", back_populates="employees", uselist=False)
    __table_args__ = (
        UniqueConstraint("user_id", "shop_id", name="employee_user_shop_key"),
    )
