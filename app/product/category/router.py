from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from . import service
from .constants import ErrorCode
from .models import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter()


@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    return service.get_all_active(db)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create(category_in: CategoryCreate, db: Session = Depends(get_db)):
    if service.get_by_title(db, title=category_in.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.CATEGORY_TITLE_ALREADY_EXISTS,
        )

    if service.get_by_slug(db, slug=category_in.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.CATEGORY_SLUG_ALREADY_EXISTS,
        )

    return service.create(db, category_in=category_in)


@router.put(
    "/{category_slug}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def update(
    category_slug: str, category_in: CategoryUpdate, db: Session = Depends(get_db)
):
    category = service.get_by_slug(db, category_slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.CATEGORY_SLUG_NOT_FOUND,
        )
    return service.update(db, category=category, category_in=category_in)
