from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# -----------user----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
# -----------post/tweet----------

class PostBase(BaseModel):
    title: str  # required
    content: str  # required
    published: bool = True  # optional (default is True)
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True
        
        
class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)  # Only allows 0 or 1
    
class PostWithVotes(BaseModel):
    post: PostResponse
    noOfVotes: int