from sqlalchemy import Column, Integer, String, Float, Boolean, Enum as SQLAlchemyEnum, DateTime
from app.config.database import Base
from datetime import datetime
from app.models.enum import OtpStatus

class OTP(Base):
    __tablename__="OTP"
    
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, unique=True)
    otp = Column(String(100), nullable=False)
    otpExp = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(OtpStatus), default=OtpStatus.Pending)
    isUsed = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
