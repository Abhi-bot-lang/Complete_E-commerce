from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.otp_model import OTP
from app.models.enum import OtpStatus 

#Helper function is created that can be used in any route 
def _save_otp(db: Session, user_id: int, otp: str):
    """Create or update an OTP record for the given user."""
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)
    existing = db.query(OTP).filter(OTP.userId == user_id).first()
    if existing:
        existing.otp = otp
        existing.status = OtpStatus.Pending
        existing.otpExp = otp_expiry
        existing.isUsed = False
    else:
        db.add(OTP(
            userId=user_id,
            otp=otp,
            status=OtpStatus.Pending,
            otpExp=otp_expiry,
            isUsed=False
        ))
    db.commit()