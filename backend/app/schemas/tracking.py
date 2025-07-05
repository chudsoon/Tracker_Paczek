from  pydantic import BaseModel

class TrackingCreate(BaseModel):
    number: str
    carrier: str
    user_id: int
    
class TrackingOut(BaseModel):
    id: int
    number: str
    carrier: str
    
    class Config:
        orm_mode = True