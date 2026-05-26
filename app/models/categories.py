from sqlalchemy import Column, Integer, String,BigInteger
from app.config.database import Base
from sqlalchemy.orm import relationship
import time 

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    createdAt = Column(BigInteger,default=lambda: int(time.time() * 1000))

    updatedAt = Column(BigInteger,default=lambda: int(time.time() * 1000),onupdate=lambda: int(time.time() * 1000))

    products = relationship("Product", back_populates="category")
     




