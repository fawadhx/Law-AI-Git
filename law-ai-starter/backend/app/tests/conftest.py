import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.services import admin_audit_service, admin_service


@pytest.fixture(autouse=True)
def reset_test_state():
    original_secret = settings.admin_auth_secret_key
    original_username = settings.admin_auth_username
    original_display_name = settings.admin_auth_display_name
    original_role = settings.admin_auth_role
    original_password = settings.admin_auth_password
    original_write_roles = list(settings.admin_auth_write_roles)

    settings.admin_auth_secret_key = "law-ai-test-secret"
    settings.admin_auth_username = "admin"
    settings.admin_auth_display_name = "Admin Tester"
    settings.admin_auth_role = "admin"
    settings.admin_auth_password = "admin123"
    settings.admin_auth_write_roles = ["admin"]

    admin_service.WORKSPACE_DRAFT_STORE.clear()
    admin_service.PUBLISH_PACKAGE_STORE.clear()
    admin_audit_service._FALLBACK_AUDIT_EVENTS.clear()
    admin_audit_service._current_admin_audit_context.set(None)

    try:
        yield
    finally:
        admin_service.WORKSPACE_DRAFT_STORE.clear()
        admin_service.PUBLISH_PACKAGE_STORE.clear()
        admin_audit_service._FALLBACK_AUDIT_EVENTS.clear()
        admin_audit_service._current_admin_audit_context.set(None)

        settings.admin_auth_secret_key = original_secret
        settings.admin_auth_username = original_username
        settings.admin_auth_display_name = original_display_name
        settings.admin_auth_role = original_role
        settings.admin_auth_password = original_password
        settings.admin_auth_write_roles = original_write_roles


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def admin_token(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/admin/login",
        json={"username": settings.admin_auth_username, "password": settings.admin_auth_password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}
