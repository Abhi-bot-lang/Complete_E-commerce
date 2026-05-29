from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.store_model import Store
from app.models.product_model import Product
from app.models.user_model import User
from app.schemas.store_schemas import StoreCreate, StoreUpdate
import uuid





def create_store(
    store: StoreCreate,
    user_id: int,
    db: Session
):
    existing_store = db.query(Store).filter(
        Store.userId == user_id
    ).first()

    if existing_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Store already exists"
        )

    new_store = Store(
        userId=user_id,
        storeName=store.storeName,
        description=store.description,
        isActive=True
    )

    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    return new_store


def get_all_stores(db: Session):
    return db.query(Store).all()


def get_store_by_id(
    store_id: str,
    db: Session
):
    # Directly compare string ID
    store = db.query(Store).filter(
        Store.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    return store


def update_store(
    store_id: str,
    data: StoreUpdate,
    db: Session
):
    # Directly compare string ID
    store = db.query(Store).filter(
        Store.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    if data.storeName is not None:
        store.storeName = data.storeName

    if data.description is not None:
        store.description = data.description

    if data.isActive is not None:
        store.isActive = data.isActive

    db.commit()
    db.refresh(store)

    return store


def delete_store(
    store_id: str,
    db: Session
):
    # Directly compare string ID
    store = db.query(Store).filter(
        Store.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    db.delete(store)
    db.commit()

    return {
        "message": "Store deleted successfully"
    }