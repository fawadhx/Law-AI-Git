from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


class BalochistanCodeAdapter(PakistanLawIngestionAdapter):
    def definition(self) -> IngestionSourceDefinition:
        return IngestionSourceDefinition(
            source_slug="balochistan_code",
            label="Balochistan Code",
            jurisdiction="Pakistan",
            government_level="provincial",
            province="Balochistan",
            trust_level="official_repository",
            source_homepage="https://balochistancode.gob.pk/",
            update_mode="incremental_sync_with_manual_review",
            coverage_scope="Balochistan laws, rules, regulations, ordinances, policies, and gazette notifications",
            supported_law_types=["Act", "Ordinance", "Rule", "Regulation", "Policy", "Gazette Notification"],
            supported_languages=["en", "ur"],
            source_notes=(
                "Balochistan Code is the official provincial code managed by the Law and Parliamentary Affairs Department, "
                "with alphabetical, departmental, chronological, and thematic access to laws and subordinate legislation."
            ),
            source_authority="Government of Balochistan / Balochistan Code / Law & Parliamentary Affairs Department",
            source_priority=10,
            ingestion_stage="adapter_ready",
            active=True,
        )

    def bootstrap_notes(self) -> list[str]:
        return [
            "Balochistan adapter should use Balochistan Code as the primary source and keep department-site downloads only as supporting references when needed.",
            "Because Balochistan Code exposes multiple law families and gazette-notification buckets, sync planning should preserve source type and category boundaries.",
        ]

    def sync_notes(self) -> list[str]:
        return [
            "Refresh against Balochistan Code listing pages and, where needed, lawdir-backed document references to detect new uploads.",
            "When a listing changes but the source URL stays stable, compare content hash or listing metadata before creating a new corpus version.",
        ]

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return [
            RawSourceDocumentInput(
                source_slug="balochistan_code",
                source_url="https://balochistancode.gob.pk/",
                title="Balochistan provincial law catalog provenance record",
                short_title="Balochistan source provenance",
                jurisdiction="Pakistan",
                government_level="provincial",
                province="Balochistan",
                category="source provenance",
                law_type="Provincial Code Registry",
                status="active",
                language="en",
                version_label="provincial_catalog_seed",
                source_trust_level="official_repository",
                source_authority="Government of Balochistan / Balochistan Code / Law & Parliamentary Affairs Department",
                extraction_metadata={
                    "seed_reason": "Adapter foundation for official Balochistan law ingestion and sync planning.",
                    "review_priority": "medium",
                },
            )
        ]
