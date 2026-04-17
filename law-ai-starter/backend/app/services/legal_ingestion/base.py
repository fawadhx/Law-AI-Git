from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.legal_corpus import IngestionSourceDefinition, RawSourceDocumentInput


class PakistanLawIngestionAdapter(ABC):
    @abstractmethod
    def definition(self) -> IngestionSourceDefinition:
        raise NotImplementedError

    def supports_bootstrap_preview(self) -> bool:
        return True

    def bootstrap_notes(self) -> list[str]:
        return []

    def seed_documents(self) -> list[RawSourceDocumentInput]:
        return []
