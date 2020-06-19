from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, event


class TimeStampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _updated_at(mapper, connection, target) -> None:
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls) -> None:
        event.listen(cls, "before_update", cls._updated_at)


class ActivatedMixin:
    is_active = Column(Boolean, default=True)


# Pydantic models
class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
