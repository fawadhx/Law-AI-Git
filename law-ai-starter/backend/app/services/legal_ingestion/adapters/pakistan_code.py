from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class PakistanCodeAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="pakistan_code",
            label="Pakistan Code",
            jurisdiction="Pakistan",
            government_level="federal",
            trust_level="official_repository",
            source_homepage="https://pakistancode.gov.pk/",
            update_mode="incremental_sync",
            coverage_scope="Federal primary and secondary legislation in revised form",
            supported_law_types=[
                "Act",
                "Ordinance",
                "Rule",
                "Regulation",
                "Order",
                "Notification",
                "SRO",
            ],
            supported_languages=["en", "ur"],
            source_notes=(
                "Managed by the Ministry of Law and Justice. The site states that it carries "
                "federal primary and secondary legislation in revised form and is updated after "
                "publication in the official Gazette."
            ),
            ingestion_stage="scaffolded",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "Use this adapter as the main seed for current consolidated federal laws.",
            "Treat revised-form text as searchable working text, but preserve Gazette provenance for publication review.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="pakistan_code",
                source_url="https://pakistancode.gov.pk/english/UY2Fqa-%23-1/act/1860/XLV/64",
                title="Pakistan Penal Code, 1860",
                short_title="Pakistan Penal Code",
                category="criminal law",
                law_type="Act",
                promulgation_date="1860-10-06",
                status="active",
                official_citation="Act XLV of 1860",
                language="en",
                version_label="revised_federal_text",
                source_trust_level="official_repository",
                extraction_metadata={
                    "seed_reason": "Existing prototype corpus already references this federal law extensively.",
                    "review_priority": "high",
                },
            ),
            RawSourceDocumentInput(
                source_slug="pakistan_code",
                source_url="https://pakistancode.gov.pk/english/UY2Fqa-%23-1/act/1898/V/12",
                title="Code of Criminal Procedure, 1898",
                short_title="CrPC",
                category="criminal procedure",
                law_type="Act",
                promulgation_date="1898-03-22",
                status="active",
                official_citation="Act V of 1898",
                language="en",
                version_label="revised_federal_text",
                source_trust_level="official_repository",
                extraction_metadata={
                    "seed_reason": "Priority federal procedural law for officer powers, arrest, search, and FIR guidance.",
                    "review_priority": "high",
                },
            ),
        ]
