from sqlalchemy import Column,Integer,String,Float,Boolean
from app.config.database import Base

class Product(Base):
    __tablename__="Products"
    id=Column(Integer,primary_key=True)
    Name=Column(String)
    Description=Column(String)
    Price=Column(Float)
    Quantity=Column(Integer)