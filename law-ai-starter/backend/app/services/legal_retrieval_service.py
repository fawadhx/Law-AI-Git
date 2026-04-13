import re
from collections import defaultdict

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
        "take",
        "took",
        "taken",
        "without permission",
        "mobile",
        "phone",
    ],
    "punishment": [
        "punishment",
        "penalty",
        "sentence",
        "fine",
        "imprisonment",
        "jail",
        "saza",
    ],
    "threat": [
        "threat",
        "threaten",
        "threatened",
        "threatening",
        "intimidation",
        "criminal intimidation",
        "alarm",
        "blackmail",
    ],
    "defamation": [
        "defamation",
        "defame",
        "reputation",
        "false statement",
        "badnami",
        "false allegation",
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
        "tiktok",
    ],
    "privacy": [
        "privacy",
        "private",
        "personal data",
        "personal information",
        "private photos",
    ],
    "modesty": [
        "modesty",
        "image misuse",
        "photo misuse",
        "explicit image",
        "video misuse",
        "minor",
        "child",
        "harassment",
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
        "login access",
    ],
    "cheating": [
        "cheating",
        "cheated",
        "fraud",
        "fraudulent",
        "scam",
        "deception",
        "dishonest inducement",
        "property deal",
        "420",
        "dhoka",
    ],
    "breach_of_trust": [
        "criminal breach of trust",
        "breach of trust",
        "entrusted property",
        "misappropriation",
        "amanat",
        "khayanat",
    ],
    "trespass": [
        "trespass",
        "criminal trespass",
        "illegal entry",
        "unlawful entry",
        "land dispute",
        "property entry",
        "qabza",
        "entered",
        "enter",
        "plot",
        "leave",
    ],
    "harassment": [
        "harassment",
        "sexual harassment",
        "stalking",
        "cyber stalking",
        "insult modesty",
        "privacy intrusion",
        "eve teasing",
    ],
    "extortion": [
        "extortion",
        "bhatta",
        "ransom",
        "money demand",
        "fear of injury",
        "demanded money",
        "demanded money by threat",
        "blackmail for money",
    ],
    "robbery": [
        "robbery",
        "mugging",
        "armed snatching",
        "snatching with force",
        "gunpoint",
        "violent theft",
        "street robbery",
        "snatched at gunpoint",
        "snatched with force",
    ],
    "restraint": [
        "wrongful restraint",
        "blocked way",
        "prevented from going",
        "stopped me from leaving",
        "obstructed",
        "rasta rokna",
    ],
    "confinement": [
        "wrongful confinement",
        "locked in",
        "kept inside",
        "confined",
        "locked me in a room",
        "band kar diya",
    ],
    "mischief": [
        "mischief",
        "property damage",
        "vandalism",
        "damage property",
        "damaged",
        "broke",
        "destroyed",
        "car",
        "vehicle",
        "tod phod",
    ],
    "identity": [
        "identity information",
        "identity theft",
        "cnic",
        "impersonation",
        "my identity",
        "my documents",
        "fake profile",
    ],
    "electronic_forgery": [
        "electronic forgery",
        "fake digital document",
        "forged screenshot",
        "fake pdf",
        "edited digital evidence",
    ],
    "electronic_fraud": [
        "electronic fraud",
        "online scam",
        "digital scam",
        "banking scam",
        "fake website",
        "wrongful gain online",
        "otp scam",
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
    "online harassment": ["online", "privacy", "harassment"],
    "social media post": ["online", "defamation"],
    "without warrant": ["arrest", "police"],
    "24 hours": ["detention", "arrest"],
    "reputation harm": ["defamation", "privacy"],
    "image misuse": ["modesty", "online"],
    "minor online": ["modesty", "online"],
    "hacked account": ["unauthorized_access", "online"],
    "property fraud": ["cheating", "breach_of_trust"],
    "entrusted money": ["breach_of_trust", "cheating"],
    "land entry": ["trespass"],
    "sexual harassment": ["harassment", "modesty"],
    "cyber stalking": ["harassment", "online", "threat"],
    "money through threats": ["extortion", "threat"],
    "snatched at gunpoint": ["robbery", "theft", "threat"],
    "blocked my way": ["restraint"],
    "locked me inside": ["confinement"],
    "damaged my property": ["mischief"],
    "used my cnic": ["identity", "electronic_fraud"],
    "fake digital document": ["electronic_forgery", "identity"],
    "online scam": ["electronic_fraud", "online", "identity"],
    "otp scam": ["electronic_fraud", "identity", "online"],
    "fake profile": ["identity", "online", "harassment"],
    "blackmail online": ["threat", "online", "harassment"],
}


