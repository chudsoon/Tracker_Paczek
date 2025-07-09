from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    
    
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_admin: bool
    
    
    class Config:
        orm_mode = True