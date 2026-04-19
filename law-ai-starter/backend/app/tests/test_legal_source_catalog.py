from app.data.legal_sources import LEGAL_SOURCES
from app.services.legal_retrieval_service import (
    explain_record_match,
    retrieve_scored_legal_sources,
    score_record,
    select_best_excerpt,
)


def test_federal_catalog_is_materially_expanded():
    assert len(LEGAL_SOURCES) >= 50


def test_federal_records_include_structured_metadata():
    record = next(item for item in LEGAL_SOURCES if item.id == "ppc-378")

    assert record.country == "Pakistan"
    assert record.jurisdiction_type == "federal"
    assert record.government_level == "federal"
    assert record.law_category == "criminal law"
    assert record.law_type == "Act"
    assert record.source_status == "curated_catalog"
    assert record.official_citation == "Act XLV of 1860"
    assert record.source_url
    assert record.source_trust_level in {"official_repository", "official_metadata_pending"}


def test_new_crpc_remand_record_is_available_for_retrieval():
    record = next(item for item in LEGAL_SOURCES if item.id == "crpc-167")

    assert record.section_title == "Procedure when investigation cannot be completed in twenty-four hours"
    assert "remand" in " ".join(record.keywords).lower()
    assert "24 hours" in " ".join(record.tags).lower()


def test_provincial_seed_records_are_structured_and_separated():
    record = next(item for item in LEGAL_SOURCES if item.id == "prov-punjab-catalog")

    assert record.country == "Pakistan"
    assert record.jurisdiction_type == "provincial"
    assert record.government_level == "provincial"
    assert record.province == "Punjab"
    assert record.law_category == "provincial law access"
    assert record.provision_kind == "source_reference"
    assert record.source_url == "https://www.punjablaws.gov.pk/"


def test_exact_section_lookup_prioritizes_requested_section():
    results = retrieve_scored_legal_sources("What does PPC section 448 cover?", limit=3)

    assert results
    assert results[0][1].section_number == "448"


def test_province_query_prioritizes_matching_provincial_source_reference():
    punjab = next(item for item in LEGAL_SOURCES if item.id == "prov-punjab-catalog")
    sindh = next(item for item in LEGAL_SOURCES if item.id == "prov-sindh-catalog")

    query = "Where can I find Punjab provincial laws?"

    assert score_record(query, punjab) > score_record(query, sindh)
    assert any("Punjab" in reason for reason in explain_record_match(query, punjab))


def test_query_aware_excerpt_prefers_relevant_evidence_fragment():
    record = next(item for item in LEGAL_SOURCES if item.id == "crpc-167")

    excerpt = select_best_excerpt("remand when investigation cannot finish in 24 hours", record)

    assert "investigation" in excerpt.lower() or "twenty-four" in excerpt.lower() or "24" in excerpt.lower()
