from pydantic import BaseModel, EmailStr
from app.models.enum import  UserRole

class User_Schema(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    role: UserRole

class LoginSchema(BaseModel):
   email: str
   password: str

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp:str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

