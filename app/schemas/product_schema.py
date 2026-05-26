from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    productName: str       
    description: Optional[str] 
    price: int              
    stock: int              
    categoryId: int
    storeId: str

class ProductUpdate(BaseModel):
    productName:Optional[str] = None
    
    price: Optional[int] = None
    stock: Optional[int] = None
    categoryId: Optional[int] = None
    storeId: Optional[str] = None    

class ProductDelete(BaseModel): 
    message: str



