from app.crud.base import CRUDBase
from app.models.product import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

category = CRUDBase[Category, CategoryCreate, CategoryUpdate](Category)
