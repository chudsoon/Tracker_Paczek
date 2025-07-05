from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    full_name: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    
    class Config:
        orm_mode = True