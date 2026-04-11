from app.schemas.chat import ChatCategory, ChatConfidence, ChatQueryResponse, Citation
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_classification_service import detect_question_category
from app.services.legal_retrieval_service import retrieve_scored_legal_sources


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


def determine_confidence(
    scored_records: list[tuple[int, LegalSourceRecord]],
) -> ChatConfidence:
    if not scored_records:
        return ChatConfidence(level="low", score=0, matched_records=0)

    top_score = scored_records[0][0]
    matched_records = len(scored_records)
    second_score = scored_records[1][0] if len(scored_records) > 1 else 0
    score_gap = top_score - second_score

    if top_score >= 18 and score_gap >= 3:
        level = "high"
    elif top_score >= 10:
        level = "medium"
    else:
        level = "low"

    return ChatConfidence(
        level=level,
        score=top_score,
        matched_records=matched_records,
    )


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


def build_confidence_note(confidence: ChatConfidence) -> str:
    if confidence.level == "high":
        return (
            "The current prototype found a comparatively strong match in its internal legal-source records."
        )
    if confidence.level == "medium":
        return (
            "The current prototype found a reasonable match, but the result should still be read cautiously."
        )
    return (
        "The current prototype found only a limited or tentative match, so this result should be treated with extra caution."
    )


def build_no_match_answer(
    question: str,
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    return (
        f"No strong legal-source match was found in the current prototype dataset.\n\n"
        f"Confidence level: {confidence.level.upper()}\n\n"
        "What this means:\n"
        "- The system could not confidently map your question to the current internal legal records.\n"
        "- This does not mean no law applies. It only means the current prototype dataset is still limited.\n\n"
        "Issue-type guidance:\n"
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
    records: list[LegalSourceRecord],
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    primary = records[0]

    if confidence.level == "high":
        opening = (
            f"The strongest current match is {primary.citation_label} under "
            f"{primary.law_name}, which relates to \"{primary.section_title}.\""
        )
    elif confidence.level == "medium":
        opening = (
            f"A reasonably relevant current match is {primary.citation_label} under "
            f"{primary.law_name}, which relates to \"{primary.section_title}.\""
        )
    else:
        opening = (
            f"A tentative current match is {primary.citation_label} under "
            f"{primary.law_name}, which relates to \"{primary.section_title}.\""
        )

    lines: list[str] = [
        "Matched legal information",
        "",
        f"Confidence level: {confidence.level.upper()}",
        "",
        opening,
        "",
        f"Plain-language summary: {primary.summary}",
        "",
        "Issue-type guidance:",
        build_category_guidance(category["key"]),
        "",
        "Confidence note:",
        build_confidence_note(confidence),
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
    confidence: ChatConfidence,
) -> str:
    if not records:
        return build_no_match_answer(question, category, confidence)

    return build_match_answer(records, category, confidence)


def generate_mock_legal_response(question: str) -> ChatQueryResponse:
    scored_records = retrieve_scored_legal_sources(question, limit=3)
    records = [record for _, record in scored_records]

    detected_category = detect_question_category(question, records)
    confidence = determine_confidence(scored_records)

    answer = build_answer(question, records, detected_category, confidence)
    citations = build_citations(records)

    return ChatQueryResponse(
        answer=answer,
        citations=citations,
        disclaimer=LEGAL_DISCLAIMER,
        category=ChatCategory(
            key=detected_category["key"],
            label=detected_category["label"],
        ),
        confidence=confidence,
    )