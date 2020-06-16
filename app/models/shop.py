import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .users import Employee  # noqa


class Shop(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    slug = Column(String, unique=True)
    description = Column(Text)
    manager_id = Column(UUID, ForeignKey("users.id"))

    manager = relationship("Employee", back_populates="shop", uselist=False)
    employees = relationship("Employee", back_populates="shop")
