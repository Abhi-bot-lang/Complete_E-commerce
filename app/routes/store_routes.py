from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.store_schemas import StoreCreate, StoreUpdate
from app.services import store_service

router = APIRouter()

@router.get("/stores")
def get_all_stores(db: Session = Depends(get_db)):
    stores = store_service.get_all_stores(db)
    return {
        "success": True,
        "data": stores
    }
##
#@router.get("/stores/{id}")
#def get_store(id: int, db: Session = Depends(get_db)):
    #return store_service.get_store(id, db)

#@router.post("/stores", status_code=status.HTTP_201_CREATED)
#def create_store(store_data: StoreCreate,db: Session = Depends(get_db)):
    #return store_service.create_store(store_data, db)

#@router.put("/stores/{id}")
#def update_store(id: int,store_data: StoreCreate,db: Session = Depends(get_db)):
   # return store_service.update_store(id, store_data, db)

##@router.delete("/stores/{id}")
#def delete_store(id: int,db: Session = Depends(get_db)):
    return store_service.delete_store(id, db)

#@router.get("/stores/{id}/products")
#def get_store_products(id: int,db: Session = Depends(get_db)):
    #return store_service.get_store_products(id, db)

#@router.get("/users/{userId}/stores")
#def get_user_stores(userId: int,db: Session = Depends(get_db)):
    #return store_service.get_user_stores(userId, db)