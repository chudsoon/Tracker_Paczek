from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Tracking(Base):
    __tablename__ = "trackings"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    carrier = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user= relationship("User", back_populates="trackings")
    
