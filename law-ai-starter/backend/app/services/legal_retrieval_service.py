import re

from app.data.legal_sources import LEGAL_SOURCES
from app.schemas.legal_source import LegalSourceRecord


CONCEPT_SYNONYMS: dict[str, list[str]] = {
    "theft": [
        "theft",
        "steal",
        "stolen",
        "stealing",
        "snatch",
        "snatched",
        "property",
    ],
    "punishment": [
        "punishment",
        "penalty",
        "sentence",
        "fine",
        "imprisonment",
        "jail",
    ],
    "threat": [
        "threat",
        "threaten",
        "threatened",
        "threatening",
        "intimidation",
        "criminal intimidation",
        "alarm",
    ],
    "defamation": [
        "defamation",
        "defame",
        "reputation",
        "false statement",
        "badnami",
    ],
    "online": [
        "online",
        "internet",
        "cyber",
        "digital",
        "social media",
        "facebook",
        "instagram",
        "whatsapp",
    ],
    "privacy": [
        "privacy",
        "private",
        "personal data",
        "personal information",
    ],
    "modesty": [
        "modesty",
        "image misuse",
        "photo misuse",
        "explicit image",
        "video misuse",
        "minor",
        "child",
    ],
    "arrest": [
        "arrest",
        "arrested",
        "custody",
        "detain",
        "detained",
        "without warrant",
        "warrant",
    ],
    "detention": [
        "detention",
        "24 hours",
        "twenty four hours",
        "twenty-four hours",
        "custody",
        "illegal detention",
    ],
    "unauthorized_access": [
        "unauthorised access",
        "unauthorized access",
        "hack",
        "hacked",
        "hacking",
        "access to data",
        "access to system",
        "account access",
    ],
    "police": [
        "police",
        "officer",
        "sho",
        "asi",
        "inspector",
    ],
}

PHRASE_HINTS: dict[str, list[str]] = {
    "online threat": ["threat", "online"],
    "social media threat": ["threat", "online"],
    "online harassment": ["online", "privacy", "defamation"],
    "social media post": ["online", "defamation"],
    "without warrant": ["arrest", "police"],
    "24 hours": ["detention", "arrest"],
    "reputation harm": ["defamation", "privacy"],
    "image misuse": ["modesty", "online"],
    "minor online": ["modesty", "online"],
    "hacked account": ["unauthorized_access", "online"],
}


def normalize_text(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s\-]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def tokenize(value: str) -> list[str]:
    cleaned = normalize_text(value)
    return [token for token in cleaned.split(" ") if token]


def expand_query_terms(query: str) -> list[str]:
    query_lower = normalize_text(query)
    expanded_terms: list[str] = []

    base_tokens = tokenize(query)
    expanded_terms.extend(base_tokens)

    for phrase, concepts in PHRASE_HINTS.items():
        if phrase in query_lower:
            expanded_terms.append(phrase)
            for concept in concepts:
                expanded_terms.append(concept)
                expanded_terms.extend(CONCEPT_SYNONYMS.get(concept, []))

    for concept, synonyms in CONCEPT_SYNONYMS.items():
        concept_matched = concept in query_lower
        synonym_matched = any(normalize_text(synonym) in query_lower for synonym in synonyms)

        if concept_matched or synonym_matched:
            expanded_terms.append(concept)
            expanded_terms.extend(synonyms)

    seen: set[str] = set()
    unique_terms: list[str] = []

    for term in expanded_terms:
        normalized = normalize_text(term)
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_terms.append(normalized)

    return unique_terms


def score_record(query: str, record: LegalSourceRecord) -> int:
    query_lower = normalize_text(query)
    query_terms = expand_query_terms(query)

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
    searchable_tokens = set(tokenize(searchable_text))

    score = 0

    for term in query_terms:
        if " " in term:
            if term in searchable_text:
                score += 4
        else:
            if term in searchable_tokens:
                score += 2
            elif term in searchable_text:
                score += 1

    if normalize_text(record.section_title) in query_lower:
        score += 5

    if normalize_text(record.law_name) in query_lower:
        score += 4

    if normalize_text(record.citation_label) in query_lower:
        score += 5

    for tag in record.tags:
        tag_normalized = normalize_text(tag)
        if tag_normalized in query_lower:
            score += 3

    if record.section_number and record.section_number in query_lower:
        score += 3

    punishment_requested = any(
        word in query_lower for word in ["punishment", "penalty", "sentence", "fine", "jail"]
    )
    if punishment_requested and "punishment" in normalize_text(record.section_title):
        score += 4

    online_requested = any(
        phrase in query_lower for phrase in ["online", "internet", "cyber", "social media"]
    )
    if online_requested and record.law_name == "Prevention of Electronic Crimes Act":
        score += 4

    police_requested = any(
        word in query_lower for word in ["police", "arrest", "detain", "custody", "warrant"]
    )
    if police_requested and record.law_name == "Code of Criminal Procedure":
        score += 4

    return score


def retrieve_legal_sources(query: str, limit: int = 3) -> list[LegalSourceRecord]:
    scored_results: list[tuple[int, LegalSourceRecord]] = []

    for record in LEGAL_SOURCES:
        score = score_record(query, record)
        if score > 0:
            scored_results.append((score, record))

    scored_results.sort(
        key=lambda item: (
            item[0],
            item[1].law_name,
            item[1].section_number,
        ),
        reverse=True,
    )

    return [record for _, record in scored_results[:limit]]