from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import AdminSessionUser
from app.services.auth_service import AdminAuthError, get_admin_user_from_token

bearer_scheme = HTTPBearer(auto_error=False)


def require_admin_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AdminSessionUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return get_admin_user_from_token(credentials.credentials)
    except AdminAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
