from pydantic import BaseModel


class AdminSessionUser(BaseModel):
    username: str
    display_name: str
    role: str = "admin"


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    admin: AdminSessionUser


class AdminMeResponse(BaseModel):
    authenticated: bool = True
    admin: AdminSessionUser
