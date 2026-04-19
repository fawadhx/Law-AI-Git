from app.data.federal_catalog.common import build_federal_record


PECA_RECORDS = [
    build_federal_record(
        law_key="peca",
        record_id="pca-6",
        section_number="6",
        section_title="Unauthorized access to information system or data",
        summary=(
            "This section generally covers unauthorized access to an information system or data."
        ),
        tags=["unauthorized access", "cyber access", "data access", "hacking"],
        aliases=["hacked account", "unauthorized login", "accessed my data"],
        keywords=["unauthorized access to data", "information system access", "cyber intrusion"],
        related_sections=["PECA Section 13", "PECA Section 14"],
        offence_group="cyber_access_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-13",
        section_number="13",
        section_title="Electronic forgery",
        summary=(
            "This provision generally applies where electronic records or data are dishonestly manipulated to create a false digital document or record."
        ),
        tags=["electronic forgery", "fake digital record", "cyber forgery"],
        aliases=["fake digital document", "forged online record", "electronic forgery"],
        keywords=["electronic forgery", "fake digital record", "altered electronic document"],
        related_sections=["PECA Section 14", "PECA Section 16"],
        offence_group="cyber_forgery_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-14",
        section_number="14",
        section_title="Electronic fraud",
        summary=(
            "This provision generally applies where electronic or online means are used fraudulently to obtain benefit or cause loss."
        ),
        tags=["electronic fraud", "online fraud", "cyber scam"],
        aliases=["online scam", "cyber fraud", "electronic cheating"],
        keywords=["electronic fraud", "online cheating", "digital scam"],
        related_sections=["PECA Section 13", "PECA Section 16", "PPC Section 420"],
        offence_group="cyber_fraud_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-16",
        section_number="16",
        section_title="Unauthorized use of identity information",
        summary=(
            "This provision generally covers unauthorized use, sale, possession, or transmission of another person's identity information."
        ),
        tags=["identity information", "impersonation", "cyber identity misuse"],
        aliases=["used my identity", "impersonation online", "identity misuse"],
        keywords=["unauthorized use of identity information", "identity theft", "used my cnic online"],
        related_sections=["PECA Section 13", "PECA Section 14"],
        offence_group="cyber_identity_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-20",
        section_number="20",
        section_title="Offences against dignity of a natural person",
        summary=(
            "This section generally covers online or electronic acts affecting dignity, including harmful dissemination or transmission in specified circumstances."
        ),
        tags=["online dignity", "harassment", "defamation online"],
        aliases=["online dignity offence", "posted online to humiliate", "digital harassment"],
        keywords=["offence against dignity", "harmful online post", "online humiliation"],
        related_sections=["PECA Section 21", "PPC Section 499"],
        offence_group="cyber_harassment_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-21",
        section_number="21",
        section_title="Offences against modesty of a natural person and minor",
        summary=(
            "This section generally addresses online acts affecting modesty, including transmission, display, or sharing in prohibited circumstances."
        ),
        tags=["online modesty", "cyber harassment", "minor protection", "privacy abuse"],
        aliases=["shared my photo", "online modesty offence", "cyber harassment of woman"],
        keywords=["offence against modesty", "shared image online", "minor online abuse"],
        related_sections=["PECA Section 20", "PPC Section 509"],
        offence_group="cyber_harassment_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="peca",
        record_id="pca-24",
        section_number="24",
        section_title="Cyber stalking",
        summary=(
            "This section generally covers repeated or harmful electronic conduct amounting to cyber stalking."
        ),
        tags=["cyber stalking", "online harassment", "repeated contact"],
        aliases=["stalking online", "cyber stalking", "keeps messaging and threatening online"],
        keywords=["cyber stalking", "repeated online contact", "online surveillance harassment"],
        related_sections=["PECA Section 20", "PECA Section 21", "PPC Section 503"],
        offence_group="cyber_harassment_offence",
        provision_kind="offence",
    ),
]
