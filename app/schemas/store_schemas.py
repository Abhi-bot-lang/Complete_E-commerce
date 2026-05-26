from pydantic import BaseModel

class StoreResponseSchema(BaseModel):
    id: int
    name: str
    address: str

class StoreCreate(BaseModel):
    name: str
    address: str
class StoreUpdate(BaseModel):
    name: str
    address: str

