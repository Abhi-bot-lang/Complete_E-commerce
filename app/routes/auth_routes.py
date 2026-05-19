from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import User_Schema, LoginSchema
from app.models.user_model import User
from app.models.otp_model import OTP
from app.config.database import get_db
from app.utils.hash_password import hash_password, verify_password
from app.utils.JWT import create_access_token, create_refresh_token
from app.utils.otp_generator import create_otp
from app.schemas.user_schema import VerifyOTPSchema, ForgotPasswordSchema, ResetPasswordSchema
from app.services.otp_service import send_otp_email
from datetime import datetime, timedelta

router = APIRouter()


# ── Helper: upsert OTP record ──────────────────────────────────────────────────
def _save_otp(db: Session, user_id: int, otp: int):
    """Create or update an OTP record for the given user."""
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)
    existing = db.query(OTP).filter(OTP.UserId == user_id).first()
    if existing:
        existing.Otp = int(otp)
        existing.Status = "Pending"
        existing.OtpExp = otp_expiry
        existing.IsUsed = False
    else:
        db.add(OTP(
            UserId=user_id,
            Otp=int(otp),
            Status="Pending",
            OtpExp=otp_expiry,
            IsUsed=False
        ))
    db.commit()


# ── Register ───────────────────────────────────────────────────────────────────
@router.post("/register")
def register(user: User_Schema, db: Session = Depends(get_db)):

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

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Generate OTP and save in OTP table
    otp = create_otp()
    try:
        _save_otp(db, db_user.id, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save OTP: {str(e)}")

    # Send OTP email
    try:
        send_otp_email(user.email, str(otp))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP mail: {str(e)}")

    return {"message": "OTP sent successfully. Please verify your email."}


# ── Verify OTP ────────────────────────────────────────────────────────────────
@router.post("/verify-otp")
def verify_otp(data: VerifyOTPSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.isVerified:
        raise HTTPException(status_code=400, detail="User already verified")

    # Look up OTP record in OTP table
    otp_record = db.query(OTP).filter(
        OTP.UserId == user.id,
        OTP.Status == "Pending"
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="No active OTP found. Please request a new one.")

    # Check OTP match
    if str(otp_record.Otp) != str(data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Check expiry
    if otp_record.OtpExp is None or datetime.utcnow() > otp_record.OtpExp:
        otp_record.Status = "Expired"
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    # Mark OTP as verified
    otp_record.Status = "Verified"
    otp_record.IsUsed = True

    # Mark user as verified and active
    user.isVerified = True
    user.isActive = True

    db.commit()

    return {"message": "Email verified successfully"}


# ── Forgot Password ───────────────────────────────────────────────────────────
@router.post("/forgot-password")
def forgot_password(user: ForgotPasswordSchema, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate OTP and save in OTP table
    otp = create_otp()
    try:
        _save_otp(db, db_user.id, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save OTP: {str(e)}")

    # Send OTP email
    try:
        send_otp_email(user.email, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")

    return {"message": "OTP sent successfully to registered email"}


# ── Reset Password ────────────────────────────────────────────────────────────
@router.post("/reset-password")
def reset_password(user: ResetPasswordSchema, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Look up OTP record in OTP table
    otp_record = db.query(OTP).filter(
        OTP.UserId == db_user.id,
        OTP.Status == "Pending"
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="No active OTP found. Please request a new one.")

    # Check OTP match
    if str(otp_record.Otp) != str(user.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Check expiry
    if otp_record.OtpExp is None or datetime.utcnow() > otp_record.OtpExp:
        otp_record.Status = "Expired"
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    # Update password and mark OTP as used
    db_user.password = hash_password(user.new_password)
    otp_record.Status = "Verified"
    otp_record.IsUsed = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Password reset failed: {str(e)}")

    return {"message": "Password reset successful"}


# ── Login ─────────────────────────────────────────────────────────────────────
@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):

    try:
        db_user = db.query(User).filter(User.email == user.email).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Password")

    if not db_user.isVerified:
        raise HTTPException(status_code=403, detail="Email is not verified. Please verify your email using OTP.")

    
    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }