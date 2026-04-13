from app.schemas.chat import (
    ChatCategory,
    ChatConfidence,
    ChatQueryResponse,
    Citation,
    MatchExplanation,
)
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_classification_service import detect_question_category
from app.services.legal_retrieval_service import (
    explain_record_match,
    retrieve_scored_legal_sources,
)


LEGAL_DISCLAIMER = (
    "Law AI provides legal information for public awareness only. "
    "It does not provide legal advice, legal representation, or a substitute for a lawyer."
)


def build_citations(records: list[LegalSourceRecord]) -> list[Citation]:
    return [
        Citation(
            title=record.law_name,
            section=record.section_number,
            note=record.section_title,
            excerpt=record.excerpt,
        )
        for record in records
    ]



def determine_confidence(
    scored_records: list[tuple[int, LegalSourceRecord]],
) -> ChatConfidence:
    if not scored_records:
        return ChatConfidence(level="low", score=0, matched_records=0)

    top_score = scored_records[0][0]
    total_matches = len(scored_records)
    second_score = scored_records[1][0] if len(scored_records) > 1 else 0
    score_gap = top_score - second_score

    if top_score >= 20 and total_matches >= 2:
        level = "high"
    elif top_score >= 12:
        level = "medium"
    else:
        level = "low"

    if level == "medium" and score_gap >= 8 and top_score >= 16:
        level = "high"

    return ChatConfidence(
        level=level,
        score=top_score,
        matched_records=total_matches,
    )



def build_why_matched(
    question: str,
    records: list[LegalSourceRecord],
) -> list[MatchExplanation]:
    explanations: list[MatchExplanation] = []

    for record in records[:3]:
        reasons = explain_record_match(question, record)
        explanations.append(
            MatchExplanation(
                title=f"{record.citation_label} — {record.section_title}",
                points=reasons,
            )
        )

    return explanations



def build_category_guidance(category_key: str) -> str:
    guidance_map = {
        "theft": (
            "This appears to involve a property-taking issue. "
            "The system will usually check the main theft provision and then any linked punishment provision."
        ),
        "cheating_fraud": (
            "This appears to involve cheating, fraud, dishonest inducement, or criminal breach of trust. "
            "The system will usually check the offence-defining section first and then any linked punishment section."
        ),
        "criminal_intimidation": (
            "This appears to involve a threat, intimidation, or pressure-related issue. "
            "The system will usually check criminal-intimidation provisions and their punishment section."
        ),
        "defamation": (
            "This appears to involve reputation harm, false statements, or defamation-related issues. "
            "The system will usually check the main defamation provision and then the punishment provision."
        ),
        "harassment": (
            "This appears to involve harassment, stalking, insulting modesty, privacy intrusion, or related conduct. "
            "The system may match PPC Section 509, PECA cyber-stalking provisions, or both, depending on the facts."
        ),
        "cybercrime": (
            "This appears to involve an online or digital issue. "
            "The system will usually check PECA-related provisions first, especially where privacy, dignity, unauthorized access, or online misuse is involved."
        ),
        "trespass": (
            "This appears to involve unlawful entry, land possession, or criminal-trespass issues. "
            "The system will usually check the trespass-defining provision and then the punishment section."
        ),
        "arrest_detention": (
            "This appears to involve arrest, detention, custody, or police procedure. "
            "The system will usually check criminal-procedure provisions such as manner of arrest, warrant rules, and detention limits."
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



def build_record_reference(record: LegalSourceRecord) -> str:
    lines = [
        f"- {record.citation_label}",
        f"  Law: {record.law_name}",
        f"  Section title: {record.section_title}",
    ]

    if record.punishment_summary:
        lines.append(f"  Punishment note: {record.punishment_summary}")

    if record.related_sections:
        lines.append(f"  Related sections: {', '.join(record.related_sections[:2])}")

    return "\n".join(lines)



def build_no_match_answer(
    question: str,
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    return (
        "No strong legal-source match was found in the current prototype dataset.\n\n"
        f"Confidence level: {confidence.level.upper()}\n\n"
        "What this means:\n"
        "- The system could not confidently map your question to the current internal legal records.\n"
        "- This does not mean no law applies. It only means the current prototype dataset is still limited.\n\n"
        "Issue-type guidance:\n"
        f"- {build_category_guidance(category['key'])}\n\n"
        "Try asking with clearer legal terms such as:\n"
        "- theft\n"
        "- cheating or 420\n"
        "- criminal breach of trust\n"
        "- arrest without warrant\n"
        "- detention for 24 hours\n"
        "- criminal intimidation\n"
        "- defamation\n"
        "- sexual harassment or cyber stalking\n"
        "- criminal trespass\n"
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
        opening = "A strong current match was found in the prototype dataset."
    elif confidence.level == "medium":
        opening = "A reasonably relevant current match was found in the prototype dataset."
    else:
        opening = "A tentative current match was found in the prototype dataset."

    lines: list[str] = [
        "Matched legal information",
        "",
        f"Confidence level: {confidence.level.upper()}",
        "",
        opening,
        "",
        "Primary matched provision:",
        build_record_reference(primary),
        "",
        f"Plain-language summary: {primary.summary}",
    ]

    if primary.punishment_summary:
        lines.extend(["", f"Punishment note: {primary.punishment_summary}"])

    lines.extend(
        [
            "",
            "Issue-type guidance:",
            build_category_guidance(category["key"]),
            "",
            "Confidence note:",
            build_confidence_note(confidence),
        ]
    )

    if len(records) > 1:
        lines.extend(
            [
                "",
                "Other potentially relevant matched provisions:",
            ]
        )

        for record in records[1:]:
            lines.append(build_record_reference(record))

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
    why_matched = build_why_matched(question, records)

    return ChatQueryResponse(
        answer=answer,
        citations=citations,
        disclaimer=LEGAL_DISCLAIMER,
        category=ChatCategory(
            key=detected_category["key"],
            label=detected_category["label"],
        ),
        confidence=confidence,
        why_matched=why_matched,
    )
