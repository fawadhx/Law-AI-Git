from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class SindhCodeAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="sindh_code",
            label="Sindh Code",
            jurisdiction="Pakistan",
            government_level="provincial",
            province="Sindh",
            trust_level="official_repository",
            source_homepage="https://sindhlaws.gov.pk/SindhIndex.aspx",
            update_mode="incremental_sync_with_manual_review",
            coverage_scope="Sindh provincial code, latest legislation, service rules, and general rules",
            supported_law_types=["Act", "Ordinance", "Rule", "Regulation", "Notification"],
            supported_languages=["en", "ur", "sd"],
            source_notes=(
                "Sindh Code and the Law Department site are official Sindh provincial sources publishing latest legislation, "
                "service rules, general rules, and other provincial legal materials."
            ),
            source_authority="Government of Sindh / Sindh Code / Law Department",
            source_priority=10,
            ingestion_stage="adapter_ready",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "Sindh adapter should use the Sindh Code index pages as primary provincial discovery sources.",
            "Where the Law Department site and Sindh Code overlap, keep the code entry as the canonical discovery source and the department page as supporting provenance.",
        ]

    def sync_notes(self) -> list[str]:
        return [
            "Refresh against latest legislation and last-uploaded Sindh Code pages to detect amendments and new uploads.",
            "Record official source URL and any uploaded-date metadata to help distinguish a fresh version from an unchanged record.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="sindh_code",
                source_url="https://sindhlaws.gov.pk/SindhIndex.aspx",
                title="Sindh provincial law catalog provenance record",
                short_title="Sindh source provenance",
                jurisdiction="Pakistan",
                government_level="provincial",
                province="Sindh",
                category="source provenance",
                law_type="Provincial Code Registry",
                status="active",
                language="en",
                version_label="provincial_catalog_seed",
                source_trust_level="official_repository",
                source_authority="Government of Sindh / Sindh Code / Law Department",
                extraction_metadata={
                    "seed_reason": "Adapter foundation for official Sindh law ingestion and sync planning.",
                    "review_priority": "medium",
                },
            )
        ]
