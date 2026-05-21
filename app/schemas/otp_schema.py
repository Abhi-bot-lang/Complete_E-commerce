from pydantic import BaseModel, Field,EmailStr
from typing import Optional

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp:str


