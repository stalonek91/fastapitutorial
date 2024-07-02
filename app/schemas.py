from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):

    title: str
    content: str
    published: Optional[bool] = True
    created: Optional[datetime] = Field(default_factory=datetime.now)


    class Config:
        orm_mode = True

class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]

class PostResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True
    


class User(BaseModel):

    id: Optional[int]
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class User_create(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True

class User_return(BaseModel):
    id: int
    email: EmailStr
    created: datetime
    
    class Config:
        orm_mode = True


class User_login(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True