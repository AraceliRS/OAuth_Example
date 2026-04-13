from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_token
from models import TokenData


def getDb():
    from main import db
    return db

router = APIRouter(prefix="/resource")
header = HTTPBearer()

#Valida el JWT
def getCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(header),
) -> TokenData:
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


#Valida el scope

def requireScope(scope: str):
    current = getCurrentUser()
    if scope == "admin" and not current.isAdmin:
            raise HTTPException(status_code=403, detail="Scope insuficiente")

@router.get("/greeting")
def get_my_resource(currentUser: TokenData = Depends(getCurrentUser)):
    return {"message": f"Hola {currentUser.name}"}

@router.get("/admin")
def get_admin_resource(currentUser: TokenData = Depends(requireScope("admin"))):
    return {"message": f"SOLO ADMIN como para {currentUser.email}"}