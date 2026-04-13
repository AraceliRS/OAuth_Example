from fastapi import APIRouter, HTTPException
from models import UserLogin, UserInDB
from auth import verify_password, create_token

router = APIRouter(prefix="/oauth")

def getDb():
    from main import db
    return db


#Valida credenciales y libera token
#Nuestro proveedor
@router.post("/token")
def sendToken(body: UserLogin):

    db = getDb()
    user = db.get(body.email)

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},  # Header estándar OAuth
        )
    
    # El token incluye scope para simular permisos OAuth
    token = create_token({
        "sub": user.id,
        "is_admin": user.is_admin,
        "scope": "admin" if user.is_admin else "user",
    })

    # Respuesta estándar OAuth 2.0
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 min
        "scope": "admin" if user.is_admin else "user",
    }