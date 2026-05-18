from fastapi import APIRouter
from app.schemas.otp_schema import OTPSchema
from app.models.otp_model import OTP
from app.services.otp_service import send_otp_email
from app.utils.otp_generator import create_otp
from datetime import datetime,timedelta
from app.config.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.config.database import engine 

router=APIRouter()

@router.post("/otp/generate")
def generate(email:str,db:Session=Depends(get_db)):
    
    my_code=create_otp()
    stop_time=datetime.utcnow()+timedelta(minutes=5)


    new_otp_record=OTP(
          OTP=int(my_code),
          Status="Pending",
          ExpiresAt=stop_time)
     
    db.add(new_otp_record)
    db.commit()
    send_otp_email(email,my_code)
     
    return {"message":"OTP Generated Successfully"}


@router.post("/otp/validation")
def validate(user_typed_code:int,db:Session=Depends(get_db)):
    found_record=db.query(OTP).filter(
       OTP.OTP==user_typed_code,
       OTP.Status=="Pending"
 ).first()
    if not found_record:
        return {"error": "The code is wrong!"}
    if datetime.utcnow()>found_record.ExpiresAt:
        found_record.Status="Expired"
        db.commit()
        return {"error": "Too late! This code has expired."}
    
    found_record.Status="Verified"
    db.commit()
    return {"message":"Code is Correct!"}
##I need to change the otp_storage to my database ,As it was my temporary database 
@router.post("/otp/Regenerate")
def Regenerat(email:str,db:Session=Depends(get_db)):
    code = create_otp()
    stop_time=datetime.utcnow()+timedelta(minutes=5)
    new_otp_record=OTP(
          OTP=int(code),
          Status="Pending",
          ExpiresAt=stop_time)
    db.add(new_otp_record)
    db.commit()
    return {"message":"OTP Re-Generated Successfully"}
