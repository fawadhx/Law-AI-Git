from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.admin_auth import require_admin_auth
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse, AdminMeResponse, AdminSessionUser
from app.services.auth_service import authenticate_admin_credentials, create_admin_access_token

router = APIRouter()


@router.post("/auth/admin/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest) -> AdminLoginResponse:
    user = authenticate_admin_credentials(payload.username, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials.",
        )

    access_token, expires_in_seconds = create_admin_access_token(user)
    return AdminLoginResponse(
        access_token=access_token,
        expires_in_seconds=expires_in_seconds,
        admin=user,
    )


@router.get("/auth/admin/me", response_model=AdminMeResponse)
def admin_me(current_admin: AdminSessionUser = Depends(require_admin_auth)) -> AdminMeResponse:
    return AdminMeResponse(admin=current_admin)
