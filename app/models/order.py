import enum
from typing import TYPE_CHECKING

from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa
    from .product import Product  # noqa

OrderProducts = Table(
    "order_products",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", UUID),
    Column("product_id", UUID),
)


class OrderStatus(enum.Enum):
    NEW = "NEW"

    PROCESS_IN_PROGRESS = "PROCESS_IN_PROGRESS"
    PROCESS_OK = "PROCESS_OK"
    PROCESS_ERROR = "PROCESS_ERROR"

    CANCEL_IN_PROGRESS = "CANCEL_IN_PROGRESS"
    CANCEL_OK = "CANCEL_OK"
    CANCEL_ERROR = "CANCEL_ERROR"


class PaymentStatus(enum.Enum):
    PENDING = 0
    PAID = 1


class Order(Base):
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    status = Column(Enum(OrderStatus, name="order_status"))
    is_paid = Column(Boolean, default=False)
    number = Column(String, unique=True)
    total = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String, index=True)
    city = Column(String)
    address = Column(String)
    email = Column(String, index=True)

    user = relationship("User", back_populates="orders", uselist=False)
    products = relationship("Product", back_populates="orders", secondary=OrderStatus)
