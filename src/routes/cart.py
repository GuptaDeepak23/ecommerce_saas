from src.schemas.cart import create_cart , response_cart 
from src.services.cart_service import add_to_cart , delete_from_cart , list_cart , update_cart
from fastapi import APIRouter , Depends
from src.config.database import dbsession
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get('/user' , response_model=list[response_cart])
def get_user_cart(db: dbsession , user = Depends(get_current_user)):
    return list_cart(db , user.id)


@router.post('/add', response_model=response_cart)
def add_cart(req: create_cart, db: dbsession, current_user = Depends(get_current_user)):
    return add_to_cart(db, req, current_user.id)

@router.put('/update' , response_model=response_cart)
def update_cart(db:dbsession , req:update_cart , user = Depends(get_current_user)):
    return update_cart(db , req , user.id)


@router.delete('/delete/{id}')
def delete_cart(id: int, db: dbsession, user = Depends(get_current_user)):
    return delete_from_cart(db, id, user.id)