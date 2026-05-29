from app.models.user_model import User
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.store_schemas import StoreCreate, StoreUpdate
from app.services import store_service
from app.utils.JWT import get_current_user


from app.services.store_service import (
    create_store,
    get_all_stores,
    get_store_by_id,
    update_store,
    delete_store
)

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/")
def create_store_route(
    store: StoreCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_store(
        store=store,
        user_id=current_user.id,
        db=db
    )


@router.get("/")
def get_stores_route(
    db: Session = Depends(get_db)
):
    return get_all_stores(db)


@router.get("/{store_id}")
def get_store_route(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_store_by_id(
        store_id=store_id,
        db=db
    )


@router.put("/{store_id}")
def update_store_route(
    store_id: str,
    store: StoreUpdate,
    db: Session = Depends(get_db)
):
    return update_store(
        store_id=store_id,
        data=store,
        db=db
    )


@router.delete("/{store_id}")
def delete_store_route(
    store_id: str,
    db: Session = Depends(get_db)
):
    return delete_store(
        store_id=store_id,
        db=db
    )