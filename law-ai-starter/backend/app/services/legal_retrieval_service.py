from app.data.legal_sources import LEGAL_SOURCES
from app.schemas.legal_source import LegalSourceRecord


def normalize_text(value: str) -> str:
    return value.strip().lower()


def tokenize(value: str) -> list[str]:
    cleaned = normalize_text(value)
    return [token for token in cleaned.replace(",", " ").replace(".", " ").split() if token]


def score_record(query: str, record: LegalSourceRecord) -> int:
    query_tokens = tokenize(query)

    searchable_parts = [
        record.source_title,
        record.law_name,
        record.section_number,
        record.section_title,
        record.summary,
        record.excerpt,
        record.citation_label,
        " ".join(record.tags),
    ]

    searchable_text = normalize_text(" ".join(searchable_parts))
    score = 0

    for token in query_tokens:
        if token in searchable_text:
            score += 1

    query_lower = normalize_text(query)

    if normalize_text(record.section_title) in query_lower:
        score += 3

    if normalize_text(record.law_name) in query_lower:
        score += 3

    for tag in record.tags:
        if normalize_text(tag) in query_lower:
            score += 2

    if record.section_number and record.section_number in query_lower:
        score += 2

    return score


def retrieve_legal_sources(query: str, limit: int = 3) -> list[LegalSourceRecord]:
    scored_results: list[tuple[int, LegalSourceRecord]] = []

    for record in LEGAL_SOURCES:
        score = score_record(query, record)
        if score > 0:
            scored_results.append((score, record))

    scored_results.sort(key=lambda item: item[0], reverse=True)

    return [record for _, record in scored_results[:limit]]