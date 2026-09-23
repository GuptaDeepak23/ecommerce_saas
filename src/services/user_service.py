from sqlalchemy.orm import Session
from fastapi import HTTPException 

from src.models.user import User
from src.schemas.user import userRequest, userLogin
from src.utils.security import hash_password, verify_password, create_access_token

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_email_Phone(db: Session, email: str, phone: str):
    return db.query(User).filter(User.email == email, User.phone == phone).first()

def create_user(db: Session, request: userRequest):
    user_exist = db.query(User).filter((User.email == request.email) | (User.phone == request.phone)).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")

    user = User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password=hash_password(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_login(db: Session, user: userLogin):
    user_exist = get_user_by_email(db, user.email)

    if not user_exist:
        raise HTTPException(status_code=400, detail="User not found. Please register")
    if not verify_password(user.password, user_exist.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({
        "sub": str(user_exist.id),
        "email": user_exist.email
    })

    return {"message" : "Login Successfull" ,"token": token}