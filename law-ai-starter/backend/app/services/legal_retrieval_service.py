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
        "fraud",
        "fraudulent",
        "scam",
        "deception",
        "dishonest inducement",
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
}


PUNISHMENT_HINTS = ["punishment", "penalty", "sentence", "fine", "jail", "imprisonment", "saza"]
ONLINE_HINTS = ["online", "internet", "cyber", "social media", "facebook", "instagram", "whatsapp", "tiktok"]
POLICE_HINTS = ["police", "arrest", "detain", "custody", "warrant"]
PROPERTY_HINTS = ["property", "money", "land", "plot", "phone", "wallet", "entrusted"]
FRAUD_HINTS = ["cheat", "cheating", "fraud", "scam", "deceive", "deceived", "420", "trust", "entrusted", "amanat", "khayanat"]
TRESPASS_HINTS = ["trespass", "illegal entry", "unlawful entry", "plot", "entered", "enter", "land", "leave"]
EXTORTION_HINTS = ["extortion", "bhatta", "ransom", "money demand", "demanded money", "demanded money by threat", "blackmail for money", "fear of injury"]
ROBBERY_HINTS = ["robbery", "mugging", "gunpoint", "armed snatching", "snatching with force", "snatched at gunpoint", "violent theft"]
RESTRAINT_HINTS = ["wrongful restraint", "blocked way", "obstruct", "rasta", "prevented from going", "stopped me"]
CONFINEMENT_HINTS = ["wrongful confinement", "locked in", "kept inside", "confined", "locked room", "band"]
MISCHIEF_HINTS = ["mischief", "vandalism", "property damage", "damaged", "broke", "destroyed", "damage car", "damage bike", "car windows", "vehicle damage"]
IDENTITY_HINTS = ["identity", "identity theft", "cnic", "impersonation", "fake profile", "my documents"]
ELECTRONIC_FRAUD_HINTS = ["electronic fraud", "online scam", "digital scam", "fake website", "banking scam", "otp"]
ELECTRONIC_FORGERY_HINTS = ["electronic forgery", "fake screenshot", "forged pdf", "edited digital evidence", "fake digital document"]


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

    punishment_requested = any(word in query_lower for word in PUNISHMENT_HINTS)
    if punishment_requested and record.provision_kind == "punishment":
        score += 5
    elif punishment_requested and record.punishment_summary:
        score += 2

    online_requested = any(phrase in query_lower for phrase in ONLINE_HINTS)
    if online_requested and record.law_name == "Prevention of Electronic Crimes Act":
        score += 4

    police_requested = any(word in query_lower for word in POLICE_HINTS)
    if police_requested and record.law_name == "Code of Criminal Procedure":
        score += 4

    property_requested = any(word in query_lower for word in PROPERTY_HINTS)
    fraud_requested = any(word in query_lower for word in FRAUD_HINTS)
    trespass_requested = any(word in query_lower for word in TRESPASS_HINTS)
    extortion_requested = any(word in query_lower for word in EXTORTION_HINTS)
    robbery_requested = any(word in query_lower for word in ROBBERY_HINTS)
    restraint_requested = any(word in query_lower for word in RESTRAINT_HINTS)
    confinement_requested = any(word in query_lower for word in CONFINEMENT_HINTS)
    mischief_requested = any(word in query_lower for word in MISCHIEF_HINTS)
    identity_requested = any(word in query_lower for word in IDENTITY_HINTS)
    electronic_fraud_requested = any(word in query_lower for word in ELECTRONIC_FRAUD_HINTS)
    electronic_forgery_requested = any(word in query_lower for word in ELECTRONIC_FORGERY_HINTS)

    if property_requested and record.offence_group == "property_offence":
        score += 2

    if fraud_requested and record.offence_group == "fraud_offence":
        score += 4

    if trespass_requested and (record.section_number in {"441", "447"} or record.offence_group == "property_offence"):
        score += 4

    if extortion_requested and record.offence_group == "violent_property_offence":
        score += 5

    if robbery_requested and record.offence_group == "violent_property_offence":
        score += 6

    if restraint_requested and not police_requested and record.offence_group == "restraint_offence":
        score += 5

    if confinement_requested and not police_requested and record.offence_group == "restraint_offence":
        score += 6

    if mischief_requested and record.offence_group == "property_damage_offence":
        score += 6

    if identity_requested and record.offence_group == "cyber_identity_offence":
        score += 6

    if electronic_fraud_requested and record.section_number == "14":
        score += 8
    elif electronic_fraud_requested and record.offence_group == "cyber_identity_offence":
        score += 5

    if electronic_forgery_requested and record.section_number == "13":
        score += 8
    elif electronic_forgery_requested and record.offence_group == "cyber_identity_offence":
        score += 5

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

    if not online_requested and not identity_requested and record.offence_group == "cyber_identity_offence":
        score -= 3

    if restraint_requested and not robbery_requested and not extortion_requested and record.offence_group == "violent_property_offence":
        score -= 3

    if mischief_requested and record.offence_group == "cyber_identity_offence":
        score -= 4

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

    return score



def retrieve_scored_legal_sources(query: str, limit: int = 3) -> list[tuple[int, LegalSourceRecord]]:
    scored_results: list[tuple[int, LegalSourceRecord]] = []

    for record in LEGAL_SOURCES:
        score = score_record(query, record)
        if score > 0:
            scored_results.append((score, record))

    scored_results.sort(
        key=lambda item: (
            item[0],
            1 if item[1].provision_kind == "definition" else 0,
            item[1].law_name,
            item[1].section_number,
        ),
        reverse=True,
    )

    return scored_results[:limit]



def retrieve_legal_sources(query: str, limit: int = 3) -> list[LegalSourceRecord]:
    return [record for _, record in retrieve_scored_legal_sources(query, limit=limit)]



def explain_record_match(query: str, record: LegalSourceRecord) -> list[str]:
    query_lower = normalize_text(query)
    searchable_text = normalize_text(" ".join(record.searchable_parts))

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

    punishment_requested = any(word in query_lower for word in PUNISHMENT_HINTS)
    if punishment_requested and record.provision_kind == "punishment":
        reasons.append("Punishment-related wording in the question aligns with this provision.")

    online_requested = any(phrase in query_lower for phrase in ONLINE_HINTS)
    if online_requested and record.law_name == "Prevention of Electronic Crimes Act":
        reasons.append("Online or cyber wording in the question aligns with PECA-related provisions.")

    police_requested = any(word in query_lower for word in POLICE_HINTS)
    if police_requested and record.law_name == "Code of Criminal Procedure":
        reasons.append("Police or detention wording in the question aligns with criminal-procedure provisions.")

    if record.related_sections:
        reasons.append(f"This record also links to related sections: {', '.join(record.related_sections[:2])}.")

    if not reasons:
        reasons.append("The prototype found a general text similarity with this record.")

    return reasons[:4]
