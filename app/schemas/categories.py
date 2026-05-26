from pydantic import BaseModel, Field,EmailStr

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Name of the category")

class CategoryUpdateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CategoryResponseSchema(BaseModel):
    id: int
    name: str