PUNISHMENT_HINTS = ["punishment", "penalty", "sentence", "fine", "jail", "imprisonment", "saza"]
ONLINE_HINTS = ["online", "internet", "cyber", "social media", "facebook", "instagram", "whatsapp", "tiktok"]
POLICE_HINTS = ["police", "arrest", "detain", "custody", "warrant"]
PROPERTY_HINTS = ["property", "money", "land", "plot", "phone", "wallet", "entrusted"]
FRAUD_HINTS = ["cheat", "cheated", "cheating", "fraud", "scam", "deceive", "deceived", "deal", "property deal", "420", "trust", "entrusted", "amanat", "khayanat"]
TRESPASS_HINTS = ["trespass", "illegal entry", "unlawful entry", "plot", "entered", "enter", "land", "leave"]
EXTORTION_HINTS = ["extortion", "bhatta", "ransom", "money demand", "demanded money", "demanded money by threat", "blackmail for money", "fear of injury"]
ROBBERY_HINTS = ["robbery", "mugging", "gunpoint", "armed snatching", "snatching with force", "snatched at gunpoint", "violent theft"]
RESTRAINT_HINTS = ["wrongful restraint", "blocked way", "obstruct", "rasta", "prevented from going", "stopped me"]
CONFINEMENT_HINTS = ["wrongful confinement", "locked in", "kept inside", "confined", "locked room", "band"]
MISCHIEF_HINTS = ["mischief", "vandalism", "property damage", "damaged", "broke", "destroyed", "damage car", "damage bike", "car windows", "vehicle damage"]
IDENTITY_HINTS = ["identity", "identity theft", "cnic", "impersonation", "fake profile", "my documents"]
ELECTRONIC_FRAUD_HINTS = ["electronic fraud", "online scam", "digital scam", "fake website", "banking scam", "otp"]
ELECTRONIC_FORGERY_HINTS = ["electronic forgery", "fake screenshot", "forged pdf", "edited digital evidence", "fake digital document"]
THREAT_HINTS = ["threat", "threaten", "intimidation", "blackmail", "alarm"]
HARASSMENT_HINTS = ["harassment", "stalking", "modesty", "privacy intrusion", "unwanted contact"]
FORCE_HINTS = ["force", "gunpoint", "weapon", "armed", "violence"]


PRIMARY_KINDS = {"definition", "offence", "aggravated_offence", "general"}


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



def build_query_signals(query: str) -> dict[str, bool]:
    query_lower = normalize_text(query)
    return {
        "punishment": any(word in query_lower for word in PUNISHMENT_HINTS),
        "online": any(phrase in query_lower for phrase in ONLINE_HINTS),
        "police": any(word in query_lower for word in POLICE_HINTS),
        "property": any(word in query_lower for word in PROPERTY_HINTS),
        "fraud": any(word in query_lower for word in FRAUD_HINTS),
        "trespass": any(word in query_lower for word in TRESPASS_HINTS),
        "extortion": any(word in query_lower for word in EXTORTION_HINTS),
        "robbery": any(word in query_lower for word in ROBBERY_HINTS),
        "restraint": any(word in query_lower for word in RESTRAINT_HINTS),
        "confinement": any(word in query_lower for word in CONFINEMENT_HINTS),
        "mischief": any(word in query_lower for word in MISCHIEF_HINTS),
        "identity": any(word in query_lower for word in IDENTITY_HINTS),
        "electronic_fraud": any(word in query_lower for word in ELECTRONIC_FRAUD_HINTS),
        "electronic_forgery": any(word in query_lower for word in ELECTRONIC_FORGERY_HINTS),
        "threat": any(word in query_lower for word in THREAT_HINTS),
        "harassment": any(word in query_lower for word in HARASSMENT_HINTS),
        "force": any(word in query_lower for word in FORCE_HINTS),
        "mentions_money": "money" in query_lower,
    }



