from sqlalchemy import Column,Integer,String,DateTime 
from app.config.database import Base 
from datetime import datetime 


class JWT(Base):
    __tablename__="JWTS"
    Id=Column(Integer,primary_key=True)
    JTI=Column(String,unique=True)
    UserId=Column(Integer)
    CreatedAt=Column(DateTime)
    UpdatedAt=Column(DateTime)
