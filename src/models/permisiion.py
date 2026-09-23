from sqlalchemy import Integer , Column , String
from src.config.database import Base

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False , unique=True)
    description = Column(String(255) , nullable=True)
    