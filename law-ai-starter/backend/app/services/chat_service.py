from collections import Counter

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

PRIMARY_KINDS = {"definition", "offence", "aggravated_offence", "general"}


def build_citations(records: list[LegalSourceRecord]) -> list[Citation]:
    seen: set[tuple[str, str, str]] = set()
    citations: list[Citation] = []

    for record in records:
        key = (record.law_name, record.section_number, record.section_title)
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            Citation(
                title=record.law_name,
                section=record.section_number,
                note=record.section_title,
                excerpt=record.excerpt,
            )
        )

    return citations



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

    for record in records[:4]:
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
            "The system usually checks the main theft section first and then any linked punishment provision."
        ),
        "cheating_fraud": (
            "This appears to involve cheating, fraud, dishonest inducement, or criminal breach of trust. "
            "The system usually checks the offence-defining section first and then linked punishment or overlap sections."
        ),
        "robbery_extortion": (
            "This appears to involve robbery, extortion, force-based snatching, or fear-based delivery of property. "
            "The system usually checks the violent-property provision first and then related punishment or threat sections."
        ),
        "criminal_intimidation": (
            "This appears to involve a threat, intimidation, or pressure-related issue. "
            "The system may also surface overlap with cyber-stalking or extortion provisions where the facts point that way."
        ),
        "defamation": (
            "This appears to involve reputation harm, false statements, or defamation-related issues. "
            "The system usually checks the main defamation provision and then the punishment provision."
        ),
        "harassment": (
            "This appears to involve harassment, stalking, insulting modesty, privacy intrusion, or related conduct. "
            "Depending on the facts, both PPC and PECA provisions may become relevant at the same time."
        ),
        "cybercrime": (
            "This appears to involve an online or digital issue. "
            "The system usually checks PECA-related provisions first, but may also surface PPC overlap where the facts include threats, fraud, or harassment."
        ),
        "trespass": (
            "This appears to involve unlawful entry, land possession, or criminal-trespass issues. "
            "The system may also surface property-damage overlap if the facts mention breaking or damaging property."
        ),
        "restraint_confinement": (
            "This appears to involve a person being blocked, stopped, confined, or prevented from leaving a place. "
            "The system usually checks wrongful-restraint or wrongful-confinement provisions and their punishment sections."
        ),
        "property_damage": (
            "This appears to involve property damage, destruction, or vandalism. "
            "The system usually checks the mischief provision and the linked punishment section."
        ),
        "arrest_detention": (
            "This appears to involve arrest, detention, custody, or police procedure. "
            "The system usually checks criminal-procedure provisions such as manner of arrest, warrant rules, and detention limits."
        ),
        "officer_authority": (
            "This appears to concern police rank, authority, or powers. "
            "The system usually checks structured officer-authority records rather than only offence provisions."
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



def is_primary_record(record: LegalSourceRecord) -> bool:
    return record.provision_kind in PRIMARY_KINDS



def build_record_reference(record: LegalSourceRecord) -> str:
    lines = [
        f"- {record.citation_label}",
        f"  Law: {record.law_name}",
        f"  Section title: {record.section_title}",
    ]

    if record.summary:
        lines.append(f"  Summary: {record.summary}")

    if record.punishment_summary:
        lines.append(f"  Punishment note: {record.punishment_summary}")

    if record.related_sections:
        lines.append(f"  Related sections: {', '.join(record.related_sections[:3])}")

    return "\n".join(lines)



def summarize_overlap(records: list[LegalSourceRecord]) -> str | None:
    if len(records) < 2:
        return None

    law_names = {record.law_name for record in records}
    offence_groups = [record.offence_group for record in records if record.offence_group]
    distinct_groups = set(offence_groups)

    if len(law_names) > 1:
        if "Prevention of Electronic Crimes Act" in law_names and "Pakistan Penal Code" in law_names:
            return (
                "The facts may engage overlapping PPC and PECA provisions in the current prototype, "
                "so both traditional criminal-law and cyber-law sections are being surfaced together."
            )
        return (
            "The current prototype found relevant sections from more than one law, which suggests an overlap issue rather than a single isolated section."
        )

    if len(distinct_groups) > 1:
        common_groups = Counter(offence_groups).most_common(2)
        group_names = ", ".join(group for group, _ in common_groups if group)
        return (
            "The current prototype found more than one offence pattern in the question. "
            f"The strongest overlap clusters were: {group_names}."
        )

    return None



def split_records(records: list[LegalSourceRecord]) -> tuple[list[LegalSourceRecord], list[LegalSourceRecord]]:
    primary_records = [record for record in records if is_primary_record(record)]
    support_records = [record for record in records if record not in primary_records]

    if not primary_records and records:
        primary_records = [records[0]]
        support_records = records[1:]

    return primary_records, support_records



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
        "- misuse of CNIC or fake profile\n"
        "- a specific section number\n\n"
        f'Your question was: "{question.strip()}"'
    )



def build_match_answer(
    records: list[LegalSourceRecord],
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    primary_records, support_records = split_records(records)
    primary = primary_records[0]

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
    ]

    if primary.punishment_summary:
        lines.extend(["", f"Primary punishment note: {primary.punishment_summary}"])

    overlap_note = summarize_overlap(records)
    if overlap_note:
        lines.extend(["", "Overlap note:", overlap_note])

    if len(primary_records) > 1:
        lines.extend(["", "Other main provisions that may also matter:"])
        for record in primary_records[1:]:
            lines.append(build_record_reference(record))

    if support_records:
        lines.extend(["", "Supporting or linked provisions:"])
        for record in support_records:
            lines.append(build_record_reference(record))

    lines.extend(
        [
            "",
            "Issue-type guidance:",
            build_category_guidance(category["key"]),
            "",
            "Confidence note:",
            build_confidence_note(confidence),
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
    scored_records = retrieve_scored_legal_sources(question, limit=4)
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
