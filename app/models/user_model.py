from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum, DateTime
from app.models.enum import UserRole
from app.config.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SQLEnum(UserRole))
    isVerified = Column(Boolean, default=False)
    isActive = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)