from app.services import admin_audit_service


VALID_DRAFT = {
    "source_title": "Pakistan Penal Code",
    "law_name": "Pakistan Penal Code, 1860",
    "section_number": "302",
    "section_title": "Punishment of qatl-i-amd",
    "summary": "Explains the punishment framework for intentional homicide in plain language for legal-information use.",
    "excerpt": "Whoever commits qatl-i-amd shall, subject to law, be punished according to the applicable punishment framework and procedure.",
    "citation_label": "Pakistan Penal Code, 1860 s. 302",
    "jurisdiction": "Pakistan",
    "tags": ["criminal law", "homicide"],
    "aliases": ["murder punishment"],
    "keywords": ["qatl-i-amd", "punishment", "homicide"],
    "related_sections": ["300", "301"],
    "offence_group": "homicide",
    "punishment_summary": "Punishment varies by applicable legal framework and circumstances.",
    "provision_kind": "punishment",
}


def test_admin_summary_is_protected(client):
    response = client.get("/api/v1/admin/summary")
    assert response.status_code == 401


def test_admin_sources_validate_allows_authenticated_admin(client, admin_headers):
    response = client.post(
        "/api/v1/admin/sources/validate",
        json=VALID_DRAFT,
        headers=admin_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["preview"]["citation_label"] == VALID_DRAFT["citation_label"]
    assert payload["readiness_score"] >= 0


def test_admin_sources_expose_structured_metadata(client, admin_headers):
    response = client.get("/api/v1/admin/sources", headers=admin_headers)

    assert response.status_code == 200
    payload = response.json()
    item = next(record for record in payload["items"] if record["id"] == "crpc-167")
    assert item["law_type"] == "Act"
    assert item["government_level"] == "federal"
    assert item["source_status"] == "curated_catalog"
    assert item["official_citation"] == "Act V of 1898"


def test_admin_sources_expose_available_provinces_and_provincial_records(client, admin_headers):
    response = client.get("/api/v1/admin/sources", headers=admin_headers)

    assert response.status_code == 200
    payload = response.json()
    assert "Punjab" in payload["available_provinces"]
    provincial_item = next(record for record in payload["items"] if record["id"] == "prov-punjab-catalog")
    assert provincial_item["government_level"] == "provincial"
    assert provincial_item["jurisdiction_type"] == "provincial"
    assert provincial_item["province"] == "Punjab"


def test_admin_workspace_save_and_stage_produce_audit_entries(client, admin_headers):
    save_response = client.post(
        "/api/v1/admin/workspace/drafts/save",
        json={"label": "Homicide draft", "draft": VALID_DRAFT},
        headers=admin_headers,
    )
    assert save_response.status_code == 200
    saved = save_response.json()
    workspace_draft_id = saved["workspace_draft"]["workspace_draft_id"]

    stage_response = client.post(
        "/api/v1/admin/workspace/publish-packages/stage",
        json={"workspace_draft_id": workspace_draft_id, "draft": VALID_DRAFT},
        headers=admin_headers,
    )
    assert stage_response.status_code == 200
    staged = stage_response.json()
    assert staged["publish_status"] == "preview_ready"

    items = admin_audit_service.list_admin_audit_events(limit=10)
    kinds = [item.kind for item in items]
    assert "workspace_save" in kinds
    assert "stage_publish" in kinds
