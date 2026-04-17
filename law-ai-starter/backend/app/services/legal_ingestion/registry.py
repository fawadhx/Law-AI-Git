from __future__ import annotations

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput
from app.services.legal_ingestion.adapters import GazettePakistanAdapter, PakistanCodeAdapter
from app.services.legal_ingestion.base import PakistanLawIngestionAdapter


def get_ingestion_adapters() -> list[PakistanLawIngestionAdapter]:
    return [
        GazettePakistanAdapter(),
        PakistanCodeAdapter(),
    ]


def get_ingestion_source_registry() -> list[IngestionSourceDefinition]:
    return [adapter.definition() for adapter in get_ingestion_adapters()]


def get_ingestion_bootstrap_notes() -> list[str]:
    notes: list[str] = []
    for adapter in get_ingestion_adapters():
        notes.extend(adapter.bootstrap_notes())
    return notes


def get_seed_source_documents() -> list[RawSourceDocumentInput]:
    documents: list[RawSourceDocumentInput] = []
    for adapter in get_ingestion_adapters():
        documents.extend(adapter.seed_documents())
    return documents
