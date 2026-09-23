from pydantic import BaseModel

class create_productP(BaseModel):
    name : str
    price : int
    stock : int
    category_id : int



class response_product(BaseModel):
    id : int
    name : str
    price : int
    stock : int
    category_id : int

    class Config:
        from_attributes = True

class update_product(BaseModel):
    name : str
    price : int
    stock : int
    category_id : int


class delete_product(BaseModel):
    id : int
    