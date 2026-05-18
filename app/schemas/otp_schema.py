from pydantic import BaseModel

class OTPSchema(BaseModel):
 Id:int
 User_Id:int
 OTP:int
 Status:str
