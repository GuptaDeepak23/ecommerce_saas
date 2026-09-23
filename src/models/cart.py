from src.config.database import Base
from sqlalchemy import Column, Integer, ForeignKey , DateTime
from sqlalchemy.sql import func

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    product_id = Column(Integer , ForeignKey("products.id") , nullable=False)
    quantity = Column(Integer , nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    