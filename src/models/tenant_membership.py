from sqlalchemy import Column, Integer, String, ForeignKey, DateTime , UniqueConstraint
from sqlalchemy.sql import func
from src.config.database import Base


class TenantMembership(Base):
    __tablename__ = "tenant_memberships"

    id = Column(Integer,primary_key=True,index=True)

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    tenant_id = Column(Integer,ForeignKey("tenants.id"),nullable=False)

    role_id = Column(Integer,ForeignKey("roles.id"),nullable=False)
    
    created_at = Column(DateTime,server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),)