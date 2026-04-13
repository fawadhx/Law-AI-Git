
import re

from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_source_store import get_active_legal_source_records, get_legal_source_store_status


def get_retrieval_source_status() -> dict[str, object]:
    status = get_legal_source_store_status()
    return {
        "active_source": status.active_source,
        "source_label": status.source_label,
        "database_ready": status.database_ready,
        "foundation_stage": status.foundation_stage,
        "active_record_count": status.active_record_count,
        "persisted_record_count": status.persisted_record_count,
        "detail": status.detail,
    }

CONCEPT_SYNONYMS: dict[str, list[str]] = {
    "theft": [
        "theft",
        "steal",
        "stealing",
        "stolen",
        "snatch",
        "snatched",
        "mobile snatching",
        "wallet",
        "phone",
        "took my phone",
        "without consent",
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
        "kill me",
        "harm me",
    ],
    "defamation": [
        "defamation",
        "defame",
        "reputation",
        "false statement",
        "badnami",
        "false allegation",
        "viral lie",
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
        "account",
        "profile",
    ],
    "privacy": [
        "privacy",
        "private",
        "personal data",
        "personal information",
        "private photos",
        "personal photos",
        "leak photos",
    ],
    "modesty": [
        "modesty",
        "harassment",
        "sexual harassment",
        "molestation",
        "touched her",
        "grabbed her",
        "private photos",
        "image misuse",
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
        "police picked me",
    ],
    "detention": [
        "detention",
        "24 hours",
        "twenty four hours",
        "twenty-four hours",
        "illegal detention",
        "kept in custody",
    ],
    "fir": [
        "fir",
        "first information report",
        "register fir",
        "registration of fir",
        "police complaint",
        "complaint to police",
        "sho refusing fir",
        "police not registering fir",
        "cognizable case",
        "cognizable offence",
        "non-cognizable",
        "non cognizable",
    ],
    "investigation": [
        "investigation",
        "investigate",
        "investigating",
        "inquiry",
        "probe",
        "power to investigate",
        "investigate cognizable case",
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
        "fake promise",
    ],
    "breach_of_trust": [
        "criminal breach of trust",
        "breach of trust",
        "entrusted property",
        "entrusted money",
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
        "entered my plot",
        "entered my house",
        "entered my home",
        "break into house",
        "break into home",
        "home intrusion",
        "qabza",
    ],
    "house_trespass": [
        "house trespass",
        "house-trespass",
        "entered my house",
        "entered my home",
        "broke into my house",
        "broke into my home",
        "home invasion",
        "ghar mein ghus gaya",
    ],
    "harassment": [
        "harassment",
        "stalking",
        "cyber stalking",
        "insult modesty",
        "eve teasing",
        "unwanted contact",
        "calling me again and again",
        "messaging me repeatedly",
    ],
    "assault": [
        "assault",
        "criminal force",
        "slap",
        "slapped",
        "push",
        "pushed",
        "hit",
        "beating",
        "beat me",
        "attack",
        "attacked",
        "grabbed me",
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
        "gunpoint",
        "armed snatching",
        "snatching with force",
        "violent theft",
        "street robbery",
        "snatched at gunpoint",
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
        "locked room",
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
        "car windows",
        "vehicle damage",
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
        "fake screenshot",
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
    "civil": [
        "civil dispute",
        "family matter",
        "divorce",
        "khula",
        "marriage",
        "inheritance",
        "maintenance",
        "child custody",
        "rent",
        "tenant",
        "landlord",
        "eviction",
        "ownership dispute",
        "partition",
        "agreement",
        "contract",
        "debt",
        "loan dispute",
        "salary issue",
        "employment dispute",
    ],
    "officer_authority": [
        "sho",
        "asi",
        "inspector",
        "sub inspector",
        "police powers",
        "officer authority",
        "rank powers",
        "can arrest",
        "can detain",
        "can register fir",
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
    "entered my house": ["house_trespass", "trespass"],
    "entered my home": ["house_trespass", "trespass"],
    "broke into my house": ["house_trespass", "trespass"],
    "broke into my home": ["house_trespass", "trespass"],
    "slapped me": ["assault"],
    "pushed me": ["assault"],
    "grabbed her": ["assault", "modesty", "harassment"],
    "touched her": ["modesty", "harassment"],
    "leak my photos": ["privacy", "harassment", "online", "threat"],
    "private photos": ["privacy", "harassment", "online"],
    "can sho arrest": ["officer_authority", "police", "arrest"],
    "can asi arrest": ["officer_authority", "police", "arrest"],
    "inspector powers": ["officer_authority", "police"],
    "register fir": ["fir", "officer_authority", "police"],
    "fir not registered": ["fir", "police"],
    "sho refusing fir": ["fir", "officer_authority", "police"],
    "non cognizable": ["fir", "investigation", "police"],
    "non-cognizable": ["fir", "investigation", "police"],
    "investigate cognizable case": ["fir", "investigation", "police"],
    "tenant dispute": ["civil"],
    "landlord dispute": ["civil"],
    "divorce issue": ["civil"],
    "inheritance dispute": ["civil"],
    "property ownership dispute": ["civil"],
}


PUNISHMENT_HINTS = ["punishment", "penalty", "sentence", "fine", "jail", "imprisonment", "saza"]
ONLINE_HINTS = ["online", "internet", "cyber", "social media", "facebook", "instagram", "whatsapp", "tiktok"]
POLICE_HINTS = ["police", "arrest", "detain", "custody", "warrant", "fir", "complaint", "investigation"]
PROPERTY_HINTS = ["property", "money", "land", "plot", "phone", "wallet", "entrusted", "house", "home"]
FRAUD_HINTS = ["cheat", "cheated", "cheating", "fraud", "scam", "deceive", "deceived", "deal", "property deal", "420", "trust", "entrusted", "amanat", "khayanat"]
TRESPASS_HINTS = ["trespass", "illegal entry", "unlawful entry", "plot", "entered", "enter", "land", "leave", "house", "home", "break into"]
HOUSE_HINTS = ["house", "home", "flat", "dwelling"]
EXTORTION_HINTS = ["extortion", "bhatta", "ransom", "money demand", "demanded money", "demanded money by threat", "blackmail for money", "fear of injury"]
ROBBERY_HINTS = ["robbery", "mugging", "gunpoint", "armed snatching", "snatching with force", "snatched at gunpoint", "violent theft"]
RESTRAINT_HINTS = ["wrongful restraint", "blocked way", "obstruct", "rasta", "prevented from going", "stopped me"]
CONFINEMENT_HINTS = ["wrongful confinement", "locked in", "kept inside", "confined", "locked room", "band"]
MISCHIEF_HINTS = ["mischief", "vandalism", "property damage", "damaged", "broke", "destroyed", "damage car", "damage bike", "car windows", "vehicle damage"]
IDENTITY_HINTS = ["identity", "identity theft", "cnic", "impersonation", "fake profile", "my documents"]
ELECTRONIC_FRAUD_HINTS = ["electronic fraud", "online scam", "digital scam", "fake website", "banking scam", "otp"]
ELECTRONIC_FORGERY_HINTS = ["electronic forgery", "fake screenshot", "forged pdf", "edited digital evidence", "fake digital document"]
THREAT_HINTS = ["threat", "threaten", "intimidation", "blackmail", "alarm", "leak"]
HARASSMENT_HINTS = ["harassment", "stalking", "modesty", "privacy intrusion", "unwanted contact", "photos", "video"]
ASSAULT_HINTS = ["assault", "slap", "slapped", "push", "pushed", "hit", "beating", "beat", "attacked", "grabbed"]
FORCE_HINTS = ["force", "gunpoint", "weapon", "armed", "violence", "grabbed", "pushed"]
FIR_HINTS = ["fir", "first information report", "register fir", "registration of fir", "police complaint", "complaint to police", "sho refusing fir", "police not registering fir", "cognizable", "non-cognizable", "non cognizable"]
INVESTIGATION_HINTS = ["investigation", "investigate", "investigating", "inquiry", "probe", "power to investigate"]
CIVIL_HINTS = ["civil", "divorce", "khula", "marriage", "inheritance", "maintenance", "custody", "rent", "tenant", "landlord", "eviction", "ownership", "partition", "agreement", "contract", "debt", "salary", "employment"]
OFFICER_AUTHORITY_HINTS = ["sho", "asi", "inspector", "sub inspector", "officer authority", "police powers", "can arrest", "can detain", "can register fir", "rank powers"]


PRIMARY_KINDS = {"definition", "offence", "aggravated_offence", "general"}


def normalize_text(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s\-\/]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def tokenize(value: str) -> list[str]:
    return [token for token in normalize_text(value).split(" ") if token]


def extract_section_references(query: str) -> list[tuple[str | None, str]]:
    cleaned = normalize_text(query)
    refs: list[tuple[str | None, str]] = []

    patterns = [
        r"(ppc|peca|crpc)\s+section\s+(\d+[a-z]?)",
        r"section\s+(\d+[a-z]?)\s+(ppc|peca|crpc)",
        r"u\s*\/?\s*s\s*(\d+[a-z]?)\s+(ppc|peca|crpc)",
        r"\b(ppc|peca|crpc)\s+(\d+[a-z]?)\b",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, cleaned):
            groups = match.groups()
            if len(groups) != 2:
                continue
            if groups[0] in {"ppc", "peca", "crpc"}:
                law_hint, section_number = groups[0], groups[1]
            else:
                section_number, law_hint = groups[0], groups[1]
            refs.append((law_hint, section_number.upper()))

    for match in re.finditer(r"\bsection\s+(\d+[a-z]?)\b", cleaned):
        refs.append((None, match.group(1).upper()))

    unique: list[tuple[str | None, str]] = []
    seen: set[tuple[str | None, str]] = set()
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            unique.append(ref)
    return unique


def law_short_name(record: LegalSourceRecord) -> str:
    if record.law_name == "Pakistan Penal Code":
        return "ppc"
    if record.law_name == "Prevention of Electronic Crimes Act":
        return "peca"
    if record.law_name == "Code of Criminal Procedure":
        return "crpc"
    return ""


def expand_query_terms(query: str) -> list[str]:
    query_lower = normalize_text(query)
    expanded_terms: list[str] = []
    expanded_terms.extend(tokenize(query))

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

    unique_terms: list[str] = []
    seen: set[str] = set()
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
        "house_context": any(word in query_lower for word in HOUSE_HINTS),
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
        "assault": any(word in query_lower for word in ASSAULT_HINTS),
        "force": any(word in query_lower for word in FORCE_HINTS),
        "fir": any(word in query_lower for word in FIR_HINTS),
        "investigation": any(word in query_lower for word in INVESTIGATION_HINTS),
        "non_cognizable": "non-cognizable" in query_lower or "non cognizable" in query_lower or "nc report" in query_lower or "nc case" in query_lower,
        "cognizable": "cognizable" in query_lower,
        "civil": any(word in query_lower for word in CIVIL_HINTS),
        "officer_authority": any(word in query_lower for word in OFFICER_AUTHORITY_HINTS),
        "officer_rank": any(word in query_lower for word in ["sho", "asi", "inspector", "sub inspector", "sub-inspector"]),
        "mentions_money": "money" in query_lower,
        "mentions_woman": any(word in query_lower for word in ["woman", "women", "girl", "female", "wife", "lady"]),
        "mentions_photo": any(word in query_lower for word in ["photo", "photos", "video", "picture", "images"]),
        "section_lookup": "section " in query_lower or "u/s" in query_lower or query_lower.startswith(("ppc ", "peca ", "crpc ")),
    }


def is_primary_record(record: LegalSourceRecord) -> bool:
    return record.provision_kind in PRIMARY_KINDS


def build_query_intent(query: str) -> dict[str, bool]:
    query_lower = normalize_text(query)
    section_refs = extract_section_references(query)
    return {
        "section_lookup": bool(section_refs),
        "punishment_focus": any(word in query_lower for word in PUNISHMENT_HINTS),
        "definition_focus": any(
            phrase in query_lower
            for phrase in [
                "what is",
                "meaning of",
                "define",
                "definition",
                "cover",
                "covers",
                "under section",
            ]
        ) and not any(word in query_lower for word in PUNISHMENT_HINTS),
        "exact_law_mentioned": any(law in query_lower for law in ["ppc", "peca", "crpc"]),
    }


def record_matches_requested_section(query: str, record: LegalSourceRecord) -> bool:
    references = extract_section_references(query)
    if not references:
        return False
    for law_hint, section_number in references:
        if section_number != record.section_number.upper():
            continue
        if law_hint and law_hint != law_short_name(record):
            continue
        return True
    return False


def sort_key_for_record(
    item: tuple[int, LegalSourceRecord],
    query: str,
) -> tuple[int, int, int, str, str]:
    score, record = item
    intent = build_query_intent(query)
    exact_match = 1 if record_matches_requested_section(query, record) else 0
    if intent["section_lookup"]:
        priority = 2 if exact_match else (1 if record.provision_kind == "punishment" else 0)
    elif intent["punishment_focus"]:
        priority = 2 if record.provision_kind == "punishment" else (1 if is_primary_record(record) else 0)
    else:
        priority = 2 if is_primary_record(record) else (1 if record.provision_kind == "punishment" else 0)

    return (score, exact_match, priority, record.law_name, record.section_number)


def citation_reference(record: LegalSourceRecord) -> str:
    return normalize_text(record.citation_label)


def record_reference_matches(reference: str, record: LegalSourceRecord) -> bool:
    ref = normalize_text(reference)
    if not ref:
        return False

    candidates = {
        normalize_text(record.citation_label),
        normalize_text(f"{record.law_name} section {record.section_number}"),
        normalize_text(f"{law_short_name(record)} section {record.section_number}"),
        normalize_text(f"section {record.section_number}"),
    }
    return ref in candidates or any(candidate in ref or ref in candidate for candidate in candidates)


def score_exact_section_match(query: str, record: LegalSourceRecord) -> int:
    references = extract_section_references(query)
    if not references:
        return 0

    score = 0
    for law_hint, section_number in references:
        if section_number != record.section_number.upper():
            continue
        score += 18
        if law_hint and law_hint == law_short_name(record):
            score += 10
        elif law_hint:
            score -= 8

    return score


def score_record(query: str, record: LegalSourceRecord) -> int:
    query_lower = normalize_text(query)
    query_terms = expand_query_terms(query)
    signals = build_query_signals(query)
    intent = build_query_intent(query)

    searchable_text = normalize_text(" ".join(record.searchable_parts))
    searchable_tokens = set(tokenize(searchable_text))
    score = 0
    civil_only = signals["civil"] and not any(
        [
            signals["online"],
            signals["police"],
            signals["threat"],
            signals["harassment"],
            signals["assault"],
            signals["trespass"],
            signals["fraud"],
            signals["mischief"],
            signals["restraint"],
            signals["confinement"],
        ]
    )

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
        score += 7

    for tag in record.tags + record.aliases + record.keywords:
        tag_normalized = normalize_text(tag)
        if tag_normalized and tag_normalized in query_lower:
            score += 3

    score += score_exact_section_match(query, record)

    if record.section_number and f" {record.section_number.lower()} " in f" {query_lower} ":
        score += 2

    if signals["punishment"] and record.provision_kind == "punishment":
        score += 10
    elif signals["punishment"] and record.punishment_summary:
        score += 4
    elif not signals["punishment"] and not intent["section_lookup"] and record.provision_kind == "punishment":
        score -= 2

    if signals["online"] and record.law_name == "Prevention of Electronic Crimes Act":
        score += 4

    if signals["police"] and record.law_name == "Code of Criminal Procedure":
        score += 5

    if signals["fir"] and record.section_number in {"154", "155", "156"}:
        score += 10

    if signals["investigation"] and record.section_number == "156":
        score += 8

    if signals["non_cognizable"] and record.section_number == "155":
        score += 14
    elif signals["non_cognizable"] and record.section_number in {"154", "156"}:
        score -= 6

    if signals["cognizable"] and record.section_number in {"154", "156"}:
        score += 6

    if signals["officer_rank"] and signals["fir"] and record.section_number == "154":
        score += 8
    elif not signals["police"] and record.offence_group == "criminal_procedure":
        score -= 5

    if signals["officer_rank"] and signals["police"] and record.section_number in {"46", "54", "61", "154", "155", "156"}:
        score += 8

    if signals["officer_authority"] and record.law_name == "Code of Criminal Procedure":
        score += 3

    if "register fir" in query_lower and record.section_number == "154":
        score += 12

    if any(phrase in query_lower for phrase in ["fir not registered", "police not registering fir", "sho refusing fir", "refused to register fir"]):
        if record.section_number == "154":
            score += 12
        elif record.section_number == "155":
            score += 4

    if any(phrase in query_lower for phrase in ["non-cognizable", "non cognizable", "nc report", "nc case"]) and record.section_number == "155":
        score += 12

    if any(phrase in query_lower for phrase in ["investigate", "investigation", "power to investigate"]) and record.section_number == "156":
        score += 8

    if signals["property"] and record.offence_group in {"theft_offence", "breach_of_trust_offence", "trespass_offence"}:
        score += 2

    if signals["fraud"] and record.offence_group == "fraud_offence":
        score += 4

    if signals["fraud"] and record.section_number in {"415", "417", "420"}:
        score += 5

    if signals["trespass"] and record.section_number in {"441", "447", "442", "448"}:
        score += 6

    if signals["house_context"] and signals["trespass"] and record.section_number in {"442", "448"}:
        score += 9

    if signals["house_context"] and signals["trespass"] and record.section_number in {"441", "447"}:
        score += 2

    if civil_only and record.offence_group in {
        "theft_offence",
        "breach_of_trust_offence",
        "fraud_offence",
        "violent_property_offence",
        "threat_offence",
        "harassment_offence",
        "assault_offence",
        "property_damage_offence",
        "restraint_offence",
        "trespass_offence",
        "cyber_offence",
        "cyber_identity_offence",
    }:
        score -= 10

    if signals["civil"] and not signals["trespass"] and record.offence_group == "trespass_offence":
        score -= 4

    if signals["civil"] and not signals["fraud"] and record.offence_group in {"fraud_offence", "breach_of_trust_offence"}:
        score -= 3

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

    if signals["assault"] and record.offence_group == "assault_offence":
        score += 8

    if signals["assault"] and record.section_number == "354" and signals["mentions_woman"]:
        score += 8

    if signals["mentions_woman"] and signals["harassment"] and record.section_number in {"354", "509", "21"}:
        score += 7

    if signals["mentions_photo"] and signals["threat"] and record.section_number in {"24", "503", "506", "21"}:
        score += 7

    if signals["mentions_photo"] and signals["harassment"] and record.section_number in {"24", "21", "20", "509"}:
        score += 9

    if any(phrase in query_lower for phrase in ["calling me", "keeps calling", "keeps messaging", "again and again"]) and record.section_number in {"24", "21", "509"}:
        score += 7

    if signals["force"] and record.offence_group == "violent_property_offence":
        score += 5

    if signals["force"] and record.offence_group == "assault_offence":
        score += 3

    if signals["threat"] and signals["online"] and record.section_number in {"24", "503", "506"}:
        score += 5

    if signals["harassment"] and signals["online"] and record.section_number in {"24", "509", "20", "21"}:
        score += 6

    if signals["harassment"] and not signals["online"] and record.section_number in {"509", "354"}:
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

    if "354" in query_lower and record.section_number == "354":
        score += 8

    if "448" in query_lower and record.section_number == "448":
        score += 8

    if "442" in query_lower and record.section_number == "442":
        score += 8

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

    if "house trespass" in query_lower and record.section_number in {"442", "448"}:
        score += 8

    if "entered my house" in query_lower and record.section_number in {"442", "448"}:
        score += 8

    if "broke into my house" in query_lower and record.section_number in {"442", "448"}:
        score += 8

    if any(phrase in query_lower for phrase in ["slapped me", "pushed me", "hit me", "beat me"]) and record.section_number in {"351", "352"}:
        score += 8

    if any(phrase in query_lower for phrase in ["grabbed a woman", "grabbed her", "touched her", "molested"]) and record.section_number in {"354", "509"}:
        score += 9

    if any(phrase in query_lower for phrase in ["leak photos", "private photos", "viral photos"]) and record.section_number in {"24", "21", "509", "503", "506"}:
        score += 8

    if "fake profile" in query_lower and record.section_number in {"16", "24", "20"}:
        score += 7

    if intent["section_lookup"] and record_matches_requested_section(query, record):
        score += 18
        if record.provision_kind == "punishment":
            score += 2

    if intent["definition_focus"] and is_primary_record(record):
        score += 4

    if signals["confinement"] and not signals["assault"] and record.offence_group == "assault_offence":
        score -= 4

    if signals["mentions_photo"] and signals["threat"] and record.section_number in {"24", "21", "20", "509"}:
        score += 3

    if signals["mentions_photo"] and signals["threat"] and record.section_number in {"503", "506"} and not signals["mentions_money"]:
        score -= 1

    if signals["punishment"] and not intent["section_lookup"] and is_primary_record(record) and record.punishment_summary:
        score += 2

    return score


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

    if signals["trespass"] and signals["mischief"]:
        return candidate_score >= 12 and candidate_record.section_number in {"441", "447", "442", "448", "425", "426"}

    if candidate_score < max(8, top_score - 8):
        return False

    if signals["online"] and signals["threat"]:
        return candidate_record.section_number in {"24", "503", "506", "21"}

    if signals["online"] and signals["harassment"]:
        return candidate_record.section_number in {"24", "509", "20", "21"}

    if signals["fir"] or signals["investigation"]:
        return candidate_record.section_number in {"154", "155", "156"}

    if signals["identity"] and (signals["fraud"] or signals["electronic_forgery"] or signals["electronic_fraud"]):
        return candidate_record.section_number in {"13", "14", "16", "420"}

    if signals["robbery"] and signals["threat"]:
        return candidate_record.section_number in {"390", "392", "503", "506", "383", "384"}

    if signals["trespass"] and signals["mischief"]:
        return candidate_record.section_number in {"441", "447", "442", "448", "425", "426"}

    if signals["harassment"] and signals["mentions_photo"]:
        return candidate_record.section_number in {"354", "509", "20", "21", "24", "503", "506"}

    if signals["assault"] and signals["mentions_woman"]:
        return candidate_record.section_number in {"354", "509", "352"}

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

    signals = build_query_signals(query)
    intent = build_query_intent(query)
    ranked_results = sorted(scored_results, key=lambda item: sort_key_for_record(item, query), reverse=True)
    top_score, primary = ranked_results[0]
    selected: list[tuple[int, LegalSourceRecord]] = [(top_score, primary)]
    selected_ids = {primary.id}

    linked_records = sorted(
        find_linked_records(primary, ranked_results),
        key=lambda item: (
            item[0],
            (
                2
                if (
                    intent["punishment_focus"]
                    and item[1].provision_kind == "punishment"
                )
                else (
                    2
                    if (
                        not intent["punishment_focus"]
                        and is_primary_record(item[1])
                    )
                    else (
                        1
                        if (
                            item[1].provision_kind == "punishment"
                        )
                        else 0
                    )
                )
            ),
        ),
        reverse=True,
    )

    for item in linked_records:
        if len(selected) >= limit:
            break
        score, record = item
        if record.id in selected_ids:
            continue
        if (
            signals["punishment"]
            or intent["section_lookup"]
            or record.provision_kind == "punishment"
            or (intent["section_lookup"] and any(ref in record.citation_label.lower() for ref in [primary.section_number.lower()]))
            or record.law_name != primary.law_name
            or (signals["house_context"] and record.section_number in {"448", "447"})
            or (signals["fir"] and record.section_number in {"154", "155", "156"})
        ):
            selected.append(item)
            selected_ids.add(record.id)
            break

    overlap_candidates = [
        item
        for item in ranked_results[1:]
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
            if intent["punishment_focus"]:
                include_linked = linked_record.provision_kind == "punishment" or is_primary_record(linked_record)
            else:
                include_linked = is_primary_record(linked_record) or (
                    linked_record.provision_kind == "punishment" and len(selected) + 1 >= limit
                )
            if include_linked:
                selected.append((linked_score, linked_record))
                selected_ids.add(linked_record.id)
                break

    minimum_fill_score = max(6, top_score - 10)
    for score, record in ranked_results[1:]:
        if len(selected) >= limit:
            break
        if record.id in selected_ids or score < minimum_fill_score:
            continue
        same_group = primary.offence_group and record.offence_group == primary.offence_group
        if not (same_group or intent["section_lookup"]):
            continue
        selected.append((score, record))
        selected_ids.add(record.id)

    return selected[:limit]


def retrieve_scored_legal_sources(query: str, limit: int = 4) -> list[tuple[int, LegalSourceRecord]]:
    all_results: list[tuple[int, LegalSourceRecord]] = []
    signals = build_query_signals(query)
    civil_only = signals["civil"] and not any(
        [
            signals["online"],
            signals["police"],
            signals["threat"],
            signals["harassment"],
            signals["assault"],
            signals["trespass"],
            signals["fraud"],
            signals["mischief"],
            signals["restraint"],
            signals["confinement"],
        ]
    )
    pure_officer_query = signals["officer_rank"] and signals["officer_authority"] and not any(
        [signals["police"], signals["section_lookup"], signals["threat"], signals["online"], signals["fraud"]]
    )

    for record in get_active_legal_source_records():
        score = score_record(query, record)
        if score > 0:
            all_results.append((score, record))

    all_results.sort(key=lambda item: sort_key_for_record(item, query), reverse=True)

    if civil_only:
        if not all_results or all_results[0][0] < 18:
            return []

    if pure_officer_query:
        if not all_results or all_results[0][0] < 14:
            return []

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

    exact_section_score = score_exact_section_match(query, record)
    if exact_section_score > 0:
        reasons.append(f"Specific section reference matched: {record.citation_label}.")

    matched_tags = [
        tag for tag in (record.tags + record.aliases + record.keywords)
        if normalize_text(tag) in query_lower
    ]
    if matched_tags:
        reasons.append(f"Matched legal tags or aliases: {', '.join(matched_tags[:3])}.")

    concept_hits = []
    for term in expand_query_terms(query):
        if len(term) >= 4 and term in searchable_text:
            concept_hits.append(term)

    unique_hits: list[str] = []
    seen: set[str] = set()
    for hit in concept_hits:
        if hit not in seen:
            seen.add(hit)
            unique_hits.append(hit)

    if unique_hits:
        reasons.append(f"Conceptual keyword overlap found: {', '.join(unique_hits[:4])}.")

    if signals["punishment"] and record.provision_kind == "punishment":
        reasons.append("Punishment-related wording in the question aligns with this provision.")

    if signals["online"] and record.law_name == "Prevention of Electronic Crimes Act":
        reasons.append("Online or cyber wording in the question aligns with PECA-related provisions.")

    if signals["police"] and record.law_name == "Code of Criminal Procedure":
        reasons.append("Police or detention wording in the question aligns with criminal-procedure provisions.")

    if signals["officer_rank"] and record.section_number in {"46", "54", "61", "154", "155", "156"}:
        reasons.append("The query mentions a police rank together with procedure-related powers, so criminal-procedure sections were prioritized.")

    if signals["fir"] and record.section_number in {"154", "155", "156"}:
        reasons.append("The query asks about FIR registration, cognizable or non-cognizable procedure, or police reporting steps.")

    if signals["investigation"] and record.section_number == "156":
        reasons.append("The query asks about investigation powers, which aligns with cognizable-case investigation procedure.")

    if signals["civil"] and not any([signals["online"], signals["police"], signals["threat"], signals["assault"], signals["harassment"]]):
        reasons.append("The query also contains civil or family-dispute wording, so this match should be treated cautiously because prototype coverage is limited there.")

    if signals["house_context"] and signals["trespass"] and record.section_number in {"442", "448"}:
        reasons.append("The query points to a house or home entry situation, which aligns with house-trespass provisions.")

    if signals["assault"] and record.section_number in {"351", "352"}:
        reasons.append("The query includes physical-force wording such as slapping, pushing, hitting, or assault.")

    if signals["mentions_woman"] and record.section_number == "354":
        reasons.append("The query mentions force or touching involving a woman, which aligns with modesty-related protection provisions.")

    if signals["mentions_photo"] and signals["threat"] and record.section_number in {"24", "21", "503", "506"}:
        reasons.append("The query combines threat wording with photo or privacy misuse, so overlapping PECA and PPC provisions were considered.")

    if signals["identity"] and (signals["fraud"] or signals["electronic_forgery"] or signals["electronic_fraud"]) and record.section_number in {"13", "14", "16", "420"}:
        reasons.append("The query combines identity misuse with fraud or forgery wording, so overlapping cyber-fraud provisions were considered.")

    if record.related_sections:
        reasons.append(f"This record also links to related sections: {', '.join(record.related_sections[:2])}.")

    if not reasons:
        reasons.append("The prototype found a general text similarity with this record.")

    return reasons[:4]
