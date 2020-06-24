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


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update(category_in: CategoryUpdate, db: Session = Depends(get_db)):
    pass


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
