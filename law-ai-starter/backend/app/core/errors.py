from __future__ import annotations

from fastapi import Request


LEGAL_INFORMATION_BOUNDARY_NOTE = (
    "Law AI provides legal information for public awareness only. "
    "It does not provide legal advice, legal representation, or a substitute for a lawyer."
)


class AppServiceError(Exception):
    def __init__(
        self,
        detail: str,
        *,
        status_code: int = 400,
        error_code: str = "service_error",
        metadata: dict[str, object] | None = None,
        boundary_note: str | None = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        self.metadata = metadata or {}
        self.boundary_note = boundary_note


def request_needs_legal_boundary_note(request: Request) -> bool:
    path = request.url.path
    return path.startswith("/api/v1/chat") or path == "/"


def build_error_payload(
    *,
    request: Request,
    detail: str,
    error_code: str,
    metadata: dict[str, object] | None = None,
    boundary_note: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "detail": detail,
        "error_code": error_code,
    }
    if metadata:
        payload["metadata"] = metadata

    resolved_boundary = boundary_note
    if resolved_boundary is None and request_needs_legal_boundary_note(request):
        resolved_boundary = LEGAL_INFORMATION_BOUNDARY_NOTE
    if resolved_boundary:
        payload["boundary_note"] = resolved_boundary

    return payload
