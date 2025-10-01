from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.utils.jwt import check_token_is_valid
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User

SECRET_KEY = "start123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
       

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Nie mozna zweryfikować poświadczeń",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
            