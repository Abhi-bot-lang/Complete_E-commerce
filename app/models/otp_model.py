from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime
from app.config.database import Base
from datetime import datetime

class OTP(Base):
    __tablename__="OTP"
    
    Id = Column(Integer, primary_key=True, index=True)

    UserId = Column(Integer, unique=True)

    Otp = Column(String(100), nullable=False)

    OtpExp = Column(DateTime, nullable=False)

    Status = Column(String, default="Pending")

    IsUsed = Column(Boolean, default=False)

    CreatedAt = Column(DateTime, default=datetime.utcnow)

    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)