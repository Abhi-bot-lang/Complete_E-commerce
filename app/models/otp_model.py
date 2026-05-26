from sqlalchemy import Column, Integer, String,Boolean, Enum as SQLAlchemyEnum, DateTime,BigInteger
from app.config.database import Base
from datetime import datetime
from app.models.enum import OtpStatus
import time

class OTP(Base):
    __tablename__="OTP"
    
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, unique=True)
    otp = Column(String(100), nullable=False)
    otpExp = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(OtpStatus), default=OtpStatus.Pending)
    isUsed = Column(Boolean, default=False)
    createdAt = Column(BigInteger,default=lambda: int(time.time() * 1000))
    updatedAt = Column(BigInteger,default=lambda: int(time.time() * 1000),onupdate=lambda: int(time.time() * 1000))


