from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 1. Response schema for public storefront details
class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool

    class Config:
        from_attributes = True  # Allows Pydantic to read directly from SQLAlchemy models


# 2. Detailed response schema for Admin / Superadmin views
class TenantDetailResponse(TenantResponse):
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
