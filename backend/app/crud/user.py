from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest
from fastapi import HTTPException, Depends
from app.utils.utils import hash_password, verify_password
from app.auth import get_current_user

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, 
                   full_name=user.full_name,
                   hashed_password=hash_password(user.password),
                   is_admin = False
                   )
   
   
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_users(db: Session, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Insuficient credentialas to get this data")
    return db.query(User).all()
    