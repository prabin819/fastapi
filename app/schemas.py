from pydantic import BaseModel

class PostBase(BaseModel):
    title: str  # required
    content: str  # required
    published: bool = True  # optional (default is True)
    
class PostCreate(PostBase):
    pass


