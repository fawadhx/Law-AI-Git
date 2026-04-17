from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, IngestionSyncPlan, RawSourceDocumentInput
from app.services.legal_ingestion.adapters import (
    BalochistanCodeAdapter,
    GazettePakistanAdapter,
    KhyberPakhtunkhwaCodeAdapter,
    PakistanCodeAdapter,
    PunjabLawsAdapter,
    SindhCodeAdapter,
)
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


def get_ingestion_adapters(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[PakistanLawIngestionAdapter]:
    adapters = [
        GazettePakistanAdapter(),
        PakistanCodeAdapter(),
        PunjabLawsAdapter(),
        SindhCodeAdapter(),
        KhyberPakhtunkhwaCodeAdapter(),
        BalochistanCodeAdapter(),
    ]
    if government_level:
        adapters = [adapter for adapter in adapters if adapter.definition().government_level == government_level]
    if province:
        adapters = [
            adapter
            for adapter in adapters
            if (adapter.definition().province or "").lower() == province.lower()
        ]
    return sorted(
        adapters,
        key=lambda adapter: (
            adapter.definition().source_priority,
            adapter.definition().government_level,
            adapter.definition().province or "",
            adapter.definition().source_slug,
        ),
    )


def get_ingestion_source_registry(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[IngestionSourceDefinition]:
    return [adapter.definition() for adapter in get_ingestion_adapters(government_level=government_level, province=province)]


def get_ingestion_bootstrap_notes() -> list[str]:
    notes: list[str] = []
    for adapter in get_ingestion_adapters():
        notes.extend(adapter.bootstrap_notes())
    return notes


def get_seed_source_documents(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[RawSourceDocumentInput]:
    documents: list[RawSourceDocumentInput] = []
    for adapter in get_ingestion_adapters(government_level=government_level, province=province):
        documents.extend(adapter.seed_documents())
    return documents


def get_ingestion_sync_plans(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[IngestionSyncPlan]:
    return [adapter.build_sync_plan() for adapter in get_ingestion_adapters(government_level=government_level, province=province)]
