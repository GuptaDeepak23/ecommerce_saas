from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from src.config.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission"
        ),
    )