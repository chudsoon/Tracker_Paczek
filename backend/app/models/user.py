from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import  relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    trackings = relationship("Tracking", back_populates="user")
    
    