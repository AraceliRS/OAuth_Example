from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserLogin, UserInDB, TokenData
from auth import hashPassword, verifyPassword, createToken, verifyToken
from authorizationServer import router as auth_router
from resourceServer import router as resource_router



db: dict[str, UserInDB] = {
    "LP@email.com" : UserInDB(
        id= 1,
        name="Luis Pablo",
        email="LP@email.com",
        hashedPwd=hashPassword("labubu24"),
        isAdmin=False,
    ),
    "admin@email.com" : UserInDB(
        id = 2,
        name="Eduardo",
        email="admin@email.com",
        hashedPwd=hashPassword("soyADMIN"),
        isAdmin=True,
    ),
}

header = HTTPBearer()


app = FastAPI()
app.include_router(auth_router)
app.include_router(resource_router)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/users")  
def list_users():
    data = [{"id": str(u.id),
            "name": u.name,
            "mail": u.email,
            "pwd": u.hashedPwd,
            "isAdmin": u.isAdmin}
            for u in db.values()]
    return data
