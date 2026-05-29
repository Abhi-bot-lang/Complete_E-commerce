from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey
from app.config.database import Base



from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import time 
import uuid

class Store(Base):
    __tablename__ = "stores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(Integer, ForeignKey("users.id"), nullable=False)

    storeName = Column(String(100),nullable=False)

    description = Column(String)

    isActive = Column(Boolean )

    createdAt = Column(BigInteger,default=lambda: int(time.time() * 1000))

    updatedAt = Column(BigInteger,default=lambda: int(time.time() * 1000),onupdate=lambda: int(time.time() * 1000))

    user = relationship(
        "User",
        back_populates="stores"
    )

    products = relationship(
        "Product",
        back_populates="store"
    )











