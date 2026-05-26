import uuid
import time
from sqlalchemy import ( Column,String,BigInteger,ForeignKey,Integer)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))

    userId= Column(Integer, ForeignKey("users.id"), nullable=False)
    productName = Column(String(100),nullable=False)

    description = Column(String(100),nullable=True)

    price = Column(Integer,nullable=False)

    stock = Column(Integer,nullable=False,default=0)

    categoryId = Column(Integer, ForeignKey("categories.id"), nullable=False)

    storeId = Column(String,ForeignKey("stores.id"),nullable=False)


    createdAt = Column(BigInteger,default=lambda: int(time.time() * 1000))

    updatedAt = Column(BigInteger,default=lambda: int(time.time() * 1000),onupdate=lambda: int(time.time() * 1000))

    category = relationship("Category",back_populates="products")

    store = relationship("Store",back_populates="products")

    user = relationship("User",back_populates="products")



