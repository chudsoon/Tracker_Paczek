from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError


SECRET_KEY = "start123"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def check_token_is_valid(token :str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, ALGORITHM)
        print("Token is valid:", decoded)
        return True
    except ExpiredSignatureError:
        print("Token expired")
        return False
    except JWTError as e:
        print("Invalid token:", e)
        return False