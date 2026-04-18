from app.services import admin_audit_service


def test_admin_login_returns_access_token_and_user(client):
    response = client.post(
        "/api/v1/auth/admin/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"]
    assert payload["expires_in_seconds"] > 0
    assert payload["admin"]["username"] == "admin"
    assert payload["admin"]["role"] == "admin"


def test_admin_me_requires_valid_bearer_token(client):
    unauthorized = client.get("/api/v1/auth/admin/me")
    assert unauthorized.status_code == 401

    login = client.post(
        "/api/v1/auth/admin/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = login.json()["access_token"]

    authorized = client.get(
        "/api/v1/auth/admin/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert authorized.status_code == 200
    assert authorized.json()["admin"]["display_name"] == "Admin Tester"


def test_failed_admin_login_is_rejected_and_audited(client):
    response = client.post(
        "/api/v1/auth/admin/login",
        json={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid admin credentials."

    items = admin_audit_service.list_admin_audit_events(limit=5)
    assert items
    assert items[0].kind == "login"
    assert items[0].status == "failed"
