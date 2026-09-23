from src.models.tenant import Tenant
from src.models.tenant_membership import TenantMembership
from src.models.user import User
from src.models.roles import Role
from src.config.database import dbsession
from src.utils.security import hash_password



from fastapi import HTTPException

def create_tenant(db, req):

    existing_tenant = db.query(Tenant).filter(Tenant.slug == req.slug).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant with this slug already exists")

    existing_user = db.query(User).filter((User.email == req.email) | (User.phone == req.owner_phone)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")

    owner_role = db.query(Role).filter(Role.name == "OWNER", Role.scope == "TENANT").first()
    if not owner_role:
        raise HTTPException(status_code=500, detail="OWNER role not found in system")

    tenant = Tenant(
        name=req.store_name,
        slug=req.slug,
        email=req.email,
    )
    db.add(tenant)
    db.flush()

    owner = User(
        name=req.owner_name,
        email=req.email,
        phone=req.owner_phone,
        password=hash_password(req.owner_password),
    )
    db.add(owner)
    db.flush()

    tenant_membership = TenantMembership(
        tenant_id=tenant.id,
        user_id=owner.id,
        role_id=owner_role.id,
    )
    db.add(tenant_membership)
    db.commit()
    db.refresh(tenant)

    return tenant

def list_tenant(db):
    return db.query(Tenant).all()
