from pydantic import BaseModel, EmailStr


class CreateStoreRequest(BaseModel):
    store_name: str
    slug: str
    email: EmailStr

    owner_name: str
    owner_phone: str
    owner_password: str

