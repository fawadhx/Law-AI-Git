from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request

from app.core.config import settings
from app.schemas.auth import AdminSessionUser
from app.services.admin_audit_service import set_current_admin_audit_context
from app.services.auth_service import AdminAuthError, get_admin_user_from_token

bearer_scheme = HTTPBearer(auto_error=False)


def require_admin_auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AdminSessionUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = get_admin_user_from_token(credentials.credentials)
        set_current_admin_audit_context(user, route_path=request.url.path)
        return user
    except AdminAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_admin_write_access(
    current_admin: AdminSessionUser = Depends(require_admin_auth),
) -> AdminSessionUser:
    if current_admin.role not in set(settings.admin_auth_write_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your admin role does not have write access.",
        )
    return current_admin
