from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from src.config.database import dbsession
from src.models.user import User
from src.utils.security import JWT_TYPE, SECRET_KEY
from src.models.tenant_membership import TenantMembership

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

def get_current_tenant_admin(db: dbsession, token: str = Depends(oauth2_bearer)):
    user = get_current_user(db, token)
    membership = (
        db.query(TenantMembership)
        .filter(
            TenantMembership.user_id == user.id,
            TenantMembership.role.in_(["OWNER", "ADMIN"])
        )
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Forbidden: You are not an admin of any store")
    return membership

def require_superadmin(db: dbsession, token: str = Depends(oauth2_bearer)):
    user = get_current_user(db, token)
    if not user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden: Superadmin access required")
    return user