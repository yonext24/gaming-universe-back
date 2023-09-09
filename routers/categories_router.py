from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db.dbconfig import get_db
from schemas.category import Category
from db.utils.categories_utils import get_all_categories, get_category_hierarchy_from_db

router = APIRouter(prefix="/categories", tags=["Endpoint to get product categories"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_categories(db: Session = Depends(get_db)):
    categories = get_all_categories(db=db)

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories


@router.get(
    "/{category}", status_code=status.HTTP_200_OK, response_model=List[Category]
)
async def get_category_hierarchy(category: str, db: Session = Depends(get_db)):
    categories = get_category_hierarchy_from_db(db=db, name=category)

    return categories
