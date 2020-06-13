from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import Employee  # noqa


class Shop(Base):
    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    manager_id = Column(UUID, ForeignKey("user.id"))

    manager = relationship("Employee", back_populates="shop", uselist=False)
    employees = relationship("Employee", back_populates="shop")
