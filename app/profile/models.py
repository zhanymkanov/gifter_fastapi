from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import TimeStampMixin

if TYPE_CHECKING:
    from app.auth.models import User  # noqa
    from app.order.models import Order  # noqa
    from app.product.models import Review  # noqa
    from app.shop.models import Shop  # noqa


class Profile(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    city = Column(String)
    address = Column(String)
    user_id = Column(UUID, ForeignKey("users.id"))

    user = relationship("User", back_populates="profiles", uselist=False)
