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
            "property",
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
            "eve teasing",
            "unwanted contact",
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
        ],
    },
    "trespass": {
        "label": "Trespass / Property Entry",
        "keywords": [
            "trespass",
            "criminal trespass",
            "illegal entry",
            "land dispute",
            "plot dispute",
            "unlawful entry",
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
    "cyber_offence": "cybercrime",
    "cyber_identity_offence": "cybercrime",
    "property_damage_offence": "property_damage",
    "restraint_offence": "restraint_confinement",
    "criminal_procedure": "arrest_detention",
}


def normalize_text(value: str) -> str:
    return value.strip().lower()



def detect_question_category(
    question: str, records: list[LegalSourceRecord] | None = None
) -> dict[str, str]:
    query = normalize_text(question)
    scores: dict[str, int] = {key: 0 for key in CATEGORY_CONFIG.keys()}

    for category_key, config in CATEGORY_CONFIG.items():
        keywords = config["keywords"]
        for keyword in keywords:
            if normalize_text(keyword) in query:
                scores[category_key] += 3

    if ("threat" in query or "threatening" in query) and "money" in query:
        scores["robbery_extortion"] += 6

    if "demanded money" in query or "money demand" in query:
        scores["robbery_extortion"] += 6

    if "gunpoint" in query or "snatched at gunpoint" in query:
        scores["robbery_extortion"] += 5

    if "blocked my way" in query or "locked me in" in query or "kept inside" in query:
        scores["restraint_confinement"] += 5

    if ("damaged" in query or "damage" in query) and ("car" in query or "bike" in query or "property" in query):
        scores["property_damage"] += 5

    if ("online" in query or "cyber" in query) and ("harassment" in query or "stalking" in query):
        scores["harassment"] += 6
        scores["cybercrime"] += 5

    if ("online" in query or "cyber" in query) and (
        "blackmail" in query or "photos" in query or "photo" in query or "privacy" in query
    ):
        scores["harassment"] += 7
        scores["cybercrime"] += 6
        scores["criminal_intimidation"] += 2

    if ("identity" in query or "cnic" in query or "fake profile" in query) and (
        "fraud" in query or "scam" in query or "forgery" in query
    ):
        scores["cybercrime"] += 7
        scores["cheating_fraud"] += 4

    for record in records or []:
        law_name = normalize_text(record.law_name)
        section_title = normalize_text(record.section_title)
        tags = " ".join(record.tags + record.aliases + record.keywords).lower()

        mapped_group = PROPERTY_GROUP_MAP.get(record.offence_group or "")
        if mapped_group:
            scores[mapped_group] += 4

        if "penal code" in law_name:
            if "theft" in section_title or "theft" in tags:
                scores["theft"] += 3
            if "defamation" in section_title or "defamation" in tags:
                scores["defamation"] += 3
            if "intimidation" in section_title or "threat" in tags:
                scores["criminal_intimidation"] += 3
            if "cheating" in section_title or "fraud" in tags or "breach of trust" in tags:
                scores["cheating_fraud"] += 4
            if "robbery" in section_title or "extortion" in tags or "mugging" in tags:
                scores["robbery_extortion"] += 7
            if "trespass" in section_title or "land" in tags or "illegal entry" in tags:
                scores["trespass"] += 5
            if "harassment" in section_title or "modesty" in tags:
                scores["harassment"] += 4
            if "restraint" in section_title or "confinement" in section_title or "blocked way" in tags:
                scores["restraint_confinement"] += 5
            if "mischief" in section_title or "property damage" in tags or "vandalism" in tags:
                scores["property_damage"] += 5

        if "electronic crimes" in law_name:
            scores["cybercrime"] += 5
            if "stalking" in section_title or "harassment" in tags:
                scores["harassment"] += 7
            if ("online" in query or "cyber" in query) and (
                "blackmail" in query or "photos" in query or "photo" in query or "privacy" in query
            ) and record.section_number == "24":
                scores["harassment"] += 8
                scores["cybercrime"] += 5
            if "identity" in section_title or "forgery" in section_title or "electronic fraud" in section_title:
                scores["cybercrime"] += 5
            if ("damaged" in query or "damage" in query) and ("car" in query or "bike" in query or "property" in query):
                scores["cybercrime"] -= 4

        if "criminal procedure" in law_name:
            scores["arrest_detention"] += 5

        if "authority" in section_title or "rank" in tags:
            scores["officer_authority"] += 4

    if scores["harassment"] > 0 and scores["cybercrime"] > 0 and ("online" in query or "cyber" in query or "social media" in query):
        scores["harassment"] += 5

    if ("online" in query or "cyber" in query) and (
        "blackmail" in query or "photos" in query or "photo" in query or "privacy" in query
    ) and scores["harassment"] > 0:
        scores["harassment"] += 4
        scores["cybercrime"] += 3

    if scores["robbery_extortion"] > 0 and scores["criminal_intimidation"] > 0 and (
        "money" in query or "gunpoint" in query or "snatched" in query
    ):
        scores["robbery_extortion"] += 5

    if scores["cybercrime"] > 0 and scores["cheating_fraud"] > 0 and (
        "online" in query or "cnic" in query or "identity" in query or "otp" in query
    ):
        scores["cybercrime"] += 5

    best_category = max(scores, key=scores.get)

    if scores[best_category] <= 0:
        best_category = "general"

    return {
        "key": best_category,
        "label": str(CATEGORY_CONFIG[best_category]["label"]),
    }
