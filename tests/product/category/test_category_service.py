from sqlalchemy.orm import Session

from app.product.category import service
from app.product.category.models import CategoryCreate, CategoryUpdate
from tests.utils import random_lower_string


def test_category_create(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)
    category = service.create(db=db, category_in=category_in)

    assert category.id is not None
    assert category.title == title
    assert category.slug == slug
    service.remove(db=db, category_id=category.id)


def test_category_get(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)

    category = service.create(db=db, category_in=category_in)
    category_stored = service.get(db=db, category_id=category.id)

    assert category.id == category_stored.id
    assert category.slug == category_stored.slug
    service.remove(db=db, category_id=category.id)


def test_category_update(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    new_title, new_slug = random_lower_string(), random_lower_string()

    category_in = CategoryCreate(title=title, slug=slug)
    category_updated = CategoryUpdate(title=new_title, slug=new_slug)

    category = service.create(db=db, category_in=category_in)
    old_updated_at = category.updated_at

    service.update(db=db, category=category, category_in=category_updated)
    new_updated_at = category.updated_at

    assert category.title == new_title
    assert category.slug == new_slug
    assert new_updated_at > old_updated_at
    service.remove(db=db, category_id=category.id)


def test_category_remove(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)

    category = service.create(db=db, category_in=category_in)
    category_removed = service.remove(db=db, category_id=category.id)

    assert not category_removed.is_active
    assert category.id == category_removed.id
