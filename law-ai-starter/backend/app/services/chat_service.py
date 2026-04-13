
from collections import Counter

from app.schemas.chat import (
    ChatCategory,
    ChatConfidence,
    ChatQueryResponse,
    Citation,
    MatchExplanation,
)
from app.data.officer_authority import OFFICER_AUTHORITY_DATA
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_classification_service import detect_question_category
from app.services.legal_retrieval_service import (
    build_query_signals,
    extract_section_references,
    explain_record_match,
    retrieve_scored_legal_sources,
)


LEGAL_DISCLAIMER = (
    "Law AI provides legal information for public awareness only. "
    "It does not provide legal advice, legal representation, or a substitute for a lawyer."
)

PRIMARY_KINDS = {"definition", "offence", "aggravated_offence", "general"}


OFFICER_RANK_ALIASES = {
    "sho": "sho",
    "station house officer": "sho",
    "asi": "asi",
    "assistant sub inspector": "asi",
    "assistant sub-inspector": "asi",
    "inspector": "inspector",
}


def detect_officer_rank(question: str) -> str | None:
    lower = question.strip().lower()
    for phrase, rank in OFFICER_RANK_ALIASES.items():
        if phrase in lower:
            return rank
    return None




def is_pure_officer_authority_query(question: str) -> bool:
    lower = question.strip().lower()
    rank = detect_officer_rank(question)
    if not rank:
        return False

    authority_terms = ["power", "powers", "authority", "rank", "jurisdiction", "can register fir", "officer authority"]
    procedure_terms = ["arrest", "detain", "detention", "custody", "warrant", "without warrant", "24 hours", "fir", "register fir", "complaint", "investigation"]

    return any(term in lower for term in authority_terms) and not any(term in lower for term in procedure_terms)


def build_officer_authority_note(rank_key: str) -> str | None:
    record = OFFICER_AUTHORITY_DATA.get(rank_key)
    if not record:
        return None

    lines = [
        f"Officer-rank note: {record['rank']}",
        record["summary"],
        "Typical prototype powers:",
    ]
    for power in record["powers"]:
        lines.append(f"- {power}")

    lines.append("Prototype limitations:")
    for limitation in record["limitations"]:
        lines.append(f"- {limitation}")

    return "\n".join(lines)


def build_scope_boundary_note(question: str, category_key: str) -> str | None:
    lower = question.strip().lower()
    civil_terms = [
        "civil",
        "divorce",
        "khula",
        "marriage",
        "nikah",
        "inheritance",
        "maintenance",
        "custody",
        "rent",
        "tenant",
        "landlord",
        "eviction",
        "ownership",
        "partition",
        "agreement",
        "contract",
        "debt",
        "salary",
        "employment",
    ]

    if category_key == "civil_family" or any(term in lower for term in civil_terms):
        return (
            "Current prototype scope note: the dataset is presently strongest for criminal-law, PECA, arrest/detention, "
            "and officer-authority public-awareness questions. Civil, family, tenancy, inheritance, contract, and broader "
            "property-rights coverage is still limited."
        )

    return None




def is_limited_civil_scope_query(question: str) -> bool:
    lower = question.strip().lower()
    civil_terms = [
        "civil",
        "divorce",
        "khula",
        "marriage",
        "nikah",
        "inheritance",
        "maintenance",
        "custody",
        "rent",
        "tenant",
        "landlord",
        "eviction",
        "ownership",
        "partition",
        "agreement",
        "contract",
        "debt",
        "salary",
        "employment",
    ]
    criminal_terms = [
        "theft",
        "steal",
        "fraud",
        "420",
        "threat",
        "blackmail",
        "assault",
        "slap",
        "push",
        "harassment",
        "stalking",
        "online",
        "cyber",
        "arrest",
        "warrant",
        "detention",
        "detain",
        "illegal entry",
        "trespass",
        "entered my house",
        "entered my plot",
        "damage",
        "mischief",
    ]
    return any(term in lower for term in civil_terms) and not any(term in lower for term in criminal_terms)


