from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    id: int
    name: str
    email: str
    hashedPwd: str
    isAdmin: bool

class TokenData(BaseModel):
    email: str | None = None
    isAdmin: bool = False