def score_record(query: str, record: LegalSourceRecord) -> int:
    query_lower = normalize_text(query)
    query_terms = expand_query_terms(query)
    signals = build_query_signals(query)

    searchable_text = normalize_text(" ".join(record.searchable_parts))
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

    section_title = normalize_text(record.section_title)
    law_name = normalize_text(record.law_name)
    citation_label = normalize_text(record.citation_label)

    if section_title and section_title in query_lower:
        score += 6

    if law_name and law_name in query_lower:
        score += 4

    if citation_label and citation_label in query_lower:
        score += 5

    for tag in record.tags + record.aliases + record.keywords:
        tag_normalized = normalize_text(tag)
        if tag_normalized and tag_normalized in query_lower:
            score += 3

    if record.section_number and record.section_number in query_lower:
        score += 3

    if signals["punishment"] and record.provision_kind == "punishment":
        score += 5
    elif signals["punishment"] and record.punishment_summary:
        score += 2

    if signals["online"] and record.law_name == "Prevention of Electronic Crimes Act":
        score += 4

    if signals["police"] and record.law_name == "Code of Criminal Procedure":
        score += 4
    elif not signals["police"] and record.offence_group == "criminal_procedure":
        score -= 4

    if signals["property"] and record.offence_group == "property_offence":
        score += 2

    if signals["fraud"] and record.offence_group == "fraud_offence":
        score += 4

    if signals["fraud"] and record.section_number in {"415", "417", "420"}:
        score += 5

    if signals["trespass"] and (record.section_number in {"441", "447"} or record.offence_group == "property_offence"):
        score += 4

    if signals["extortion"] and record.offence_group == "violent_property_offence":
        score += 5

    if signals["robbery"] and record.offence_group == "violent_property_offence":
        score += 6

    if signals["restraint"] and not signals["police"] and record.offence_group == "restraint_offence":
        score += 5

    if signals["confinement"] and not signals["police"] and record.offence_group == "restraint_offence":
        score += 6

    if signals["mischief"] and record.offence_group == "property_damage_offence":
        score += 6

    if signals["identity"] and record.offence_group == "cyber_identity_offence":
        score += 6

    if signals["electronic_fraud"] and record.section_number == "14":
        score += 8
    elif signals["electronic_fraud"] and record.offence_group == "cyber_identity_offence":
        score += 5

    if signals["electronic_forgery"] and record.section_number == "13":
        score += 8
    elif signals["electronic_forgery"] and record.offence_group == "cyber_identity_offence":
        score += 5

    if signals["force"] and record.offence_group == "violent_property_offence":
        score += 5

    if signals["threat"] and signals["online"] and record.section_number in {"24", "503", "506"}:
        score += 5

    if signals["harassment"] and signals["online"] and record.section_number in {"24", "509", "20", "21"}:
        score += 6

    if signals["harassment"] and not signals["online"] and record.section_number == "509":
        score += 5

    if signals["identity"] and signals["fraud"] and record.section_number in {"14", "16", "420"}:
        score += 5

    if signals["identity"] and signals["online"] and record.section_number in {"16", "14", "13"}:
        score += 6

    if signals["online"] and signals["threat"] and record.offence_group == "threat_offence":
        score += 3

    if signals["online"] and signals["harassment"] and record.offence_group == "harassment_offence":
        score += 3

    if signals["mentions_money"] and signals["threat"] and record.section_number == "383":
        score += 8

    if signals["mentions_money"] and signals["threat"] and record.section_number == "503":
        score += 4

    if "420" in query_lower and record.section_number == "420":
        score += 6

    if "509" in query_lower and record.section_number == "509":
        score += 6

    if "24" in query_lower and "cyber stalking" in query_lower and record.section_number == "24":
        score += 8
    elif "cyber stalking" in query_lower and record.section_number == "24":
        score += 8

    if "16" in query_lower and "identity" in query_lower and record.section_number == "16":
        score += 8

    if "13" in query_lower and "forgery" in query_lower and record.section_number == "13":
        score += 8

    if "14" in query_lower and "fraud" in query_lower and record.section_number == "14":
        score += 8

    if "392" in query_lower and record.section_number == "392":
        score += 8

    if "384" in query_lower and record.section_number == "384":
        score += 8

    if "341" in query_lower and record.section_number == "341":
        score += 7

    if "342" in query_lower and record.section_number == "342":
        score += 7

    if "426" in query_lower and record.section_number == "426":
        score += 7

    if not signals["online"] and record.law_name == "Prevention of Electronic Crimes Act":
        score -= 4

    if not signals["harassment"] and not signals["online"] and record.offence_group == "harassment_offence":
        score -= 4

    if not signals["online"] and not signals["identity"] and record.offence_group == "cyber_identity_offence":
        score -= 3

    if signals["restraint"] and not signals["robbery"] and not signals["extortion"] and record.offence_group == "violent_property_offence":
        score -= 3

    if (signals["restraint"] or signals["confinement"]) and record.offence_group == "criminal_procedure":
        score -= 5

    if signals["mischief"] and record.offence_group == "cyber_identity_offence":
        score -= 4

    if signals["force"] and record.offence_group == "property_offence":
        score -= 2

    if signals["fraud"] and not signals["force"] and record.offence_group == "property_offence":
        score -= 3

    if signals["online"] and not signals["identity"] and record.offence_group == "property_damage_offence":
        score -= 2

    if "without permission" in query_lower and record.section_number == "378":
        score += 5

    if "gunpoint" in query_lower and record.section_number == "390":
        score += 7

    if "snatched" in query_lower and "gunpoint" in query_lower and record.section_number == "390":
        score += 8

    if "bhatta" in query_lower and record.section_number == "383":
        score += 7

    if "demanded money" in query_lower and record.section_number == "383":
        score += 8

    if "cnic" in query_lower and record.section_number == "16":
        score += 8

    if "car" in query_lower and "damaged" in query_lower and record.section_number == "425":
        score += 7

    if "fake profile" in query_lower and record.section_number in {"16", "24", "20"}:
        score += 7

    if "blackmail online" in query_lower and record.section_number in {"24", "503", "506"}:
        score += 7

    return score



