import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import UUID4, EmailStr, SecretStr
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import OrmBaseModel, TimeStampMixin

if TYPE_CHECKING:
    from app.shop.models import Shop  # noqa
    from app.order.models import Order  # noqa
    from app.product.models import Review  # noqa
    from app.profile.models import Profile  # noqa


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    profiles = relationship("Profile", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")


# Pydantic Models
class UserBase(OrmBaseModel):
    email: Optional[EmailStr] = None


class UserRegister(UserBase):
    email: EmailStr
    password: SecretStr


class UserLogin(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[SecretStr] = None


# Base Properties for models stored in DB
class UserInDBBase(UserBase):
    id: UUID4
    email: EmailStr


# Returned to Client
class UserResponse(UserInDBBase):
    pass


# Stored in DB
class UserInDB(UserInDBBase):
    password: SecretStr
