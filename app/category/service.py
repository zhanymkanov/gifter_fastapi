from typing import Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .models import Category, CategoryCreate, CategoryRead, CategoryUpdate


def get(db: Session, category_id: Any) -> Optional[CategoryRead]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_slug(db: Session, slug: str) -> Optional[CategoryRead]:
    return db.query(Category).filter(Category.slug == slug).first()


def get_all(db: Session) -> Optional[CategoryRead]:
    return db.query(Category).filter(Category.is_active).all()


def create(db: Session, *, category_in: CategoryCreate) -> Category:
    category = Category(**category_in.dict())
    db.add(category)
    db.commit()
    return category


def update(db: Session, *, category: Category, category_in: CategoryUpdate) -> Category:
    category_data = jsonable_encoder(category)
    update_data = category_in.dict(exclude_unset=True)

    for field in category_data:
        if field in update_data:
            setattr(category, field, update_data[field])

    db.add(category)
    db.commit()
    return category


def remove(db: Session, *, category_id: int) -> Category:
    category: Category = db.query(Category).get(category_id)
    category.is_active = False

    db.add(category)
    db.commit()
    return category
