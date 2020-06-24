import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin

if TYPE_CHECKING:
    from app.auth.models import User  # noqa
    from app.product.models import Product  # noqa


class Review(Base, TimeStampMixin):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating = Column(SmallInteger, index=True)
    plus = Column(String)
    minus = Column(String)
    comment = Column(String)
    product_id = Column(UUID, ForeignKey("product.id"))
    user_id = Column(UUID, ForeignKey("users.id"))

    product = relationship("Product", back_populates="reviews", uselist=False)
    user = relationship("User", back_populates="reviews", uselist=False)
