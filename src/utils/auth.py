from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from src.config.database import dbsession
from src.models.user import User
from src.utils.security import JWT_TYPE, SECRET_KEY
from src.models.roles import Role

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(db: dbsession, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_TYPE])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        user = db.query(User).filter(User.id == int(user_id)).first()
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

