from __future__ import annotations

from app.schemas.legal_corpus import IngestionDiscoveryResult, IngestionNormalizationResult
from app.services.legal_ingestion.registry import get_ingestion_adapters


def run_seed_discovery(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[IngestionDiscoveryResult]:
    return [
        adapter.discover_documents()
        for adapter in get_ingestion_adapters(government_level=government_level, province=province)
    ]


def run_seed_normalization(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[IngestionNormalizationResult]:
    return [
        adapter.normalize_seed_documents()
        for adapter in get_ingestion_adapters(government_level=government_level, province=province)
    ]
