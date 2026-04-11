from app.schemas.chat import Citation, ChatQueryResponse
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_classification_service import detect_question_category
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


def build_category_guidance(category_key: str) -> str:
    guidance_map = {
        "theft": (
            "This appears to relate to a property-removal or theft-type issue. "
            "The system will usually check the core offence provision first, then the punishment provision."
        ),
        "criminal_intimidation": (
            "This appears to involve threats, intimidation, or pressure intended to cause alarm. "
            "The system will usually check both the offence definition and the punishment-related provision."
        ),
        "defamation": (
            "This appears to involve reputation harm, false statements, or defamation-related issues. "
            "The system will usually check the main defamation provision and then the punishment provision."
        ),
        "cybercrime": (
            "This appears to involve an online or digital issue. "
            "The system will usually check PECA-related provisions first, especially where privacy, dignity, unauthorized access, or online misuse is involved."
        ),
        "arrest_detention": (
            "This appears to involve arrest, detention, custody, or police procedure. "
            "The system will usually check criminal-procedure provisions such as warrant and detention limits."
        ),
        "officer_authority": (
            "This appears to concern police rank, authority, or powers. "
            "The system will usually check structured officer-authority records rather than only offence provisions."
        ),
        "general": (
            "This appears to be a broader legal-information question. "
            "The system will try to match the closest available structured legal records in the prototype dataset."
        ),
    }

    return guidance_map.get(category_key, guidance_map["general"])


def build_no_match_answer(question: str, category: dict[str, str]) -> str:
    return (
        f"Detected category: {category['label']}\n\n"
        "No strong legal-source match was found in the current prototype dataset.\n\n"
        "What this means:\n"
        "- The system could not confidently map your question to the small internal sample of legal records.\n"
        "- This does not mean no law applies. It only means the current prototype dataset is still limited.\n\n"
        "Category guidance:\n"
        f"- {build_category_guidance(category['key'])}\n\n"
        "Try asking with clearer legal terms such as:\n"
        "- theft\n"
        "- arrest without warrant\n"
        "- detention for 24 hours\n"
        "- criminal intimidation\n"
        "- defamation\n"
        "- PECA dignity or privacy\n"
        "- a specific section number\n\n"
        f'Your question was: "{question.strip()}"'
    )


def build_match_answer(
    question: str,
    records: list[LegalSourceRecord],
    category: dict[str, str],
) -> str:
    primary = records[0]

    lines: list[str] = [
        f"Detected category: {category['label']}",
        "",
        "Matched legal information",
        "",
        (
            f"The strongest current match is {primary.citation_label} under "
            f"{primary.law_name}, which relates to \"{primary.section_title}.\""
        ),
        "",
        f"Plain-language summary: {primary.summary}",
        "",
        "Category guidance:",
        build_category_guidance(category["key"]),
    ]

    if len(records) > 1:
        lines.extend(
            [
                "",
                "Other potentially relevant provisions:",
            ]
        )

        for record in records[1:]:
            lines.append(f"- {record.citation_label} ({record.section_title})")

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


def build_answer(
    question: str,
    records: list[LegalSourceRecord],
    category: dict[str, str],
) -> str:
    if not records:
        return build_no_match_answer(question, category)

    return build_match_answer(question, records, category)


def generate_mock_legal_response(question: str) -> ChatQueryResponse:
    records = retrieve_legal_sources(question, limit=3)
    category = detect_question_category(question, records)
    answer = build_answer(question, records, category)
    citations = build_citations(records)

    return ChatQueryResponse(
        answer=answer,
        citations=citations,
        disclaimer=LEGAL_DISCLAIMER,
    )