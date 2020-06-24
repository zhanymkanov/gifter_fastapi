from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin

if TYPE_CHECKING:
    from app.product.models import Product  # noqa


class Image(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    order = Column(SmallInteger)
    product_id = Column(UUID, ForeignKey("product.id"))

    product = relationship("Product", back_populates="images", uselist=False)
