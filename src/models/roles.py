from sqlalchemy import Integer , Column , String
from src.config.database import Base

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    scope = Column(String(20), nullable=False)