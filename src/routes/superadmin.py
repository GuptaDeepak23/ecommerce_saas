from fastapi import APIRouter

from src.config.database import dbsession
from src.schemas.superadmin import CreateStoreRequest
from src.services.superadmin_tenant import create_tenant, list_tenant

from fastapi import Depends
from src.utils.auth import get_current_user



router = APIRouter(
    prefix="/superadmin",
    tags=["SuperAdmin"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/stores")
def create_store_account(request: CreateStoreRequest, db: dbsession):
    return create_tenant(db, request)

@router.get("/stores")
def get_all_store(db: dbsession):
    return list_tenant(db)
