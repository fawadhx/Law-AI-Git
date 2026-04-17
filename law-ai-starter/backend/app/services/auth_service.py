from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.schemas.auth import AdminSessionUser


class AdminAuthError(ValueError):
    pass


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("ascii"))


def _json_b64url(value: dict[str, object]) -> str:
    return _b64url_encode(json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8"))


def _sign_token(message: str) -> str:
    signature = hmac.new(
        settings.admin_auth_secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return _b64url_encode(signature)


def _build_token(payload: dict[str, object]) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _json_b64url(header)
    payload_segment = _json_b64url(payload)
    signing_input = f"{header_segment}.{payload_segment}"
    signature_segment = _sign_token(signing_input)
    return f"{signing_input}.{signature_segment}"


def _decode_token(token: str) -> dict[str, object]:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise AdminAuthError("Malformed token.") from exc

    signing_input = f"{header_segment}.{payload_segment}"
    expected_signature = _sign_token(signing_input)
    if not hmac.compare_digest(expected_signature, signature_segment):
        raise AdminAuthError("Invalid token signature.")

    try:
        payload = json.loads(_b64url_decode(payload_segment).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AdminAuthError("Invalid token payload.") from exc

    if not isinstance(payload, dict):
        raise AdminAuthError("Invalid token payload.")

    issuer = str(payload.get("iss") or "")
    if issuer != settings.admin_auth_issuer:
        raise AdminAuthError("Invalid token issuer.")

    expires_at = int(payload.get("exp") or 0)
    if expires_at <= int(datetime.now(timezone.utc).timestamp()):
        raise AdminAuthError("Token expired.")

    if str(payload.get("role") or "") != "admin":
        raise AdminAuthError("Invalid admin role.")

    return payload


def _expected_password_hash() -> str:
    if settings.admin_auth_password_sha256:
        return settings.admin_auth_password_sha256.strip().lower()
    return hashlib.sha256(settings.admin_auth_password.encode("utf-8")).hexdigest()


def authenticate_admin_credentials(username: str, password: str) -> AdminSessionUser | None:
    normalized_username = username.strip()
    if not hmac.compare_digest(normalized_username, settings.admin_auth_username):
        return None

    provided_password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if not hmac.compare_digest(provided_password_hash, _expected_password_hash()):
        return None

    return AdminSessionUser(
        username=settings.admin_auth_username,
        display_name=settings.admin_auth_display_name,
        role=settings.admin_auth_role,
    )


def create_admin_access_token(user: AdminSessionUser) -> tuple[str, int]:
    expires_in_seconds = settings.admin_auth_access_token_ttl_minutes * 60
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user.username,
        "username": user.username,
        "display_name": user.display_name,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in_seconds)).timestamp()),
        "iss": settings.admin_auth_issuer,
    }
    return _build_token(payload), expires_in_seconds


def get_admin_user_from_token(token: str) -> AdminSessionUser:
    payload = _decode_token(token)
    return AdminSessionUser(
        username=str(payload.get("username") or payload.get("sub") or settings.admin_auth_username),
        display_name=str(payload.get("display_name") or settings.admin_auth_display_name),
        role=str(payload.get("role") or settings.admin_auth_role),
    )
