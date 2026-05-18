from pydantic import BaseModel
from app.models.enum import  UserRole

class User_Schema(BaseModel):
    Id: int
    FirstName: str
    LastName: str
    Email: str
    Password: str
    Role: UserRole

class LoginSchema(BaseModel):
    Email:str
    Password:str


