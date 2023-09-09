from typing import Optional, List

from fastapi import APIRouter, status, Cookie, HTTPException

from schemas.product import Product

router = APIRouter(prefix="/products", tags=["Endpoint to CRUD products."])


@router.post("", status_code=status.HTTP_200_OK, response_model=Product)
async def create_product(session_id: Optional[str] = Cookie()):
    pass


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Product])
async def get_products():
    return []
