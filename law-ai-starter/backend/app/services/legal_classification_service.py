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
            "fraud",
            "scam",
            "deceive",
            "deception",
            "420",
            "dhoka",
            "breach of trust",
            "criminal breach of trust",
            "amanat",
            "khayanat",
            "entrusted money",
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
    "threat_offence": "criminal_intimidation",
    "reputation_offence": "defamation",
    "harassment_offence": "harassment",
    "cyber_offence": "cybercrime",
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
            if "trespass" in section_title or "trespass" in tags:
                scores["trespass"] += 4
            if "harassment" in section_title or "modesty" in tags:
                scores["harassment"] += 4
            if "trespass" in section_title or "land" in tags or "illegal entry" in tags:
                scores["trespass"] += 5

        if "electronic crimes" in law_name:
            scores["cybercrime"] += 5
            if "stalking" in section_title or "harassment" in tags:
                scores["harassment"] += 7

        if "criminal procedure" in law_name:
            scores["arrest_detention"] += 5

        if "authority" in section_title or "rank" in tags:
            scores["officer_authority"] += 4

    best_category = max(scores, key=scores.get)

    if scores[best_category] <= 0:
        best_category = "general"

    return {
        "key": best_category,
        "label": str(CATEGORY_CONFIG[best_category]["label"]),
    }
