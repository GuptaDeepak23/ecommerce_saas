from pydantic import BaseModel, Field


class create_cart(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, default=1)


class response_cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class update_cart_schema(BaseModel):
    id: int
    quantity: int = Field(gt=0, default=1)


class delete_cart(BaseModel):
    id: int