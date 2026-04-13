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
        offence_group="theft_offence",
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
        offence_group="theft_offence",
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
        offence_group="breach_of_trust_offence",
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
        offence_group="breach_of_trust_offence",
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
        related_sections=["PPC Section 415", "PPC Section 417", "PECA Section 14", "PECA Section 16"],
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
        offence_group="trespass_offence",
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
        offence_group="trespass_offence",
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
        related_sections=["PPC Section 506", "PECA Section 24"],
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
        related_sections=["PPC Section 503", "PECA Section 24"],
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
        aliases=["harassment", "sexual harassment", "eve teasing", "privacy intrusion"],
        keywords=["insult modesty", "intrudes upon privacy", "harassing conduct"],
        related_sections=["PECA Section 24", "PECA Section 20"],
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
        aliases=["how arrest is made", "arrest procedure", "police arrest method"],
        keywords=["manner of arrest", "taking into custody", "how police arrest"],
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
        aliases=["illegal arrest", "warrantless arrest", "can police arrest without warrant", "sho arrest without warrant"],
        keywords=["arrest without warrant", "police powers", "when police may arrest", "officer arrest power"],
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
        aliases=["24 hour rule", "illegal detention", "24 ghantay rule"],
        keywords=["detained more than twenty four hours", "custody limit", "how long police can detain"],
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
        aliases=["cyberstalking", "online stalking", "blackmail online", "revenge posting", "online blackmail"],
        keywords=["fake profiles", "repeated unwanted contact", "online monitoring"],
        related_sections=["PECA Section 20", "PECA Section 21", "PPC Section 509", "PPC Section 503", "PPC Section 506"],
        offence_group="cyber_offence",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="ppc-339",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="339",
        section_title="Wrongful restraint",
        summary=(
            "This provision generally applies where a person is voluntarily obstructed "
            "so that they cannot proceed in a direction in which they have a right to go."
        ),
        excerpt=(
            "Whoever voluntarily obstructs any person so as to prevent that person from "
            "proceeding in any direction in which that person has a right to proceed may "
            "commit wrongful restraint."
        ),
        citation_label="PPC Section 339",
        tags=["wrongful restraint", "blocked way", "obstruction", "forced stop"],
        aliases=["rasta rokna", "prevented from going", "stopped me from leaving"],
        keywords=["blocked path", "prevented movement", "cannot proceed"],
        related_sections=["PPC Section 341", "PPC Section 340"],
        offence_group="restraint_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-341",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="341",
        section_title="Punishment for wrongful restraint",
        summary=(
            "This provision covers punishment that may apply where wrongful restraint is established."
        ),
        excerpt=(
            "Whoever wrongfully restrains any person may be punished with simple imprisonment "
            "for a term which may extend to one month, or with fine, or with both."
        ),
        citation_label="PPC Section 341",
        tags=["wrongful restraint", "punishment", "simple imprisonment", "fine"],
        aliases=["wrongful restraint punishment", "rasta rokna saza"],
        keywords=["one month", "punishment for blocking way"],
        related_sections=["PPC Section 339", "PPC Section 340"],
        offence_group="restraint_offence",
        punishment_summary="The punishment may extend to one month, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-340",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="340",
        section_title="Wrongful confinement",
        summary=(
            "This provision generally applies where a person is wrongfully restrained in a way "
            "that prevents them from moving beyond certain limits."
        ),
        excerpt=(
            "Whoever wrongfully restrains any person in such a manner as to prevent that person "
            "from proceeding beyond certain circumscribing limits may commit wrongful confinement."
        ),
        citation_label="PPC Section 340",
        tags=["wrongful confinement", "locked in", "detained privately", "kept inside"],
        aliases=["band kar dena", "locked me in a room", "confined person"],
        keywords=["prevented from leaving", "circumscribing limits", "kept inside premises"],
        related_sections=["PPC Section 342", "PPC Section 339"],
        offence_group="restraint_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-342",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="342",
        section_title="Punishment for wrongful confinement",
        summary=(
            "This provision covers punishment that may apply where wrongful confinement is established."
        ),
        excerpt=(
            "Whoever wrongfully confines any person may be punished with imprisonment "
            "for a term which may extend to one year, or with fine, or with both."
        ),
        citation_label="PPC Section 342",
        tags=["wrongful confinement", "punishment", "imprisonment", "fine"],
        aliases=["wrongful confinement punishment", "band kar dena saza"],
        keywords=["one year", "punishment for confinement"],
        related_sections=["PPC Section 340", "PPC Section 339"],
        offence_group="restraint_offence",
        punishment_summary="The punishment may extend to one year, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-383",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="383",
        section_title="Extortion",
        summary=(
            "This provision generally applies where a person is intentionally put in fear of injury "
            "and is thereby induced to deliver property, valuable security, or something convertible into value."
        ),
        excerpt=(
            "Whoever intentionally puts any person in fear of injury and thereby dishonestly induces "
            "that person to deliver property or valuable security may commit extortion."
        ),
        citation_label="PPC Section 383",
        tags=["extortion", "fear of injury", "money demand", "property demand"],
        aliases=["bhatta", "blackmail for money", "forced money demand"],
        keywords=["demanding money through threats", "fear-based delivery of property", "ransom-like demand"],
        related_sections=["PPC Section 384", "PPC Section 503"],
        offence_group="violent_property_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-384",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="384",
        section_title="Punishment for extortion",
        summary=(
            "This provision covers punishment that may apply where extortion is established."
        ),
        excerpt=(
            "Whoever commits extortion may be punished with imprisonment "
            "for a term which may extend to three years, or with fine, or with both."
        ),
        citation_label="PPC Section 384",
        tags=["extortion", "punishment", "fine", "imprisonment"],
        aliases=["extortion punishment", "bhatta saza"],
        keywords=["three years", "punishment for extortion"],
        related_sections=["PPC Section 383", "PPC Section 503"],
        offence_group="violent_property_offence",
        punishment_summary="The punishment may extend to three years, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-390",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="390",
        section_title="Robbery",
        summary=(
            "This provision generally applies when theft or extortion is accompanied by immediate violence, "
            "attempted violence, or fear of instant death, hurt, or wrongful restraint."
        ),
        excerpt=(
            "Theft becomes robbery where violence, attempted violence, or fear of instant hurt, death, "
            "or wrongful restraint is used in committing the taking; extortion may also become robbery "
            "where delivery is induced by fear of instant injury in the person's presence."
        ),
        citation_label="PPC Section 390",
        tags=["robbery", "snatching with force", "violent theft", "mugging"],
        aliases=["mugging", "armed snatching", "street robbery", "dacoity-like robbery"],
        keywords=["force during theft", "fear of instant hurt", "snatched at gunpoint"],
        related_sections=["PPC Section 392", "PPC Section 378", "PPC Section 383"],
        offence_group="violent_property_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-392",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="392",
        section_title="Punishment for robbery",
        summary=(
            "This provision covers punishment that may apply where robbery is established."
        ),
        excerpt=(
            "Whoever commits robbery may be punished with rigorous imprisonment for a term "
            "that may extend from three to ten years, and shall also be liable to fine."
        ),
        citation_label="PPC Section 392",
        tags=["robbery", "punishment", "rigorous imprisonment", "fine"],
        aliases=["robbery punishment", "snatching punishment", "mugging punishment"],
        keywords=["three to ten years", "punishment for robbery"],
        related_sections=["PPC Section 390", "PPC Section 378", "PPC Section 383"],
        offence_group="violent_property_offence",
        punishment_summary="The punishment may range from three to ten years and fine.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-425",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="425",
        section_title="Mischief",
        summary=(
            "This provision generally applies where a person causes destruction of property or "
            "changes it in a way that diminishes its value, utility, or causes wrongful loss or damage."
        ),
        excerpt=(
            "Whoever with intent to cause, or knowing that it is likely to cause, wrongful loss or damage "
            "to the public or to any person causes destruction of property or a change that diminishes "
            "its value or utility may commit mischief."
        ),
        citation_label="PPC Section 425",
        tags=["mischief", "property damage", "vandalism", "destruction"],
        aliases=["tod phod", "damage property", "vandalism"],
        keywords=["damaged property", "broke vehicle", "destroyed object"],
        related_sections=["PPC Section 426"],
        offence_group="property_damage_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-426",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="426",
        section_title="Punishment for mischief",
        summary=(
            "This provision covers punishment that may apply where mischief is established."
        ),
        excerpt=(
            "Whoever commits mischief may be punished with imprisonment "
            "for a term which may extend to three months, or with fine, or with both."
        ),
        citation_label="PPC Section 426",
        tags=["mischief", "punishment", "property damage", "fine"],
        aliases=["mischief punishment", "vandalism punishment"],
        keywords=["three months", "punishment for property damage"],
        related_sections=["PPC Section 425"],
        offence_group="property_damage_offence",
        punishment_summary="The punishment may extend to three months, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="pca-13",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="13",
        section_title="Electronic forgery",
        summary=(
            "This provision may apply where digital systems or data are manipulated to create unauthentic "
            "data intended to be acted on as authentic for legal or fraudulent purposes."
        ),
        excerpt=(
            "Whoever uses or interferes with an information system, device, or data to create "
            "unauthentic data intended to be considered or acted upon as authentic may commit electronic forgery."
        ),
        citation_label="PECA Section 13",
        tags=["electronic forgery", "fake digital document", "forged data", "cyber forgery"],
        aliases=["fake screenshot", "fake digital record", "forged online document"],
        keywords=["forged pdf", "edited digital evidence", "fake digital document"],
        related_sections=["PECA Section 14", "PECA Section 16"],
        offence_group="cyber_identity_offence",
        punishment_summary="The punishment may extend to three years, fine, or both.",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="pca-14",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="14",
        section_title="Electronic fraud",
        summary=(
            "This provision may apply where a person uses an information system, device, or data "
            "for wrongful gain, deception, or inducing another person into a harmful relationship or transaction."
        ),
        excerpt=(
            "Whoever with intent for wrongful gain uses an information system, device, or data or deceives any person "
            "through such means in a way likely to cause harm may commit electronic fraud."
        ),
        citation_label="PECA Section 14",
        tags=["electronic fraud", "online scam", "digital deception", "cyber fraud"],
        aliases=["online fraud", "fake website scam", "banking scam", "otp scam"],
        keywords=["fraudulent website", "digital scam", "wrongful gain online"],
        related_sections=["PECA Section 13", "PECA Section 16", "PPC Section 420"],
        offence_group="cyber_identity_offence",
        punishment_summary="The punishment may extend to two years, fine, or both.",
        provision_kind="offence",
    ),
    LegalSourceRecord(
        id="pca-16",
        source_title="Prevention of Electronic Crimes Act, 2016",
        law_name="Prevention of Electronic Crimes Act",
        section_number="16",
        section_title="Unauthorized use of identity information",
        summary=(
            "This provision may apply where another person's identity information is obtained, sold, "
            "possessed, transmitted, or used without authorization."
        ),
        excerpt=(
            "Whoever obtains, sells, possesses, transmits, or uses another person's identity information "
            "without authorization may commit an offence under this section."
        ),
        citation_label="PECA Section 16",
        tags=["identity information", "identity theft", "cnic misuse", "impersonation"],
        aliases=["identity theft", "cnic used", "fake profile using my identity"],
        keywords=["unauthorized identity use", "my cnic", "my documents used"],
        related_sections=["PECA Section 13", "PECA Section 14", "PECA Section 20", "PPC Section 420"],
        offence_group="cyber_identity_offence",
        punishment_summary="The punishment may extend to three years or fine up to five million rupees, or both.",
        provision_kind="offence",
    ),

    LegalSourceRecord(
        id="ppc-351",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="351",
        section_title="Assault",
        summary=(
            "This provision generally covers gestures or preparations that create an apprehension "
            "of immediate criminal force in the mind of another person."
        ),
        excerpt=(
            "Whoever makes a gesture, or preparation, intending or knowing it to be likely that such "
            "gesture or preparation will cause another person present to apprehend that criminal force "
            "is about to be used against that person, may commit assault."
        ),
        citation_label="PPC Section 351",
        tags=["assault", "criminal force", "attack", "gesture causing apprehension"],
        aliases=["slap threat", "push attack", "physical assault", "maar peet", "attack"],
        keywords=["slapped me", "pushed me", "raised hand", "tried to hit"],
        related_sections=["PPC Section 352"],
        offence_group="assault_offence",
        provision_kind="definition",
    ),
    LegalSourceRecord(
        id="ppc-352",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="352",
        section_title="Punishment for assault or criminal force otherwise than on grave provocation",
        summary=(
            "This provision covers punishment that may apply where assault or criminal force is established "
            "and no more specific aggravated section is the better fit."
        ),
        excerpt=(
            "Whoever assaults or uses criminal force to any person, otherwise than on grave and sudden "
            "provocation, may be punished with short imprisonment, fine, or both."
        ),
        citation_label="PPC Section 352",
        tags=["assault", "criminal force", "punishment", "physical attack"],
        aliases=["assault punishment", "criminal force punishment"],
        keywords=["punishment for assault", "saza for assault", "slap punishment"],
        related_sections=["PPC Section 351", "PPC Section 354"],
        offence_group="assault_offence",
        punishment_summary="The section provides punishment for assault or criminal force through short imprisonment, fine, or both.",
        provision_kind="punishment",
    ),
    LegalSourceRecord(
        id="ppc-354",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="354",
        section_title="Assault or criminal force to woman with intent to outrage her modesty",
        summary=(
            "This provision generally applies where assault or criminal force is used against a woman "
            "with intent to outrage, or with knowledge that it is likely to outrage, her modesty."
        ),
        excerpt=(
            "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be "
            "likely that thereby her modesty will be outraged, may commit an offence under this section."
        ),
        citation_label="PPC Section 354",
        tags=["woman", "modesty", "sexual harassment", "criminal force", "assault"],
        aliases=["touching woman", "grabbed a woman", "outrage modesty", "molestation"],
        keywords=["touched her inappropriately", "grabbed her", "physical sexual harassment"],
        related_sections=["PPC Section 509", "PPC Section 352"],
        offence_group="harassment_offence",
        punishment_summary="The punishment may extend to two years, or fine, or both.",
        provision_kind="aggravated_offence",
    ),
    LegalSourceRecord(
        id="ppc-442",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="442",
        section_title="House-trespass",
        summary=(
            "This provision generally applies where criminal trespass takes place by entering into or "
            "remaining in a building, tent, or vessel used as a human dwelling, place of worship, or "
            "place for custody of property."
        ),
        excerpt=(
            "Whoever commits criminal trespass by entering into or remaining in any building, tent, or vessel "
            "used as a human dwelling, or any building used as a place for worship or for custody of property, "
            "is said to commit house-trespass."
        ),
        citation_label="PPC Section 442",
        tags=["house trespass", "home entry", "illegal house entry", "home invasion"],
        aliases=["entered my house", "entered my home", "broke into house", "ghar mein ghus gaya"],
        keywords=["house entry", "home intrusion", "break into my home"],
        related_sections=["PPC Section 448", "PPC Section 441"],
        offence_group="trespass_offence",
        provision_kind="aggravated_offence",
    ),
    LegalSourceRecord(
        id="ppc-448",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="448",
        section_title="Punishment for house-trespass",
        summary="This provision covers punishment that may apply where house-trespass is established.",
        excerpt=(
            "Whoever commits house-trespass may be punished with imprisonment which may extend to one year, "
            "or with fine, or with both."
        ),
        citation_label="PPC Section 448",
        tags=["house trespass", "punishment", "home invasion", "illegal house entry"],
        aliases=["house trespass punishment", "home trespass punishment"],
        keywords=["punishment for house trespass", "section 448", "break into house punishment"],
        related_sections=["PPC Section 442", "PPC Section 441", "PPC Section 447"],
        offence_group="trespass_offence",
        punishment_summary="The punishment may extend to one year, fine, or both.",
        provision_kind="punishment",
    ),

]
