from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.schemas.category import create_category, response_category, update_category
from src.services.category_service import create_cat, get_cat, update_cat, get_category_by_id
from src.utils.auth import get_current_user
from src.utils.auth import get_current_tenant_admin
from src.models.tenant_membership import TenantMembership

router = APIRouter(
    tags=["category"],
    prefix="/category"
)

@router.post("/create", response_model=response_category)
def create_category(request: create_category, db: dbsession , admin= Depends(get_current_tenant_admin)):
    return create_cat(db, request , admin.tenant_id)

@router.get("/get_all", response_model=list[response_category])
def get_all_category(db: dbsession   , admin= Depends(get_current_tenant_admin)):
    return get_cat(db , admin.tenant_id)

@router.put("/update/{id}", response_model=response_category)
def update_category_router(id: int, request: update_category, db: dbsession , admin= Depends(get_current_tenant_admin)):
    return update_cat(db, id, request , admin.tenant_id)

@router.get("/{id}", response_model=response_category)
def get_cat_by_id(db: dbsession, id: int , admin= Depends(get_current_tenant_admin)):
    return get_category_by_id(db, id , admin.tenant_id)