from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str  # required
    content: str  # required
    published: bool = True  # optional (default is True)
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True