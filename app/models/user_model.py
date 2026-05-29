from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum, DateTime
from app.models.enum import UserRole
from app.config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from datetime import datetime
from sqlalchemy import BigInteger
from app.models.enum import UserRole
from sqlalchemy.orm import relationship
import time 
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SQLEnum(UserRole))
    isVerified = Column(Boolean, default=False)
    isActive = Column(Boolean, default=False)
    createdAt = Column(BigInteger,default=lambda: int(time.time() * 1000))
    updatedAt = Column(BigInteger,default=lambda: int(time.time() * 1000),onupdate=lambda: int(time.time() * 1000))


    products = relationship("Product", back_populates="user")
    stores = relationship("Store", back_populates="user")