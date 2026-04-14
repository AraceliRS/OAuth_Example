from fastapi import APIRouter, HTTPException
from models import UserLogin, UserInDB
from auth import verifyPassword, createToken

router = APIRouter(prefix="/oauth")

def getDb():
    from main import db
    return db


@router.post("/token")
def sendToken(body: UserLogin):

    db = getDb()
    user = db.get(body.email)

    if not user or not verifyPassword(body.password, user.hashedPwd):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = createToken({
        "sub": user.email,
        "isAdmin": user.isAdmin,
        "name": user.name,
        "scope": "admin" if user.isAdmin else "user",
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800,
        "scope": "admin" if user.isAdmin else "user",
    }