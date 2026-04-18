from app.services.legal_import_service import (
    get_corpus_sync_plan,
    import_federal_seed_foundation,
    preview_seed_documents,
)


def test_seed_preview_uses_official_federal_sources():
    previews = preview_seed_documents()

    assert previews
    assert any(item.government_level == "federal" for item in previews)
    assert all(item.source_url for item in previews)
    assert any("official" in item.provenance_summary.lower() for item in previews)


def test_sync_plan_includes_federal_and_provincial_sources():
    response = get_corpus_sync_plan()
    source_slugs = {item.source_slug for item in response.sync_plans}

    assert "pakistan_code" in source_slugs
    assert "punjab_laws" in source_slugs
    assert "sindh_code" in source_slugs
    assert "kp_code" in source_slugs
    assert "balochistan_code" in source_slugs


def test_federal_import_pipeline_skips_duplicate_versions(monkeypatch):
    monkeypatch.setattr(
        "app.services.legal_import_service.find_matching_instrument_candidates",
        lambda **kwargs: [],
    )
    monkeypatch.setattr(
        "app.services.legal_import_service.find_matching_version_candidates",
        lambda **kwargs: [
            type(
                "VersionMatch",
                (),
                {
                    "instrument_id": "instrument-existing",
                    "version_id": "version-existing",
                    "source_url": kwargs["source_url"],
                    "content_hash": kwargs["content_hash"],
                },
            )()
        ],
    )
    monkeypatch.setattr(
        "app.services.legal_import_service.upsert_instrument_bundle",
        lambda bundle: True,
    )
    monkeypatch.setattr(
        "app.services.legal_import_service.record_ingestion_run",
        lambda run: True,
    )

    response = import_federal_seed_foundation()

    assert response.status == "ok"
    assert response.discovered_document_count >= 1
    assert response.duplicate_bundle_count >= 1
    assert all(item.outcome == "duplicate_skipped" for item in response.items)
