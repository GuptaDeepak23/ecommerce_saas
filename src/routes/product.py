from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.schemas.product import create_productP, update_product, response_product
from src.services.product_service import create_pro, get_all_pro , update_pro
from src.utils.auth import get_current_user
from src.utils.auth import get_current_tenant_admin
from src.models.tenant_membership import TenantMembership

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)

@router.post("/create", response_model=response_product)
def create_P(db: dbsession, request: create_productP , admin= Depends(get_current_tenant_admin)):
    return create_pro(db, request , admin.tenant_id)

@router.get("/get_all", response_model=list[response_product])
def get_all_P(db: dbsession , admin= Depends(get_current_tenant_admin)):
    return get_all_pro(db , admin.tenant_id)

@router.put("/update/{id}" , response_model=response_product)
def update_P(db:dbsession , id:int , request : update_product , admin= Depends(get_current_tenant_admin)):
    return update_pro(db , id , request , admin.tenant_id)
    