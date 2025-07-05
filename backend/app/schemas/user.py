from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    full_name: str
    
class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    
    class Config:
        orm_mode = True