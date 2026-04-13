from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserLogin, UserInDB, TokenData
from auth import hashPassword, verifyPassword, createToken, verifyToken, createToken



db: dict[int, UserInDB] = {
    1 : UserInDB(
        id= 1,
        name="Luis Pablo",
        email="LP@email.com",
        hashedPwd=hashPassword("labubu24"),
        isAdmin=False,
    ),
    2 : UserInDB(
        id = 1,
        name="Eduardo",
        email="admin@email.com",
        hashedPwd=hashPassword("soyADMIN"),
        isAdmin=True,
    ),
}

header = HTTPBearer()


#rutas: 
app = FastAPI()
app.include_router(auth_router)    # Authorization Server
app.include_router(resource_router) # Resource Server

#debug
def root():
    return {"message": "API is running"}

@app.get("/users")  
def list_users():
    data = [{"id": u.id.toString(),
            "name": u.name,
            "mail": u.email,
            "pwd": u.hashedPwd,
            "isAdmin": u.isAdmin}
            for u in db.values()]
    return data
