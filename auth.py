import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from models import TokenData


#Hashing
passwordHash = PasswordHash.recommended()

def hashPassword(pwd):
    return passwordHash.hash(pwd)
    
def verifyPassword(pwd, hashedPwd):
    return passwordHash.verify(pwd, hashedPwd)


#JWT

SECRET_KEY = "supersecretkey"  # En un caso real usa .env
ALGORITHM = "HS256" 
EXPIRATION_TIME_MIN = 30


def createToken(data: dict):
    to_encode = data.copy()  #subject y isAdmin
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verifyToken(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        is_admin: bool = payload.get("isAdmin", False)
        if email is None:
            return None
        return TokenData(email=email, is_admin=is_admin)
    except InvalidTokenError:
        return None
    

    
