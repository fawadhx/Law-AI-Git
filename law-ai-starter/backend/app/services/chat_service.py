from app.schemas.chat import Citation, ChatQueryResponse
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_retrieval_service import retrieve_legal_sources


LEGAL_DISCLAIMER = (
    "This system is intended for legal information and public awareness only. "
    "It should not be treated as a substitute for professional legal advice or representation."
)


def build_citations(records: list[LegalSourceRecord]) -> list[Citation]:
    citations: list[Citation] = []

    for record in records:
        citations.append(
            Citation(
                title=record.source_title,
                section=f"{record.citation_label} — {record.section_title}",
                note=record.summary,
            )
        )

    return citations


def build_no_match_answer(question: str) -> str:
    return (
        "No strong legal-source match was found in the current prototype dataset.\n\n"
        "What this means:\n"
        "- The system could not confidently map your question to the small internal sample of legal records.\n"
        "- This does not mean no law applies. It only means the current prototype dataset is limited.\n\n"
        "Try asking with clearer legal terms such as:\n"
        "- theft\n"
        "- arrest without warrant\n"
        "- detention for 24 hours\n"
        "- criminal intimidation\n"
        "- defamation\n"
        "- PECA dignity or privacy\n"
        "- a specific section number\n\n"
        f"Your question was: \"{question.strip()}\""
    )


def build_match_answer(question: str, records: list[LegalSourceRecord]) -> str:
    primary = records[0]

    lines: list[str] = [
        "Matched legal information",
        "",
        (
            f"The strongest current match is {primary.citation_label} under "
            f"{primary.law_name}, which relates to \"{primary.section_title}.\""
        ),
        "",
        f"Plain-language summary: {primary.summary}",
    ]

    if len(records) > 1:
        lines.extend(
            [
                "",
                "Other potentially relevant provisions:",
            ]
        )

        for record in records[1:]:
            lines.append(
                f"- {record.citation_label} ({record.section_title})"
            )

    lines.extend(
        [
            "",
            "Current prototype note:",
            (
                "This answer is based on the internal structured legal-source records currently "
                "loaded into the prototype. It is general legal information, not a substitute for "
                "professional legal advice."
            ),
        ]
    )

    return "\n".join(lines)


def build_answer(question: str, records: list[LegalSourceRecord]) -> str:
    if not records:
        return build_no_match_answer(question)

    return build_match_answer(question, records)


def generate_mock_legal_response(question: str) -> ChatQueryResponse:
    records = retrieve_legal_sources(question, limit=3)
    answer = build_answer(question, records)
    citations = build_citations(records)

    return ChatQueryResponse(
        answer=answer,
        citations=citations,
        disclaimer=LEGAL_DISCLAIMER,
    )