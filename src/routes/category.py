from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.schemas.category import create_category, response_category, update_category
from src.services.category_service import create_cat, get_cat, update_cat, get_category_by_id
from src.utils.auth import get_current_user

router = APIRouter(
    tags=["category"],
    prefix="/category"
)

@router.post("/create", response_model=response_category, dependencies=[Depends(get_current_user)])
def create_category(request: create_category, db: dbsession):
    return create_cat(db, request)

@router.get("/get_all", response_model=list[response_category])
def get_all_category(db: dbsession):
    return get_cat(db)

@router.put("/update/{id}", response_model=response_category, dependencies=[Depends(get_current_user)])
def update_category_router(id: int, request: update_category, db: dbsession):
    return update_cat(db, id, request)

@router.get("/{id}", response_model=response_category)
def get_cat_by_id(db: dbsession, id: int):
    return get_category_by_id(db, id)