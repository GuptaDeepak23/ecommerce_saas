from fastapi import APIRouter
from src.config.database import dbsession
from src.schemas.tenant import TenantResponse
from src.schemas.category import response_category
from src.schemas.product import response_product
from src.services.tenant_service import (
    get_all_active_tenants,
    get_active_tenant_by_slug,
    get_public_categories_by_store,
    get_public_products_by_store
)

router = APIRouter(
    prefix="/stores",
    tags=["Public Storefront"]
)

# 1. Public list of all active stores
@router.get("", response_model=list[TenantResponse])
def get_all_stores(db: dbsession):
    return get_all_active_tenants(db)


# 2. Get specific store details by slug
@router.get("/{slug}", response_model=TenantResponse)
def get_store(slug: str, db: dbsession):
    return get_active_tenant_by_slug(db, slug)


# 3. Get categories belonging to this store
@router.get("/{slug}/categories", response_model=list[response_category])
def get_store_categories(slug: str, db: dbsession):
    return get_public_categories_by_store(db, slug)


# 4. Get products belonging to this store
@router.get("/{slug}/products", response_model=list[response_product])
def get_store_products(slug: str, db: dbsession):
    return get_public_products_by_store(db, slug)