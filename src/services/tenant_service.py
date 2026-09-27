from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.tenant import Tenant
from src.models.category import Category
from src.models.product import Product


def get_all_active_tenants(db: Session):
    return db.query(Tenant).filter(Tenant.is_active == True).all()


def get_active_tenant_by_slug(db: Session, slug: str) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.slug == slug, Tenant.is_active == True).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Store not found or inactive")
    return tenant


def get_public_categories_by_store(db: Session, slug: str):
    tenant = get_active_tenant_by_slug(db, slug)
    return db.query(Category).filter(Category.tenant_id == tenant.id).all()


def get_public_products_by_store(db: Session, slug: str):
    tenant = get_active_tenant_by_slug(db, slug)
    return db.query(Product).filter(Product.tenant_id == tenant.id).all()
