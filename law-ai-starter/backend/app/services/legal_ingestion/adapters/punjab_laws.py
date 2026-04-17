from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class PunjabLawsAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="punjab_laws",
            label="Punjab Laws Online",
            jurisdiction="Pakistan",
            government_level="provincial",
            province="Punjab",
            trust_level="official_repository",
            source_homepage="https://www.punjablaws.gov.pk/",
            update_mode="incremental_sync_with_manual_review",
            coverage_scope="Punjab Acts, rules, regulations, and regularly updated provincial laws",
            supported_law_types=["Act", "Ordinance", "Rule", "Regulation", "Notification"],
            supported_languages=["en", "ur"],
            source_notes=(
                "Punjab Laws Online is an official Government of Punjab laws repository and states that "
                "it contains Punjab laws from 1860 onward and is updated regularly after new laws and amendments."
            ),
            source_authority="Government of Punjab / Punjab Laws Online",
            source_priority=10,
            ingestion_stage="adapter_ready",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "Punjab adapter should keep provincial instruments separate from federal laws via province-aware duplicate matching.",
            "Start with metadata discovery and official source links before attempting deep document extraction.",
        ]

    def sync_notes(self) -> list[str]:
        return [
            "Run periodic catalog refresh against Punjab Laws list/search pages to detect newly uploaded or amended provincial instruments.",
            "Preserve original Punjab source URLs and compare content hash or citation metadata before creating a new version record.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="punjab_laws",
                source_url="https://www.punjablaws.gov.pk/",
                title="Punjab provincial law catalog provenance record",
                short_title="Punjab source provenance",
                jurisdiction="Pakistan",
                government_level="provincial",
                province="Punjab",
                category="source provenance",
                law_type="Provincial Code Registry",
                status="active",
                language="en",
                version_label="provincial_catalog_seed",
                source_trust_level="official_repository",
                source_authority="Government of Punjab / Punjab Laws Online",
                extraction_metadata={
                    "seed_reason": "Adapter foundation for official Punjab law ingestion and sync planning.",
                    "review_priority": "medium",
                },
            )
        ]
