from fastapi import APIRouter, Depends
from src.config.database import dbsession
from src.schemas.product import create_productP, update_product, response_product
from src.services.product_service import create_pro, get_all_pro , update_pro
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)

@router.post("/create", response_model=response_product, dependencies=[Depends(get_current_user)])
def create_P(db: dbsession, request: create_productP):
    return create_pro(db, request)

@router.get("/get_all", response_model=list[response_product] , dependencies=[Depends(get_current_user)])
def get_all_P(db: dbsession):
    return get_all_pro(db)

@router.put("/update/{id}" , response_model=response_product , dependencies=[Depends(get_current_user)])
def update_P(db:dbsession , id:int , request : update_product):
    return update_pro(db , id , request)
    