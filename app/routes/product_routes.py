from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductCreate,ProductUpdate
from app.config.database import get_db
from app.models.product_model import Product
from app.services.product_service import get_all_products, get_product_by_id, create_product,delete_product,update_product
# pyrefly: ignore [missing-import]
from app.services



router = APIRouter()
# Get All Products
@router.post("/products")
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    
    return create_product(
        product=product,
        user_id=current_user.id,
        db=db
    )
@router.get("/products")
def get_products_route(
    db: Session = Depends(get_db)
):
    return get_all_products(db)



@router.get("/products/{product_id}")
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    return get_product_by_id(
        product_id=product_id,
        db=db
    )
@router.put("/products/{product_id}")
def update_product_route(
    product_id: str,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_product(
        product_id=product_id,
        data=product,
        user_id=current_user.id,
        db=db
    )

@router.delete("/products/{product_id}")
def delete_product_route(
    product_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return delete_product(
        product_id=product_id,
        user_id=current_user.id,
        db=db
    )


