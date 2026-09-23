from fastapi import APIRouter
from src.config.database import dbsession
from src.schemas.user import userRequest,userResponse , userLogin
from src.services.user_service import get_user_by_email_Phone , create_user ,user_login
from src.utils.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)



@router.get('/check')
def check_user(email: str,phone:str,db: dbsession):
    return get_user_by_email_Phone( db , email , phone)


@router.post("/register", response_model=userResponse)
def register(request : userRequest , db : dbsession):
    return create_user(db,request)


@router.post("/login")
def login(user : userLogin , db : dbsession):
    return user_login(db,user)

@router.get("/me", response_model=userResponse)
def me(current_user = Depends(get_current_user)):
    return current_user