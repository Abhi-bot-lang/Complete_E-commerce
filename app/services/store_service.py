from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.store_model import Store
from app.models.product_model import Product
from app.models.user_model import User
from app.schemas.store_schemas import StoreCreate

def get_all_stores(db: Session):
    try:
        stores = db.query(Store).all()

        if not stores:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No stores found"
            )

        return stores

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )

#
def update_store(id: int, store_data: StoreCreate, db: Session):
    store = db.query(Store).filter(Store.id == id).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    store.name = store_data.name
    store.description = store_data.description

    db.commit()
    db.refresh(store)

    return {
        "message": "Store updated successfully",
        "data": store
    }

def delete_store(id: int, db: Session):
    store = db.query(Store).filter(Store.id == id).first()

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

def get_store_products(id: int, db: Session):
    store = db.query(Store).filter(Store.id == id).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    products = db.query(Product).filter(
        Product.store_id == id
    ).all()

    return {
        "store_id": id,
        "products": products
    }

def get_user_stores(user_id: int, db: Session):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    stores = db.query(Store).filter(
        Store.user_id == user_id
    ).all()

    return {
        "user_id": user_id,
        "stores": stores
    }