def citation_reference(record: LegalSourceRecord) -> str:
    return normalize_text(record.citation_label)



def is_primary_record(record: LegalSourceRecord) -> bool:
    return record.provision_kind in PRIMARY_KINDS



def record_reference_matches(reference: str, record: LegalSourceRecord) -> bool:
    ref = normalize_text(reference)
    if not ref:
        return False

    candidates = {
        normalize_text(record.citation_label),
        normalize_text(f"{record.law_name} section {record.section_number}"),
        normalize_text(f"section {record.section_number}"),
    }
    return ref in candidates or any(candidate in ref or ref in candidate for candidate in candidates)



def find_linked_records(
    anchor: LegalSourceRecord,
    scored_results: list[tuple[int, LegalSourceRecord]],
) -> list[tuple[int, LegalSourceRecord]]:
    linked: list[tuple[int, LegalSourceRecord]] = []
    related_refs = anchor.related_sections or []

    for score, record in scored_results:
        if record.id == anchor.id:
            continue
        if any(record_reference_matches(reference, record) for reference in related_refs):
            linked.append((score, record))

    if linked:
        return linked

    for score, record in scored_results:
        if record.id == anchor.id:
            continue
        if anchor.offence_group and anchor.offence_group == record.offence_group:
            if anchor.provision_kind == "punishment" and is_primary_record(record):
                linked.append((score, record))
            elif record.provision_kind == "punishment":
                linked.append((score, record))

    return linked



def should_include_overlap(
    primary_record: LegalSourceRecord,
    candidate_record: LegalSourceRecord,
    candidate_score: int,
    top_score: int,
    query: str,
) -> bool:
    query_lower = normalize_text(query)
    signals = build_query_signals(query)

    if candidate_record.id == primary_record.id:
        return False

    if candidate_record.offence_group == primary_record.offence_group and candidate_record.law_name == primary_record.law_name:
        return False

    if candidate_score < max(8, top_score - 7):
        return False

    if signals["online"] and signals["threat"]:
        return candidate_record.section_number in {"24", "503", "506"}

    if signals["online"] and signals["harassment"]:
        return candidate_record.section_number in {"24", "509", "20", "21"}

    if signals["identity"] and (signals["fraud"] or signals["electronic_forgery"] or signals["electronic_fraud"]):
        return candidate_record.section_number in {"13", "14", "16", "420"}

    if signals["robbery"] and signals["threat"]:
        return candidate_record.section_number in {"390", "392", "503", "506", "383", "384"}

    if signals["trespass"] and signals["mischief"]:
        return candidate_record.section_number in {"441", "447", "425", "426"}

    if signals["harassment"] and "privacy" in query_lower:
        return candidate_record.section_number in {"509", "20", "24"}

    if candidate_record.law_name != primary_record.law_name:
        return True

    return candidate_record.offence_group != primary_record.offence_group



