from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.schemas.superadmin import CreateStoreRequest
from src.services.superadmin_tenant import create_tenant, list_tenant
from src.utils.auth import require_superadmin

router = APIRouter(
    prefix="/superadmin",
    tags=["SuperAdmin"],
    dependencies=[Depends(require_superadmin)]
)

@router.post("/stores")
def create_store_account(request: CreateStoreRequest, db: dbsession):
    return create_tenant(db, request)

@router.get("/stores")
def get_all_store(db: dbsession):
    return list_tenant(db)
