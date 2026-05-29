from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services import categories_services
from app.schemas.categories import CategoryCreate, CategoryUpdateSchema



router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return categories_services.get_all_categories(db)

@router.get("/categories/{category_id}")
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db)
):
    return categories_services.get_category_by_id(category_id, db)

@router.post("/categories", status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return categories_services.create_category(category, db)

@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category: CategoryUpdateSchema,
    db: Session = Depends(get_db)
):
    return categories_services.update_category(category_id, category, db)

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return categories_services.delete_category(category_id, db)
