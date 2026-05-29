from app.models import JWT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import User_Schema, LoginSchema
from app.models.user_model import User
from app.models.otp_model import OTP
from app.config.database import get_db
from app.utils.hash_password import hash_password, verify_password
from app.utils.JWT import create_access_token, create_refresh_token
from app.utils.otp_generator import create_otp
from app.schemas.user_schema import ForgotPasswordSchema, ResetPasswordSchema
from app.services.otp_service import send_otp_email
from datetime import datetime, timedelta
from app.utils.otp_helper import _save_otp
from app.models.enum import OtpStatus
from app.schemas.otp_schema import VerifyOTPSchema


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Register
@router.post("/register")
def register(user: User_Schema, db: Session = Depends(get_db)):
    try:
        # Check existing user
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

     



        # Create user (no OTP fields on User model)
        db_user = User(
            firstName=user.firstName,
            lastName=user.lastName,
            email=user.email,
            password=hash_password(user.password),
            role=user.role,
            isVerified=False
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Generate OTP and save in OTP table
        otp = create_otp()
        _save_otp(db, db_user.id, otp)

        # Send OTP email
        send_otp_email(user.email, str(otp))

        return {"message": "OTP sent successfully. Please verify your email."}

    except HTTPException as exc:
         raise exc
        
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Verify OTP 
@router.post("/verify-otp")
def verify_otp(data: VerifyOTPSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.isVerified:
            raise HTTPException(status_code=400, detail="User already verified")

        # Look up OTP record in OTP table
        otp_record = db.query(OTP).filter(
            OTP.userId == user.id,
            OTP.status == OtpStatus.Pending
        ).first()

        if not otp_record:
            raise HTTPException(status_code=400, detail="No active OTP found. Please request a new one.")

        # Check OTP match
        if str(otp_record.otp) != str(data.otp):
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Check expiry
        if otp_record.otpExp is None or datetime.utcnow() > otp_record.otpExp:
            otp_record.status = OtpStatus.Expired
            db.commit()
            raise HTTPException(status_code=400, detail="OTP expired")

        # Mark OTP as verified
        otp_record.status = OtpStatus.Verified
        otp_record.isUsed = True

        # Mark user as verified and active
        user.isVerified = True
        user.isActive = True

        db.commit()

        return {"message": "Email verified successfully"}
    except HTTPException as exc:
       raise exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Forgot Password 
@router.post("/forgot-password")
def forgot_password(user: ForgotPasswordSchema, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        print(db_user)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate OTP and save in OTP table
        otp = create_otp()
        _save_otp(db, db_user.id, otp)

        # Send OTP email
        send_otp_email(user.email, otp)
           
        return {"message": "OTP sent successfully to registered email"}

    except HTTPException:
        raise HTTPException
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Reset Password
@router.post("/reset-password")
def reset_password(user: ResetPasswordSchema, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # The below function is just for OTP retrivel from my database 
        otp_record = db.query(OTP).filter(
            OTP.userId == db_user.id,
            OTP.status == OtpStatus.Pending
        ).first()

        if not otp_record:
            raise HTTPException(status_code=400, detail="No active OTP found. Please request a new one.")

        # Check OTP match
        if str(otp_record.otp) != str(user.otp):
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Check expiry
        if otp_record.otpExp is None or datetime.utcnow() > otp_record.otpExp:
            otp_record.status = OtpStatus.Expired
            db.commit()
            raise HTTPException(status_code=400, detail="OTP expired")

        # Update password and mark OTP as used
        db_user.password = hash_password(user.new_password)
        otp_record.status = OtpStatus.Verified
        otp_record.isUsed = True

        db.commit()

        return {"message": "Password reset successful"}

    except HTTPException:
        print("This HTTP Exception is thrown ")
        raise HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Login
@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        #404 means the page does not exist 

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid Password")
            #401 is unauthorised that means the creditiles are wrong 

        if not db_user.isVerified:
            raise HTTPException(status_code=403, detail="Email is not verified. Please verify your email using OTP.")
            #403 is forbidden that means the user is not allowed to access this resource
        
        access_token = create_access_token({"sub": db_user.email})
        refresh_token = create_refresh_token({"sub": db_user.email})

        return {
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except HTTPException as exc:
        # Preserve original exception details
        raise exc
        # Log if desired
        raise exc
      
        raise HTTPException
    
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
