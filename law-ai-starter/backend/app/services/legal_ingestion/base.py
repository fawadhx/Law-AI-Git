from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.legal_corpus import (
    IngestionDiscoveryResult,
    IngestionNormalizationResult,
    IngestionSourceDefinition,
    IngestionSyncPlan,
    RawSourceDocumentInput,
    SourceDocumentLocator,
)
from app.services.legal_ingestion.normalization import normalize_source_document


class PakistanLawIngestionAdapter(ABC):
    @abstractmethod
    def definition(self) -> IngestionSourceDefinition:
        raise NotImplementedError

    def supports_bootstrap_preview(self) -> bool:
        return True

    def bootstrap_notes(self) -> list[str]:
        return []

    def sync_notes(self) -> list[str]:
        return []

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return []

    def build_sync_plan(self) -> IngestionSyncPlan:
        definition = self.definition()
        return IngestionSyncPlan(
            source_slug=definition.source_slug,
            source_label=definition.label,
            jurisdiction=definition.jurisdiction,
            government_level=definition.government_level,
            province=definition.province,
            update_mode=definition.update_mode,
            source_priority=definition.source_priority,
            duplicate_identity_fields=[
                "jurisdiction",
                "government_level",
                "province",
                "title",
                "official_citation",
            ],
            duplicate_version_fields=[
                "source_url",
                "content_hash",
                "gazette_reference",
                "version_label",
            ],
            provenance_fields=[
                "source_slug",
                "source_url",
                "source_authority",
                "source_trust_level",
                "gazette_reference",
            ],
            sync_notes=self.sync_notes(),
        )

    def discover_documents(self) -> IngestionDiscoveryResult:
        seed_documents = self.seed_documents()
        return IngestionDiscoveryResult(
            adapter_key=self.definition().source_slug,
            discovered_documents=[
                SourceDocumentLocator(
                    document_id=f"{self.definition().source_slug}-{index + 1}",
                    source_slug=document.source_slug,
                    source_url=document.source_url,
                    label=document.title,
                    source_format=document.source_format,
                )
                for index, document in enumerate(seed_documents)
            ],
            notes=[
                f"Seed-only discovery currently available for {self.definition().label}.",
                f"{len(seed_documents)} seed source document(s) are registered for normalization preview.",
            ],
        )

    def normalize_seed_documents(self) -> IngestionNormalizationResult:
        bundles = [normalize_source_document(document) for document in self.seed_documents()]
        return IngestionNormalizationResult(
            adapter_key=self.definition().source_slug,
            bundles=bundles,
            notes=[
                f"Normalized {len(bundles)} seed document(s) into canonical instrument/version/section bundles.",
            ],
        )
