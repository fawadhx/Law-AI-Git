from app.schemas.legal_source import LegalSourceRecord


LEGAL_SOURCES: list[LegalSourceRecord] = [
    LegalSourceRecord(
        id="ppc-378",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="378",
        section_title="Theft",
        summary=(
            "Theft generally means dishonestly taking movable property out of another "
            "person's possession without that person's consent."
        ),
        excerpt=(
            "Whoever, intending to take dishonestly any movable property out of the "
            "possession of any person without that person's consent, moves that property "
            "in order to such taking, is said to commit theft."
        ),
        citation_label="PPC Section 378",
        tags=["theft", "property", "dishonest taking", "movable property"],
        aliases=["stealing", "stolen property", "mobile snatching"],
        keywords=["property offence", "dishonestly take", "without consent"],
        related_sections=["PPC Section 379"],
        offence_group="property_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-379",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="379",
        section_title="Punishment for theft",
        summary="This provision covers the punishment that may apply when theft is proved.",
        excerpt=(
            "Whoever commits theft shall be punished with imprisonment of either "
            "description for a term which may extend to three years, or with fine, "
            "or with both."
        ),
        citation_label="PPC Section 379",
        tags=["theft", "punishment", "fine", "imprisonment"],
        aliases=["theft penalty", "theft sentence"],
        keywords=["punishment for theft", "fine for theft"],
        related_sections=["PPC Section 378"],
        offence_group="property_offence",
        punishment_summary="The punishment may extend to three years, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-405",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="405",
        section_title="Criminal breach of trust",
        summary=(
            "This provision generally applies when a person entrusted with property or control "
            "over property dishonestly misappropriates it or uses it in violation of law or contract."
        ),
        excerpt=(
            "A person entrusted with property, or with dominion over property, who dishonestly "
            "misappropriates, converts, uses, or disposes of that property in violation of a legal "
            "direction or contract may commit criminal breach of trust."
        ),
        citation_label="PPC Section 405",
        tags=["criminal breach of trust", "entrusted property", "misappropriation", "dishonest use"],
        aliases=["amanat mein khayanat", "breach of trust", "misuse of entrusted property"],
        keywords=["entrusted money", "misappropriation of property", "dishonest conversion"],
        related_sections=["PPC Section 406"],
        offence_group="property_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-406",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="406",
        section_title="Punishment for criminal breach of trust",
        summary=(
            "This provision covers punishment that may apply where criminal breach of trust is established."
        ),
        excerpt=(
            "Whoever commits criminal breach of trust shall be punished with imprisonment "
            "which may extend to seven years, or with fine, or with both."
        ),
        citation_label="PPC Section 406",
        tags=["criminal breach of trust", "punishment", "fine", "imprisonment"],
        aliases=["breach of trust punishment", "amanat mein khayanat saza"],
        keywords=["sentence for breach of trust", "7 years"],
        related_sections=["PPC Section 405"],
        offence_group="property_offence",
        punishment_summary="The punishment may extend to seven years, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-415",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="415",
        section_title="Cheating",
        summary=(
            "Cheating generally involves deceiving a person and thereby dishonestly or fraudulently "
            "inducing delivery of property, consent to retain property, or an act or omission that causes harm."
        ),
        excerpt=(
            "Whoever, by deceiving any person, fraudulently or dishonestly induces that person to deliver "
            "property, to consent to retention of property, or to do or omit something causing harm in body, "
            "mind, reputation, or property, is said to cheat."
        ),
        citation_label="PPC Section 415",
        tags=["cheating", "fraud", "deception", "dishonest inducement"],
        aliases=["fraud", "scam", "dhoka", "property cheating"],
        keywords=["deceiving a person", "false inducement", "fraudulent inducement"],
        related_sections=["PPC Section 417", "PPC Section 420"],
        offence_group="fraud_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-417",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="417",
        section_title="Punishment for cheating",
        summary="This provision covers punishment that may apply where cheating is established.",
        excerpt="Whoever cheats shall be punished according to the punishment clause applicable under law.",
        citation_label="PPC Section 417",
        tags=["cheating", "fraud", "punishment", "sentence"],
        aliases=["cheating punishment", "fraud penalty"],
        keywords=["punishment for cheating", "sentence for fraud"],
        related_sections=["PPC Section 415", "PPC Section 420"],
        offence_group="fraud_offence",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-420",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="420",
        section_title="Cheating and dishonestly inducing delivery of property",
        summary=(
            "This provision generally applies to a more specific and serious form of cheating tied to dishonest "
            "inducement involving property or valuable security."
        ),
        excerpt=(
            "A person who cheats and thereby dishonestly induces the delivery of property or the making, "
            "alteration, or destruction of a valuable security may commit an offence under this section."
        ),
        citation_label="PPC Section 420",
        tags=["cheating", "property fraud", "dishonest inducement", "valuable security"],
        aliases=["420", "section 420", "fraud over property"],
        keywords=["delivery of property", "dishonest inducement", "valuable security"],
        related_sections=["PPC Section 415", "PPC Section 417"],
        offence_group="fraud_offence",
        provision_kind="aggravated_offence",
    ),
    LegalSourceRecord(
        id="ppc-441",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="441",
        section_title="Criminal trespass",
        summary=(
            "Criminal trespass generally involves entering property in another person's possession with intent "
            "to commit an offence, or to intimidate, insult, or annoy the person in possession."
        ),
        excerpt=(
            "Whoever enters into or upon property in the possession of another with intent to commit an offence, "
            "or to intimidate, insult, or annoy any person in possession of such property, or unlawfully remains "
            "there with such intent, commits criminal trespass."
        ),
        citation_label="PPC Section 441",
        tags=["criminal trespass", "property entry", "land dispute", "unlawful entry"],
        aliases=["trespass", "illegal entry", "qabza dispute"],
        keywords=["entering property", "remaining unlawfully", "land entry"],
        related_sections=["PPC Section 447"],
        offence_group="property_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-447",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="447",
        section_title="Punishment for criminal trespass",
        summary=(
            "This provision covers punishment that may apply where criminal trespass is established."
        ),
        excerpt=(
            "Whoever commits criminal trespass shall be punished with imprisonment which may extend to three months, "
            "or with fine, or with both."
        ),
        citation_label="PPC Section 447",
        tags=["criminal trespass", "punishment", "fine", "imprisonment"],
        aliases=["trespass punishment", "illegal entry punishment"],
        keywords=["3 months", "punishment for trespass"],
        related_sections=["PPC Section 441"],
        offence_group="property_offence",
        punishment_summary="The punishment may extend to three months, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-499",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="499",
        section_title="Defamation",
        summary=(
            "Defamation generally concerns making or publishing an imputation about a "
            "person with intent to harm, or knowing it may harm, that person's reputation."
        ),
        excerpt=(
            "Whoever by words either spoken or intended to be read, or by signs or by "
            "visible representations, makes or publishes any imputation concerning any "
            "person intending to harm, or knowing or having reason to believe that such "
            "imputation will harm, the reputation of such person, is said to defame that person."
        ),
        citation_label="PPC Section 499",
        tags=["defamation", "reputation", "spoken words", "published statement"],
        aliases=["badnami", "reputation harm", "false allegation"],
        keywords=["harm reputation", "publish imputation"],
        related_sections=["PPC Section 500"],
        offence_group="reputation_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-500",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="500",
        section_title="Punishment for defamation",
        summary="This provision covers the punishment that may apply in defamation matters.",
        excerpt=(
            "Whoever defames another shall be punished with simple imprisonment for a term "
            "which may extend to two years, or with fine, or with both."
        ),
        citation_label="PPC Section 500",
        tags=["defamation", "punishment", "fine", "simple imprisonment"],
        aliases=["defamation punishment", "badnami saza"],
        keywords=["punishment for defamation", "simple imprisonment"],
        related_sections=["PPC Section 499"],
        offence_group="reputation_offence",
        punishment_summary="The punishment may extend to two years, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-503",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="503",
        section_title="Criminal intimidation",
        summary=(
            "Criminal intimidation generally involves threatening someone with injury to "
            "their person, reputation, or property in order to cause alarm or pressure them."
        ),
        excerpt=(
            "Whoever threatens another with any injury to his person, reputation or property, "
            "or to the person or reputation of anyone in whom that person is interested, with "
            "intent to cause alarm to that person, or to cause that person to do any act which "
            "he is not legally bound to do, or to omit to do any act which that person is legally "
            "entitled to do, as the means of avoiding the execution of such threat, commits criminal intimidation."
        ),
        citation_label="PPC Section 503",
        tags=["threat", "criminal intimidation", "alarm", "reputation", "property"],
        aliases=["death threat", "threatening message", "blackmail threat"],
        keywords=["cause alarm", "threat to reputation", "threat to property"],
        related_sections=["PPC Section 506"],
        offence_group="threat_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-506",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="506",
        section_title="Punishment for criminal intimidation",
        summary=(
            "This provision covers punishment that may apply where criminal intimidation is established."
        ),
        excerpt=(
            "Whoever commits the offence of criminal intimidation shall be punished "
            "according to the terms provided by law."
        ),
        citation_label="PPC Section 506",
        tags=["criminal intimidation", "punishment", "threat", "offence"],
        aliases=["threat punishment", "criminal intimidation sentence"],
        keywords=["punishment for threat", "punishment for intimidation"],
        related_sections=["PPC Section 503"],
        offence_group="threat_offence",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-509",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="509",
        section_title="Insulting modesty or causing sexual harassment",
        summary=(
            "This provision may apply where words, gestures, conduct, or intrusion on privacy are used to insult "
            "the modesty of a woman or amount to sexual harassment."
        ),
        excerpt=(
            "Whoever, intending to insult modesty or cause sexual harassment, uses words, sounds, gestures, "
            "objects, or intrudes upon privacy in a way directed at a woman may commit an offence under this section."
        ),
        citation_label="PPC Section 509",
        tags=["sexual harassment", "insult modesty", "privacy intrusion", "harassment"],
        aliases=["harassment", "sexual harassment", "eve teasing"],
        keywords=["insult modesty", "intrudes upon privacy", "harassing conduct"],
        offence_group="harassment_offence",
        punishment_summary="This section was amended to provide a stronger harassment-focused punishment framework.",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="crpc-46",
        source_title="Code of Criminal Procedure, 1898",
        law_name="Code of Criminal Procedure",
        section_number="46",
        section_title="Arrest how made",
        summary=(
            "This provision concerns the manner in which arrest is to be carried out, including submission to custody "
            "or physical touching or confinement where needed according to law."
        ),
        excerpt=(
            "In making an arrest, the police process concerns the manner in which the person is to be taken into custody "
            "according to law."
        ),
        citation_label="CrPC Section 46",
        tags=["arrest", "custody", "arrest procedure", "police process"],
        aliases=["how arrest is made", "arrest procedure"],
        keywords=["manner of arrest", "taking into custody"],
        offence_group="criminal_procedure",
        provision_kind="procedure",
    ),
    LegalSourceRecord(
        id="crpc-54",
        source_title="Code of Criminal Procedure, 1898",
        law_name="Code of Criminal Procedure",
        section_number="54",
        section_title="When police may arrest without warrant",
        summary=(
            "This provision addresses situations in which police may arrest a person without a warrant."
        ),
        excerpt=(
            "A police officer may, in circumstances provided by law, arrest without an order "
            "from a Magistrate and without a warrant."
        ),
        citation_label="CrPC Section 54",
        tags=["arrest", "without warrant", "police power", "criminal procedure"],
        aliases=["illegal arrest", "warrantless arrest"],
        keywords=["arrest without warrant", "police powers"],
        related_sections=["CrPC Section 46", "CrPC Section 61"],
        offence_group="criminal_procedure",
        provision_kind="procedure",
    ),
    LegalSourceRecord(
        id="crpc-61",
        source_title="Code of Criminal Procedure, 1898",
        law_name="Code of Criminal Procedure",
        section_number="61",
        section_title="Person arrested not to be detained more than twenty-four hours",
        summary=(
            "A person arrested by police should not ordinarily be detained for more than "
            "twenty-four hours without legal authority."
        ),
        excerpt=(
            "No police officer shall detain in custody a person arrested without warrant for a "
            "longer period than under all the circumstances of the case is reasonable, and such "
            "period shall not, in the absence of a special order of a Magistrate, exceed twenty-four hours."
        ),
        citation_label="CrPC Section 61",
        tags=["detention", "24 hours", "custody", "arrest", "rights"],
        aliases=["24 hour rule", "illegal detention"],
        keywords=["detained more than twenty four hours", "custody limit"],
        related_sections=["CrPC Section 54"],
        offence_group="criminal_procedure",
        provision_kind="rights_limit",
    ),
    LegalSourceRecord(
        id="pca-6",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="6",
        section_title="Unauthorised access to information system or data",
        summary=(
            "This provision concerns gaining unauthorised access to an information system or data."
        ),
        excerpt=(
            "A person who gains unauthorized access to any information system or data "
            "may commit an offence under the law."
        ),
        citation_label="PECA Section 6",
        tags=["cybercrime", "unauthorized access", "data", "information system"],
        aliases=["hacking", "account hack", "unauthorised login"],
        keywords=["illegal access to account", "access to system"],
        offence_group="cyber_offence",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="pca-20",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="20",
        section_title="Offences against dignity of a natural person",
        summary=(
            "This provision may apply where online conduct harms the dignity, privacy, or reputation of a person."
        ),
        excerpt=(
            "Whoever intentionally and publicly exhibits or displays or transmits any information "
            "through any information system or device that harms the reputation or privacy of a "
            "natural person may commit an offence under the law."
        ),
        citation_label="PECA Section 20",
        tags=["online harassment", "dignity", "privacy", "reputation", "cyber"],
        aliases=["online defamation", "online privacy harm", "social media humiliation"],
        keywords=["harm online reputation", "online privacy", "dignity online"],
        related_sections=["PPC Section 499", "PECA Section 24"],
        offence_group="cyber_offence",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="pca-21",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="21",
        section_title="Offences against modesty of a natural person and minor",
        summary=(
            "This provision may apply in cases involving online sharing or transmission of "
            "content affecting modesty, including cases involving minors."
        ),
        excerpt=(
            "Whoever intentionally and publicly exhibits or displays or transmits through any "
            "information system any information which superimposes a photograph of the face of a "
            "natural person over any sexually explicit image or video, or includes a minor, may "
            "commit an offence under the law."
        ),
        citation_label="PECA Section 21",
        tags=["modesty", "minor", "image misuse", "online abuse", "cybercrime"],
        aliases=["morphed image", "explicit image misuse", "minor online abuse"],
        keywords=["sexual image", "face superimposition", "minor content misuse"],
        related_sections=["PPC Section 509", "PECA Section 24"],
        offence_group="cyber_offence",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="pca-24",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="24",
        section_title="Cyber stalking",
        summary=(
            "This provision may apply where digital tools, online communication, surveillance, unwanted contact, "
            "or online publication are used to stalk, harass, threaten, monitor, or blackmail a person."
        ),
        excerpt=(
            "A person commits the offence of cyber stalking where online conduct is used to stalk or harass a natural person, "
            "damage reputation, create fear, seek revenge, or blackmail through an information system."
        ),
        citation_label="PECA Section 24",
        tags=["cyber stalking", "online harassment", "blackmail", "monitoring", "revenge"],
        aliases=["cyberstalking", "online stalking", "blackmail online", "revenge posting"],
        keywords=["fake profiles", "repeated unwanted contact", "online monitoring"],
        related_sections=["PECA Section 20", "PECA Section 21", "PPC Section 509"],
        offence_group="cyber_offence",
        provision_kind="offence",
    ),
]
