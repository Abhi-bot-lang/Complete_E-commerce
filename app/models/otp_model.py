from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime
from app.config.database import Base

class OTP(Base):
    __tablename__="OTP"
    id=Column(Integer,primary_key=True)
    UserId=Column(Integer,unique=True)
    OTP=Column(Integer)
    Status=Column(String,default="Pending")
    ExpiresAt=Column(DateTime)