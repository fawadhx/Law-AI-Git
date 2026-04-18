from pydantic import BaseModel, Field, field_validator


class AdminSessionUser(BaseModel):
    username: str
    display_name: str
    role: str = "admin"


class AdminLoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=128)
    password: str = Field(min_length=6, max_length=256)

    @field_validator("username", "password")
    @classmethod
    def normalize_credentials(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Credentials cannot be blank.")
        return normalized


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    admin: AdminSessionUser


class AdminMeResponse(BaseModel):
    authenticated: bool = True
    admin: AdminSessionUser
