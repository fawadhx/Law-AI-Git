
from app.schemas.legal_source import LegalSourceRecord


CATEGORY_CONFIG: dict[str, dict[str, object]] = {
    "theft": {
        "label": "Theft / Property Offence",
        "keywords": [
            "theft",
            "steal",
            "stolen",
            "stealing",
            "snatch",
            "snatched",
            "mobile snatching",
            "wallet",
            "phone",
        ],
    },
    "cheating_fraud": {
        "label": "Cheating / Fraud / Breach of Trust",
        "keywords": [
            "cheating",
            "cheated",
            "fraud",
            "scam",
            "deceive",
            "deception",
            "420",
            "dhoka",
            "deal",
            "property deal",
            "breach of trust",
            "criminal breach of trust",
            "amanat",
            "khayanat",
            "entrusted money",
            "investment scam",
        ],
    },
    "robbery_extortion": {
        "label": "Robbery / Extortion / Violent Taking",
        "keywords": [
            "robbery",
            "extortion",
            "mugging",
            "gunpoint",
            "bhatta",
            "ransom",
            "money demand",
            "snatching with force",
            "snatched at gunpoint",
            "demanded money",
            "armed snatching",
        ],
    },
    "criminal_intimidation": {
        "label": "Threat / Criminal Intimidation",
        "keywords": [
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
    },
    "defamation": {
        "label": "Defamation / Reputation Harm",
        "keywords": [
            "defamation",
            "defame",
            "reputation",
            "false statement",
            "badnami",
            "insult",
            "reputation harm",
            "false allegation",
        ],
    },
    "harassment": {
        "label": "Harassment / Modesty / Stalking",
        "keywords": [
            "harassment",
            "sexual harassment",
            "stalking",
            "cyber stalking",
            "modesty",
            "privacy intrusion",
            "509",
            "354",
            "eve teasing",
            "unwanted contact",
            "grabbed her",
            "touched her",
            "leak photos",
            "private photos",
        ],
    },
    "assault_force": {
        "label": "Assault / Criminal Force",
        "keywords": [
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
    },
    "cybercrime": {
        "label": "Cybercrime / PECA-related Issue",
        "keywords": [
            "online",
            "internet",
            "cyber",
            "digital",
            "social media",
            "facebook",
            "instagram",
            "whatsapp",
            "hack",
            "hacked",
            "hacking",
            "account",
            "privacy",
            "data",
            "unauthorized access",
            "unauthorised access",
            "minor",
            "image misuse",
            "identity theft",
            "cnic",
            "fake profile",
            "electronic fraud",
            "electronic forgery",
            "otp scam",
            "fake screenshot",
        ],
    },
    "trespass": {
        "label": "Trespass / Property Entry",
        "keywords": [
            "trespass",
            "criminal trespass",
            "house trespass",
            "illegal entry",
            "land dispute",
            "plot dispute",
            "unlawful entry",
            "entered my plot",
            "entered my house",
            "entered my home",
            "broke into my house",
            "qabza",
        ],
    },
    "restraint_confinement": {
        "label": "Wrongful Restraint / Confinement",
        "keywords": [
            "wrongful restraint",
            "wrongful confinement",
            "blocked way",
            "locked in",
            "prevented from going",
            "stopped me from leaving",
            "kept inside",
        ],
    },
    "property_damage": {
        "label": "Property Damage / Mischief",
        "keywords": [
            "mischief",
            "property damage",
            "vandalism",
            "damage property",
            "damaged property",
            "damaged my car",
            "car windows",
            "broke my car",
            "destroyed property",
            "tod phod",
        ],
    },
    "arrest_detention": {
        "label": "Arrest / Detention / Criminal Procedure",
        "keywords": [
            "arrest",
            "arrested",
            "detain",
            "detained",
            "detention",
            "custody",
            "24 hours",
            "twenty-four hours",
            "twenty four hours",
            "warrant",
            "without warrant",
            "police",
        ],
    },
    "officer_authority": {
        "label": "Police Rank / Officer Authority",
        "keywords": [
            "sho",
            "asi",
            "inspector",
            "sub inspector",
            "officer authority",
            "rank",
            "powers of police",
            "police powers",
        ],
    },
    "general": {
        "label": "General Legal Information",
        "keywords": [],
    },
}


PROPERTY_GROUP_MAP = {
    "fraud_offence": "cheating_fraud",
    "violent_property_offence": "robbery_extortion",
    "threat_offence": "criminal_intimidation",
    "reputation_offence": "defamation",
    "harassment_offence": "harassment",
    "assault_offence": "assault_force",
    "cyber_offence": "cybercrime",
    "cyber_identity_offence": "cybercrime",
    "property_damage_offence": "property_damage",
    "restraint_offence": "restraint_confinement",
    "criminal_procedure": "arrest_detention",
    "property_offence": "trespass",
}


def normalize_text(value: str) -> str:
    return value.strip().lower()


def detect_question_category(
    question: str, records: list[LegalSourceRecord] | None = None
) -> dict[str, str]:
    query = normalize_text(question)
    scores: dict[str, int] = {key: 0 for key in CATEGORY_CONFIG.keys()}

    for category_key, config in CATEGORY_CONFIG.items():
        for keyword in config["keywords"]:
            if normalize_text(keyword) in query:
                scores[category_key] += 3

    if ("threat" in query or "threatening" in query or "blackmail" in query) and "money" in query:
        scores["robbery_extortion"] += 6

    if "demanded money" in query or "money demand" in query:
        scores["robbery_extortion"] += 6

    if "gunpoint" in query or "snatched at gunpoint" in query or "armed snatching" in query:
        scores["robbery_extortion"] += 6

    if "blocked my way" in query or "locked me in" in query or "kept inside" in query:
        scores["restraint_confinement"] += 5

    if ("damaged" in query or "damage" in query) and ("car" in query or "bike" in query or "property" in query):
        scores["property_damage"] += 5

    if any(term in query for term in ["slap", "slapped", "push", "pushed", "hit", "beat", "beating", "attack", "attacked"]):
        scores["assault_force"] += 6

    if any(term in query for term in ["woman", "girl", "female", "wife", "lady"]) and any(
        term in query for term in ["grab", "grabbed", "touch", "touched", "harass", "modesty", "molest"]
    ):
        scores["harassment"] += 8
        scores["assault_force"] += 2

    if any(term in query for term in ["calling me", "keeps calling", "keeps messaging", "again and again"]) and any(
        term in query for term in ["photo", "photos", "video", "private"]
    ) and any(term in query for term in ["threat", "threatening", "blackmail", "leak", "viral"]):
        scores["harassment"] += 10
        scores["cybercrime"] += 6
        scores["criminal_intimidation"] += 2

    if ("online" in query or "cyber" in query) and ("harassment" in query or "stalking" in query):
        scores["harassment"] += 6
        scores["cybercrime"] += 5

    if any(term in query for term in ["private photos", "photo", "photos", "video"]) and any(
        term in query for term in ["leak", "upload", "share", "viral", "blackmail", "threat", "threaten"]
    ):
        scores["harassment"] += 7
        scores["cybercrime"] += 5
        scores["criminal_intimidation"] += 3

    if ("identity" in query or "cnic" in query or "fake profile" in query) and (
        "fraud" in query or "scam" in query or "forgery" in query
    ):
        scores["cybercrime"] += 7
        scores["cheating_fraud"] += 4

    if any(term in query for term in ["house", "home", "room", "flat"]) and any(
        term in query for term in ["entered", "entry", "broke into", "break into", "illegal entry", "trespass"]
    ):
        scores["trespass"] += 8

    if "section " in query or "u/s " in query or query.startswith("ppc ") or query.startswith("peca ") or query.startswith("crpc "):
        scores["general"] += 1

    for record in records or []:
        scores[PROPERTY_GROUP_MAP.get(record.offence_group or "", "general")] += 4

        section_title = normalize_text(record.section_title)
        tags = " ".join(record.tags).lower()
        law_name = normalize_text(record.law_name)

        if "electronic crimes" in law_name:
            scores["cybercrime"] += 4

        if "criminal procedure" in law_name:
            scores["arrest_detention"] += 4

        if record.section_number in {"442", "448"}:
            scores["trespass"] += 5
        if record.section_number in {"351", "352"}:
            scores["assault_force"] += 5
        if record.section_number == "354":
            scores["harassment"] += 6
            scores["assault_force"] += 2

        if "house-trespass" in section_title:
            scores["trespass"] += 6
        if "assault" in section_title and record.section_number != "354":
            scores["assault_force"] += 4
        if "modesty" in section_title or "harassment" in tags:
            scores["harassment"] += 5

        if "threat" in query and record.section_number in {"503", "506"}:
            scores["criminal_intimidation"] += 4
        if "money" in query and record.section_number in {"383", "384", "390", "392"}:
            scores["robbery_extortion"] += 4

    if scores["harassment"] > 0 and scores["cybercrime"] > 0 and (
        "online" in query or "cyber" in query or "social media" in query or "photos" in query
    ):
        scores["harassment"] += 4

    if scores["robbery_extortion"] > 0 and scores["criminal_intimidation"] > 0 and (
        "money" in query or "gunpoint" in query or "snatched" in query
    ):
        scores["robbery_extortion"] += 4

    if scores["trespass"] > 0 and scores["property_damage"] > 0 and (
        "house" in query or "home" in query or "plot" in query or "property" in query
    ):
        scores["trespass"] += 3

    if scores["cybercrime"] > 0 and scores["cheating_fraud"] > 0 and (
        "online" in query or "cnic" in query or "identity" in query or "otp" in query
    ):
        scores["cybercrime"] += 4

    best_category = max(scores, key=scores.get)
    if scores[best_category] <= 0:
        best_category = "general"

    return {
        "key": best_category,
        "label": str(CATEGORY_CONFIG[best_category]["label"]),
    }
