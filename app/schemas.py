from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = True
    created: Optional[datetime] = Field(default_factory=datetime.now)


    class Config:
        orm_mode = True

