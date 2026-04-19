from __future__ import annotations

from dataclasses import dataclass

from app.schemas.legal_source import LegalSourceRecord


@dataclass(frozen=True, slots=True)
class ProvincialSourceMetadata:
    province: str
    source_title: str
    source_label: str
    source_url: str
    source_authority: str
    category: str = "provincial law access"
    law_type: str = "Provincial Code Registry"
    source_trust_level: str = "official_repository"
    source_status: str = "official_repository_index"


PROVINCIAL_SOURCE_METADATA: dict[str, ProvincialSourceMetadata] = {
    "punjab": ProvincialSourceMetadata(
        province="Punjab",
        source_title="Punjab Laws Online",
        source_label="Punjab Laws",
        source_url="https://www.punjablaws.gov.pk/",
        source_authority="Government of Punjab / Punjab Laws Online",
    ),
    "sindh": ProvincialSourceMetadata(
        province="Sindh",
        source_title="Sindh Code",
        source_label="Sindh Code",
        source_url="https://sindhlaws.gov.pk/SindhIndex.aspx",
        source_authority="Government of Sindh / Sindh Code / Law Department",
    ),
    "kpk": ProvincialSourceMetadata(
        province="Khyber Pakhtunkhwa",
        source_title="Khyber Pakhtunkhwa Code",
        source_label="KP Code",
        source_url="https://kpcode.kp.gov.pk/",
        source_authority="Government of Khyber Pakhtunkhwa / KP Code",
    ),
    "balochistan": ProvincialSourceMetadata(
        province="Balochistan",
        source_title="Balochistan Code",
        source_label="Balochistan Code",
        source_url="https://balochistancode.gob.pk/",
        source_authority="Government of Balochistan / Balochistan Code / Law & Parliamentary Affairs Department",
    ),
}


def build_provincial_source_record(
    *,
    province_key: str,
    record_id: str,
    section_title: str,
    summary: str,
    aliases: list[str] | None = None,
    keywords: list[str] | None = None,
    tags: list[str] | None = None,
) -> LegalSourceRecord:
    metadata = PROVINCIAL_SOURCE_METADATA[province_key]
    merged_tags = [
        metadata.category,
        "provincial law",
        metadata.province,
        metadata.source_label.lower(),
    ]
    merged_tags.extend(tags or [])

    return LegalSourceRecord(
        id=record_id,
        source_title=metadata.source_title,
        law_name=f"{metadata.province} provincial legislation catalog",
        section_number="catalog",
        section_title=section_title,
        summary=summary,
        excerpt=(
            f"This is a province-aware source-reference record for {metadata.province}. "
            "It points users and internal matching logic to the official provincial legislation repository. "
            "It is not a substitute for verified section-level provincial law extraction."
        ),
        citation_label=f"{metadata.source_label} catalog reference",
        country="Pakistan",
        jurisdiction="Pakistan",
        jurisdiction_type="provincial",
        government_level="provincial",
        province=metadata.province,
        law_category=metadata.category,
        law_type=metadata.law_type,
        source_status=metadata.source_status,
        official_citation=None,
        enactment_year=None,
        effective_year=None,
        source_url=metadata.source_url,
        source_last_verified=None,
        amendment_notes=(
            "This record is a structured provincial seed reference only. "
            "Verified province-specific section records should be added later from official provincial repositories."
        ),
        tags=merged_tags,
        aliases=list(aliases or []),
        keywords=list(keywords or []),
        related_sections=[],
        offence_group="provincial_source_reference",
        punishment_summary=None,
        provision_kind="source_reference",
        provenance=f"{metadata.source_authority} | trust: {metadata.source_trust_level} | official source",
        source_trust_level=metadata.source_trust_level,
    )