def build_answer_intent(question: str) -> dict[str, bool]:
    refs = extract_section_references(question)
    lower = question.strip().lower()
    punishment_focus = any(
        term in lower for term in ["punishment", "penalty", "sentence", "fine", "jail", "imprisonment", "saza"]
    )
    return {
        "section_lookup": bool(refs),
        "punishment_focus": punishment_focus,
    }


def record_matches_requested_section(question: str, record: LegalSourceRecord) -> bool:
    refs = extract_section_references(question)
    if not refs:
        return False

    law_short = ""
    if record.law_name == "Pakistan Penal Code":
        law_short = "ppc"
    elif record.law_name == "Prevention of Electronic Crimes Act":
        law_short = "peca"
    elif record.law_name == "Code of Criminal Procedure":
        law_short = "crpc"

    for law_hint, section in refs:
        if section != record.section_number.upper():
            continue
        if law_hint and law_hint != law_short:
            continue
        return True
    return False


def choose_primary_record(question: str, records: list[LegalSourceRecord]) -> LegalSourceRecord:
    intent = build_answer_intent(question)

    if intent["section_lookup"]:
        for record in records:
            if record_matches_requested_section(question, record):
                return record

    if intent["punishment_focus"]:
        for record in records:
            if record.provision_kind == "punishment":
                return record

    for record in records:
        if is_primary_record(record):
            return record

    return records[0]


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

    if top_score >= 22 and total_matches >= 2:
        level = "high"
    elif top_score >= 13:
        level = "medium"
    else:
        level = "low"

    if level == "medium" and score_gap >= 9 and top_score >= 17:
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
        "assault_force": (
            "This appears to involve assault, criminal force, slapping, pushing, hitting, or similar physical-force conduct. "
            "The system usually checks the basic assault provision first and then any more specific modesty or punishment section if the facts point there."
        ),
        "cybercrime": (
            "This appears to involve an online or digital issue. "
            "The system usually checks PECA-related provisions first, but may also surface PPC overlap where the facts include threats, fraud, or harassment."
        ),
        "trespass": (
            "This appears to involve unlawful entry, land possession, criminal trespass, or house-trespass issues. "
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
        "fir_reporting": (
            "This appears to involve FIR registration, police complaint handling, cognizable or non-cognizable procedure, or investigation powers. "
            "The system usually checks reporting and investigation provisions first, and may also surface officer-authority context where rank wording is included."
        ),
        "officer_authority": (
            "This appears to concern police rank, authority, powers, or whether a rank may act in a certain way. "
            "The system may combine structured officer-authority notes with CrPC arrest/detention provisions where the question also asks about warrant, custody, or police procedure."
        ),
        "civil_family": (
            "This appears to involve a civil, family, tenancy, inheritance, contract, or broader property-rights issue. "
            "Current prototype coverage in that area is limited, so answers should be read very cautiously and may require later dataset expansion."
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


def split_records(
    question: str,
    records: list[LegalSourceRecord],
) -> tuple[LegalSourceRecord, list[LegalSourceRecord], list[LegalSourceRecord]]:
    primary = choose_primary_record(question, records)

    exact_matches = [
        record for record in records
        if record.id != primary.id and record_matches_requested_section(question, record)
    ]

    related_matches = [
        record
        for record in records
        if record.id != primary.id
        and primary.related_sections
        and any(ref.endswith(record.section_number) for ref in primary.related_sections)
    ]

    if primary.provision_kind == "punishment":
        main_related = [record for record in related_matches if record.provision_kind != "punishment"]
        support_records = [
            record
            for record in records
            if record.id != primary.id and record not in exact_matches and record not in main_related
        ]
    else:
        main_related = [
            record for record in records
            if record.id != primary.id and record.provision_kind != "punishment"
        ]
        support_records = [
            record
            for record in records
            if record.id != primary.id and record not in exact_matches and record not in main_related
        ]

    ordered_main = exact_matches + [record for record in main_related if record not in exact_matches]
    return primary, ordered_main, support_records



def build_rephrase_suggestions(question: str, category_key: str) -> list[str]:
    signals = build_query_signals(question)
    suggestions: list[str] = []

    if signals["section_lookup"]:
        suggestions.append("Ask with both the law and section, for example: What does PPC section 448 cover?")
    if category_key == "civil_family" or signals.get("civil"):
        suggestions.append("Mention the issue type clearly, for example: tenancy dispute, inheritance share, divorce, child custody, contract breach, or salary issue.")
    if category_key == "trespass" or signals["house_context"]:
        suggestions.append("Mention whether it was a house/home entry, plot entry, or staying on property after being asked to leave.")
    if category_key == "assault_force" or signals["assault"]:
        suggestions.append("Mention whether the conduct involved slapping, pushing, hitting, grabbing, or use of force.")
    if category_key == "harassment" or signals["mentions_photo"]:
        suggestions.append("Mention whether there were repeated calls/messages, private photos, threats, or conduct involving a woman or girl.")
    if category_key == "cybercrime" or signals["online"] or signals["identity"]:
        suggestions.append("Mention whether the issue involved a fake profile, CNIC misuse, account access, digital evidence, or an online scam.")
    if category_key == "robbery_extortion" or signals["threat"]:
        suggestions.append("Mention whether property was taken, money was demanded, or force or fear was used.")
    if category_key == "officer_authority" or signals.get("officer_authority") or signals.get("officer_rank"):
        suggestions.append("Mention the rank clearly, such as SHO, ASI, or Inspector, and whether you are asking about arrest, detention, FIR handling, or general authority.")
    if category_key == "fir_reporting" or signals.get("fir") or signals.get("investigation"):
        suggestions.append("Mention whether the issue is FIR registration, refusal to register, cognizable vs non-cognizable, or police investigation after complaint.")
    if not suggestions:
        suggestions.extend(
            [
                "Use simple facts like who did what, to whom, and whether it happened online or offline.",
                "Mention whether money, property, threats, physical force, or police action were involved.",
            ]
        )

    unique: list[str] = []
    seen: set[str] = set()
    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique.append(suggestion)

    return unique[:3]


def build_no_match_answer(
    question: str,
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    suggestion_lines = "\n".join(
        f"- {suggestion}" for suggestion in build_rephrase_suggestions(question, category["key"])
    )

    section_note = ""
    if extract_section_references(question):
        section_note = "The question appears to ask about a specific section, but that exact section could not be confidently resolved from the current prototype records.\n\n"
    scope_note = build_scope_boundary_note(question, category["key"])
    scope_block = f"{scope_note}\n\n" if scope_note else ""

    return (
        "No strong legal-source match was found in the current prototype dataset.\n\n"
        f"Confidence level: {confidence.level.upper()}\n\n"
        f"{section_note}"
        f"{scope_block}"
        "What this means:\n"
        "- The system could not confidently map your question to the current internal legal records.\n"
        "- This does not mean no law applies. It only means the current prototype dataset is still limited.\n\n"
        "Issue-type guidance:\n"
        f"- {build_category_guidance(category['key'])}\n\n"
        "Try asking with clearer facts like:\n"
        f"{suggestion_lines}\n\n"
        "Useful example terms currently covered in the prototype include:\n"
        "- theft\n"
        "- cheating or 420\n"
        "- criminal breach of trust\n"
        "- arrest without warrant\n"
        "- detention for 24 hours\n"
        "- criminal intimidation\n"
        "- defamation\n"
        "- assault or slapping / pushing\n"
        "- house-trespass or illegal home entry\n"
        "- sexual harassment or cyber stalking\n"
        "- criminal trespass\n"
        "- property damage / mischief\n"
        "- misuse of CNIC or fake profile\n"
        "- a specific section number\n\n"
        f'Your question was: "{question.strip()}"'
    )


def build_weak_match_answer(
    question: str,
    records: list[LegalSourceRecord],
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    section_note = build_specific_section_note(question, records)
    unresolved_section_note = build_unresolved_section_note(question, records)
    scope_note = build_scope_boundary_note(question, category["key"])
    lines = [
        "Closest currently available legal information",
        "",
        f"Confidence level: {confidence.level.upper()}",
        "",
        "The prototype found only a weak or partial match for this wording.",
        "That means the sections below are the nearest current records, but they may not fully capture the facts as asked.",
        "",
        "Closest prototype sections:",
    ]

    if section_note:
        lines.extend(["", "Section-note guidance:", section_note])
    elif unresolved_section_note:
        lines.extend(["", "Section-note guidance:", unresolved_section_note])

    if scope_note:
        lines.extend(["", "Scope note:", scope_note])

    for record in records[:3]:
        lines.append(build_record_reference(record))

    lines.extend(
        [
            "",
            "Issue-type guidance:",
            build_category_guidance(category["key"]),
            "",
            "Try rephrasing with clearer facts:",
        ]
    )

    for suggestion in build_rephrase_suggestions(question, category["key"]):
        lines.append(f"- {suggestion}")

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


def build_specific_section_note(question: str, records: list[LegalSourceRecord]) -> str | None:
    refs = extract_section_references(question)
    if not refs or not records:
        return None

    matched_sections = {record.section_number.upper() for record in records}
    requested = [section for _, section in refs]
    if any(section in matched_sections for section in requested):
        return (
            "The query appears to ask about a specific section number, so the system prioritized that exact section first and then added closely linked provisions."
        )

    return None


def build_unresolved_section_note(question: str, records: list[LegalSourceRecord]) -> str | None:
    refs = extract_section_references(question)
    if not refs:
        return None

    requested = {section for _, section in refs}
    matched_sections = {record.section_number.upper() for record in records}
    if requested & matched_sections:
        return None

    requested_list = ", ".join(sorted(requested))
    return (
        f"The query appears to ask about section {requested_list}, but that exact section was not confidently resolved in the current prototype dataset. "
        "The answer below is therefore only a best-effort match using the closest available records."
    )


def build_match_answer(
    question: str,
    records: list[LegalSourceRecord],
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    primary, main_related_records, support_records = split_records(question, records)
    intent = build_answer_intent(question)
    scope_note = build_scope_boundary_note(question, category["key"])
    officer_rank = detect_officer_rank(question)
    officer_note = build_officer_authority_note(officer_rank) if officer_rank else None

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
        ("Requested section" if intent["section_lookup"] else ("Primary punishment provision" if intent["punishment_focus"] and primary.provision_kind == "punishment" else "Primary matched provision")) + ":",
        build_record_reference(primary),
    ]

    if primary.punishment_summary and primary.provision_kind != "punishment":
        lines.extend(["", f"Primary punishment note: {primary.punishment_summary}"])

    section_note = build_specific_section_note(question, records)
    unresolved_section_note = build_unresolved_section_note(question, records)
    if section_note:
        lines.extend(["", "Section-note guidance:", section_note])
    elif unresolved_section_note:
        lines.extend(["", "Section-note guidance:", unresolved_section_note])

    if officer_note and (category["key"] in {"officer_authority", "fir_reporting"} or "police" in question.lower() or "arrest" in question.lower() or "warrant" in question.lower() or "detain" in question.lower() or "detention" in question.lower() or "custody" in question.lower() or "fir" in question.lower() or "complaint" in question.lower()):
        lines.extend(["", officer_note])

    if scope_note:
        lines.extend(["", "Scope note:", scope_note])

    overlap_note = summarize_overlap(records)
    if overlap_note:
        lines.extend(["", "Overlap note:", overlap_note])

    if main_related_records:
        lines.extend(["", "Other main provisions that may also matter:"])
        for record in main_related_records:
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



def build_officer_only_answer(
    question: str,
    category: dict[str, str],
    confidence: ChatConfidence,
    rank_key: str,
) -> str:
    officer_note = build_officer_authority_note(rank_key)
    scope_note = build_scope_boundary_note(question, category["key"])

    lines = [
        "Matched legal-information note",
        "",
        f"Confidence level: {confidence.level.upper()}",
        "",
    ]

    if officer_note:
        lines.extend([officer_note, ""])

    lines.extend(
        [
            "Issue-type guidance:",
            build_category_guidance(category["key"]),
        ]
    )

    if scope_note:
        lines.extend(["", "Scope note:", scope_note])

    lines.extend(
        [
            "",
            "Current prototype note:",
            "This officer-rank response comes from the prototype's structured officer-authority records and is general legal information only.",
        ]
    )
    return "\n".join(lines)


def build_officer_why_matched(rank_key: str) -> list[MatchExplanation]:
    record = OFFICER_AUTHORITY_DATA.get(rank_key)
    if not record:
        return []

    return [
        MatchExplanation(
            title=f"{record['rank']} — Officer authority prototype record",
            points=[
                f"Direct police-rank mention matched: {record['rank']}.",
                "The question was routed to structured officer-authority data.",
                "Officer authority notes remain subject to procedural law and legal limits.",
            ],
        )
    ]


def build_officer_citations(rank_key: str) -> list[Citation]:
    record = OFFICER_AUTHORITY_DATA.get(rank_key)
    if not record:
        return []

    return [
        Citation(
            title="Officer Authority Prototype",
            section=record["rank"],
            note="Structured rank summary and authority limitations",
            excerpt=record["summary"],
        )
    ]


def build_answer(
    question: str,
    scored_records: list[tuple[int, LegalSourceRecord]],
    records: list[LegalSourceRecord],
    category: dict[str, str],
    confidence: ChatConfidence,
) -> str:
    rank_key = detect_officer_rank(question)
    if is_pure_officer_authority_query(question) and rank_key:
        return build_officer_only_answer(
            question,
            {"key": "officer_authority", "label": "Police Rank / Officer Authority"},
            confidence,
            rank_key,
        )

    if not records:
        if category["key"] == "officer_authority" and rank_key:
            return build_officer_only_answer(question, category, confidence, rank_key)
        return build_no_match_answer(question, category, confidence)

    if confidence.level == "low" and scored_records and scored_records[0][0] < 8:
        return build_weak_match_answer(question, records, category, confidence)

    return build_match_answer(question, records, category, confidence)


def generate_mock_legal_response(question: str) -> ChatQueryResponse:
    scored_records = retrieve_scored_legal_sources(question, limit=4)
    records = [record for _, record in scored_records]

    detected_category = detect_question_category(question, records)
    confidence = determine_confidence(scored_records)
    officer_rank = detect_officer_rank(question)

    if is_pure_officer_authority_query(question) and officer_rank:
        detected_category = {
            "key": "officer_authority",
            "label": "Police Rank / Officer Authority",
        }

    if is_limited_civil_scope_query(question) and (not scored_records or scored_records[0][0] < 18):
        scored_records = []
        records = []
        confidence = ChatConfidence(level="low", score=0, matched_records=0)
        detected_category = {
            "key": "civil_family",
            "label": "Civil / Family / Property / Contract (Limited Prototype Coverage)",
        }

    answer = build_answer(question, scored_records, records, detected_category, confidence)

    if (not records and detected_category["key"] == "officer_authority" and officer_rank) or is_pure_officer_authority_query(question):
        citations = build_officer_citations(officer_rank) if officer_rank else []
        why_matched = build_officer_why_matched(officer_rank) if officer_rank else []
    else:
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
