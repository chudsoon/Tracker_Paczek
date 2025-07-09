from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.user import UserCreate, LoginRequest, UserOut
from app.crud.user import create_user, get_users, authenticate_user
from app.models.user import User
from app.db import Base, engine
from app.utils.jwt import create_access_token
from app.auth import get_current_user





Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserOut])
def list_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_users(db, current_user)

@router.get("/by_email")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

