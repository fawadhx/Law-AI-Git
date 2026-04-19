from __future__ import annotations

from dataclasses import dataclass

from app.schemas.legal_source import LegalSourceRecord


@dataclass(frozen=True, slots=True)
class FederalLawMetadata:
    law_name: str
    source_title: str
    short_label: str
    category: str
    law_type: str
    official_citation: str | None
    enactment_year: int | None
    effective_year: int | None
    source_url: str | None
    source_trust_level: str | None
    source_status: str
    source_last_verified: str | None
    amendment_notes: str | None


FEDERAL_LAW_METADATA: dict[str, FederalLawMetadata] = {
    "ppc": FederalLawMetadata(
        law_name="Pakistan Penal Code",
        source_title="Pakistan Penal Code, 1860",
        short_label="PPC",
        category="criminal law",
        law_type="Act",
        official_citation="Act XLV of 1860",
        enactment_year=1860,
        effective_year=1860,
        source_url="https://pakistancode.gov.pk/english/UY2Fqa-%23-1/act/1860/XLV/64",
        source_trust_level="official_repository",
        source_status="curated_catalog",
        source_last_verified=None,
        amendment_notes=(
            "This catalog uses structured federal-law records keyed to the Pakistan Code revised-form source. "
            "Gazette-linked amendment lineage should still be checked where exact amendment history matters."
        ),
    ),
    "crpc": FederalLawMetadata(
        law_name="Code of Criminal Procedure",
        source_title="Code of Criminal Procedure, 1898",
        short_label="CrPC",
        category="criminal procedure",
        law_type="Act",
        official_citation="Act V of 1898",
        enactment_year=1898,
        effective_year=1898,
        source_url="https://pakistancode.gov.pk/english/UY2Fqa-%23-1/act/1898/V/12",
        source_trust_level="official_repository",
        source_status="curated_catalog",
        source_last_verified=None,
        amendment_notes=(
            "This catalog captures high-value public-facing CrPC sections for arrest, FIR, investigation, remand, and reporting guidance. "
            "It is not yet a complete procedural corpus."
        ),
    ),
    "peca": FederalLawMetadata(
        law_name="Prevention of Electronic Crimes Act",
        source_title="Prevention of Electronic Crimes Act, 2016",
        short_label="PECA",
        category="cyber law",
        law_type="Act",
        official_citation="Act XL of 2016",
        enactment_year=2016,
        effective_year=2016,
        source_url=None,
        source_trust_level="official_metadata_pending",
        source_status="curated_catalog",
        source_last_verified=None,
        amendment_notes=(
            "The current PECA records are structured for retrieval and public-awareness coverage. "
            "Exact repository-link validation should be completed before broader corpus migration."
        ),
    ),
}


def build_structured_excerpt(*, law_name: str, section_number: str, section_title: str) -> str:
    return (
        f"Structured catalog note: this record covers {law_name} section {section_number} on {section_title}. "
        "It is a retrieval-oriented educational summary, and the official source metadata should be used for verification."
    )


def build_federal_record(
    *,
    law_key: str,
    record_id: str,
    section_number: str,
    section_title: str,
    summary: str,
    excerpt: str | None = None,
    citation_label: str | None = None,
    tags: list[str] | None = None,
    aliases: list[str] | None = None,
    keywords: list[str] | None = None,
    related_sections: list[str] | None = None,
    offence_group: str | None = None,
    punishment_summary: str | None = None,
    provision_kind: str = "general",
) -> LegalSourceRecord:
    metadata = FEDERAL_LAW_METADATA[law_key]
    merged_tags = [metadata.category, "federal law", metadata.short_label.lower()]
    merged_tags.extend(tags or [])

    return LegalSourceRecord(
        id=record_id,
        source_title=metadata.source_title,
        law_name=metadata.law_name,
        section_number=section_number,
        section_title=section_title,
        summary=summary,
        excerpt=excerpt or build_structured_excerpt(
            law_name=metadata.law_name,
            section_number=section_number,
            section_title=section_title,
        ),
        citation_label=citation_label or f"{metadata.short_label} Section {section_number}",
        country="Pakistan",
        jurisdiction="Pakistan",
        jurisdiction_type="federal",
        government_level="federal",
        province=None,
        law_category=metadata.category,
        law_type=metadata.law_type,
        source_status=metadata.source_status,
        official_citation=metadata.official_citation,
        enactment_year=metadata.enactment_year,
        effective_year=metadata.effective_year,
        source_url=metadata.source_url,
        source_last_verified=metadata.source_last_verified,
        amendment_notes=metadata.amendment_notes,
        tags=merged_tags,
        aliases=list(aliases or []),
        keywords=list(keywords or []),
        related_sections=list(related_sections or []),
        offence_group=offence_group,
        punishment_summary=punishment_summary,
        provision_kind=provision_kind,
        source_trust_level=metadata.source_trust_level,
        provenance=(
            f"{metadata.source_title} structured federal catalog entry"
            if not metadata.source_url
            else f"{metadata.source_title} | trust: {metadata.source_trust_level} | official source"
        ),
    )