def select_contextual_records(
    query: str,
    scored_results: list[tuple[int, LegalSourceRecord]],
    limit: int,
) -> list[tuple[int, LegalSourceRecord]]:
    if not scored_results:
        return []

    top_score, primary = scored_results[0]
    signals = build_query_signals(query)
    selected: list[tuple[int, LegalSourceRecord]] = [(top_score, primary)]
    selected_ids = {primary.id}

    linked_records = sorted(
        find_linked_records(primary, scored_results),
        key=lambda item: (
            1 if item[1].provision_kind == "punishment" else 0,
            item[0],
        ),
        reverse=True,
    )

    for item in linked_records:
        if len(selected) >= limit:
            break
        score, record = item
        if record.id in selected_ids:
            continue
        if signals["punishment"] or record.provision_kind == "punishment" or record.law_name != primary.law_name:
            selected.append(item)
            selected_ids.add(record.id)
            break

    overlap_candidates = [
        item
        for item in scored_results[1:]
        if item[1].id not in selected_ids
        and should_include_overlap(primary, item[1], item[0], top_score, query)
    ]

    overlap_candidates.sort(
        key=lambda item: (
            item[0],
            1 if is_primary_record(item[1]) else 0,
            item[1].law_name,
        ),
        reverse=True,
    )

    for score, record in overlap_candidates:
        if len(selected) >= limit:
            break
        selected.append((score, record))
        selected_ids.add(record.id)

        overlap_linked = find_linked_records(record, scored_results)
        for linked_score, linked_record in overlap_linked:
            if len(selected) >= limit:
                break
            if linked_record.id in selected_ids:
                continue
            if linked_record.provision_kind == "punishment" or signals["punishment"]:
                selected.append((linked_score, linked_record))
                selected_ids.add(linked_record.id)
                break
        if len(selected) >= limit:
            break

    minimum_fill_score = max(6, top_score - 10)
    for score, record in scored_results[1:]:
        if len(selected) >= limit:
            break
        if record.id in selected_ids or score < minimum_fill_score:
            continue
        selected.append((score, record))
        selected_ids.add(record.id)

    return selected[:limit]



def retrieve_scored_legal_sources(query: str, limit: int = 4) -> list[tuple[int, LegalSourceRecord]]:
    all_results: list[tuple[int, LegalSourceRecord]] = []

    for record in LEGAL_SOURCES:
        score = score_record(query, record)
        if score > 0:
            all_results.append((score, record))

    all_results.sort(
        key=lambda item: (
            item[0],
            1 if is_primary_record(item[1]) else 0,
            item[1].law_name,
            item[1].section_number,
        ),
        reverse=True,
    )

    return select_contextual_records(query, all_results, limit)



def retrieve_legal_sources(query: str, limit: int = 4) -> list[LegalSourceRecord]:
    return [record for _, record in retrieve_scored_legal_sources(query, limit=limit)]



def explain_record_match(query: str, record: LegalSourceRecord) -> list[str]:
    query_lower = normalize_text(query)
    searchable_text = normalize_text(" ".join(record.searchable_parts))
    signals = build_query_signals(query)

    reasons: list[str] = []

    if normalize_text(record.section_title) in query_lower:
        reasons.append(f"Direct match with section title: {record.section_title}.")

    if normalize_text(record.law_name) in query_lower:
        reasons.append(f"Direct mention of law name: {record.law_name}.")

    if record.section_number and record.section_number in query_lower:
        reasons.append(f"Section number {record.section_number} was mentioned in the query.")

    matched_tags = [
        tag for tag in (record.tags + record.aliases + record.keywords)
        if normalize_text(tag) in query_lower
    ]
    if matched_tags:
        reasons.append(f"Matched legal tags or aliases: {', '.join(matched_tags[:3])}.")

    expanded_terms = expand_query_terms(query)
    concept_hits = []
    for term in expanded_terms:
        if len(term) >= 4 and term in searchable_text:
            concept_hits.append(term)

    unique_hits: list[str] = []
    seen: set[str] = set()
    for hit in concept_hits:
        if hit not in seen:
            seen.add(hit)
            unique_hits.append(hit)

    if unique_hits:
        reasons.append(
            f"Conceptual keyword overlap found: {', '.join(unique_hits[:4])}."
        )

    if signals["punishment"] and record.provision_kind == "punishment":
        reasons.append("Punishment-related wording in the question aligns with this provision.")

    if signals["online"] and record.law_name == "Prevention of Electronic Crimes Act":
        reasons.append("Online or cyber wording in the question aligns with PECA-related provisions.")

    if signals["police"] and record.law_name == "Code of Criminal Procedure":
        reasons.append("Police or detention wording in the question aligns with criminal-procedure provisions.")

    if signals["online"] and signals["threat"] and record.section_number in {"24", "503", "506"}:
        reasons.append("The query combines online and threat signals, which can overlap across PECA and PPC provisions.")

    if signals["identity"] and (signals["fraud"] or signals["electronic_forgery"] or signals["electronic_fraud"]) and record.section_number in {"13", "14", "16", "420"}:
        reasons.append("The query combines identity misuse with fraud or forgery wording, so overlapping cyber-fraud provisions were considered.")

    if record.related_sections:
        reasons.append(f"This record also links to related sections: {', '.join(record.related_sections[:2])}.")

    if not reasons:
        reasons.append("The prototype found a general text similarity with this record.")

    return reasons[:4]
