from pydantic import BaseModel, EmailStr,Field
from app.models.enum import  UserRole

class User_Schema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str=Field(...,min_length=4)
    role: UserRole

class LoginSchema(BaseModel):
   email: EmailStr
   password: str=Field(...,min_length=4)


class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp: str
    new_password: str



