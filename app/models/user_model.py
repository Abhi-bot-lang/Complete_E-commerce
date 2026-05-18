from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum,DateTime
from app.models.enum import UserRole
from app.config.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    FirstName=Column(String)
    LastName=Column(String)
    Email=Column(String,unique=True)
    Password=Column(String)
    Role = Column(SQLEnum(UserRole))
    is_Active=Column(Boolean,default=False)
    is_Verified=Column(Boolean,default=False)
    Created_At=Column(DateTime,default=datetime.utcnow)
    Updated_At=Column(DateTime,default=datetime.utcnow)