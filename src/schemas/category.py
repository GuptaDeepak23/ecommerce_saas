from pydantic import BaseModel


class create_category(BaseModel):
    name : str

class response_category(BaseModel):
    id : int
    name : str

    class Config:
        from_attributes = True

from typing import Optional

class update_category(BaseModel):
    name : str


class delete_category(BaseModel):
    id : int
