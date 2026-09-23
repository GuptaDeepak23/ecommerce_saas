from pydantic import BaseModel , EmailStr

class userRequest(BaseModel):
    name : str
    email : EmailStr
    phone : str
    password : str

class userResponse(BaseModel):
    id : int
    name : str
    email : EmailStr

    class Config:
        from_attributes = True

class userLogin(BaseModel):
    email : EmailStr
    password : str
    
    