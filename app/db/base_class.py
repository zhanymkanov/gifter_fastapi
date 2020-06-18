from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, event
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimeStampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _updated_at(mapper, connection, target) -> None:
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls) -> None:
        event.listen(cls, "before_update", cls._updated_at)
