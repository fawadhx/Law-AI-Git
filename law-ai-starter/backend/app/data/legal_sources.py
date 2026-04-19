from app.data.federal_catalog import FEDERAL_LEGAL_SOURCES
from app.data.provincial_catalog import PROVINCIAL_LEGAL_SOURCES
from app.schemas.legal_source import LegalSourceRecord


LEGAL_SOURCES: list[LegalSourceRecord] = [
    *FEDERAL_LEGAL_SOURCES,
    *PROVINCIAL_LEGAL_SOURCES,
]
