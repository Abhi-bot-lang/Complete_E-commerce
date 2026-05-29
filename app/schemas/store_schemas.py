from pydantic import BaseModel
from typing import Optional


class StoreCreate(BaseModel):
    storeName: str
    description: str
    user_id:int


class StoreUpdate(BaseModel):
    storeName: str
    description:str
    isActive:bool 