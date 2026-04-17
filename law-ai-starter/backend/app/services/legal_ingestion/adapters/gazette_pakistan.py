from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class GazettePakistanAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="gazette_pakistan",
            label="Gazette Notifications via Pakistan Code DRS",
            jurisdiction="Pakistan",
            government_level="federal",
            trust_level="gazette_original",
            source_homepage="https://pakistancode.gov.pk/",
            update_mode="append_only_with_dedup",
            coverage_scope="Official Gazette notifications and source publication references for federal legislation",
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
                "Use Gazette-linked publications as the highest-trust provenance layer. The Pakistan Code site "
                "exposes a Document Retrieval System for Gazette notifications and also warns that users should "
                "refer to the original Gazette where doubt exists."
            ),
            source_authority="Official Gazette / Gazette-linked federal publications",
            source_priority=1,
            ingestion_stage="scaffolded",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "Prefer Gazette metadata and document identifiers for deduplication and amendment lineage.",
            "Keep Gazette files immutable and link revised Pakistan Code versions back to the originating Gazette entries.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="gazette_pakistan",
                source_url="https://pakistancode.gov.pk/",
                title="Gazette-backed federal law provenance record",
                short_title="Federal Gazette provenance",
                category="source provenance",
                law_type="Gazette Notification",
                status="active",
                language="en",
                version_label="gazette_reference_seed",
                source_trust_level="gazette_original",
                source_authority="Official Gazette / Gazette-linked federal publications",
                extraction_metadata={
                    "seed_reason": "Track Gazette provenance separately from revised-text repositories.",
                    "review_priority": "high",
                },
            )
        ]
