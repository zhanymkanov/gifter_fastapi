import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin

if TYPE_CHECKING:
    from app.auth.models import Users  # noqa
    from app.product.models import Product  # noqa

OrderProducts = Table(
    "order_products",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", UUID, ForeignKey("order.id")),
    Column("product_id", UUID, ForeignKey("product.id")),
)


class OrderStatus(enum.Enum):
    NEW = "NEW"

    PROCESS_IN_PROGRESS = "PROCESS_IN_PROGRESS"
    PROCESS_OK = "PROCESS_OK"
    PROCESS_ERROR = "PROCESS_ERROR"

    CANCEL_IN_PROGRESS = "CANCEL_IN_PROGRESS"
    CANCEL_OK = "CANCEL_OK"
    CANCEL_ERROR = "CANCEL_ERROR"


class Order(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
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
    expires_at = Column(DateTime)

    user = relationship("Users", back_populates="orders", uselist=False)
    products = relationship("Product", back_populates="orders", secondary=OrderProducts)
