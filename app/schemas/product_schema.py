from pydantic import UUID4
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    productName: str
    description: str
    price: int
    stock: int
    categoryId: int
    storeId: str

class ProductUpdate(BaseModel):
    productName:str
    description: str
    price: int
    stock: int
    categoryId:int
    storeId:UUID4
    
class ProductDelete(BaseModel):
    message: str

class ProductSearch(BaseModel):
    search: str = Field(
    min_length=1,
    max_length=100,
    description="Product search keyword"
    )
