from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class KhyberPakhtunkhwaCodeAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="kp_code",
            label="Khyber Pakhtunkhwa Code",
            jurisdiction="Pakistan",
            government_level="provincial",
            province="Khyber Pakhtunkhwa",
            trust_level="official_repository",
            source_homepage="https://kpcode.kp.gov.pk/",
            update_mode="incremental_sync_with_manual_review",
            coverage_scope="Khyber Pakhtunkhwa laws in English and Urdu with search and categorized discovery",
            supported_law_types=["Act", "Ordinance", "Rule", "Regulation", "Notification"],
            supported_languages=["en", "ur"],
            source_notes=(
                "Khyber Pakhtunkhwa Code is the official provincial code site with alphabetical, departmental, "
                "chronological, and category-wise access to laws."
            ),
            source_authority="Government of Khyber Pakhtunkhwa / KP Code",
            source_priority=10,
            ingestion_stage="adapter_ready",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "KP adapter should rely on the official KP Code search and categorized lists for discovery rather than brittle deep scraping.",
            "Store province metadata explicitly as Khyber Pakhtunkhwa so similarly named federal laws stay separated.",
        ]

    def sync_notes(self) -> list[str]:
        return [
            "Run refreshes against chronological and latest search result pages to detect new or amended KP laws.",
            "Treat language variants as source-level metadata and avoid collapsing Urdu and English pages unless the underlying legal version is the same.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="kp_code",
                source_url="https://kpcode.kp.gov.pk/",
                title="Khyber Pakhtunkhwa provincial law catalog provenance record",
                short_title="KP source provenance",
                jurisdiction="Pakistan",
                government_level="provincial",
                province="Khyber Pakhtunkhwa",
                category="source provenance",
                law_type="Provincial Code Registry",
                status="active",
                language="en",
                version_label="provincial_catalog_seed",
                source_trust_level="official_repository",
                source_authority="Government of Khyber Pakhtunkhwa / KP Code",
                extraction_metadata={
                    "seed_reason": "Adapter foundation for official KP law ingestion and sync planning.",
                    "review_priority": "medium",
                },
            )
        ]
