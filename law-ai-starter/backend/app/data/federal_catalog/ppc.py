from app.data.federal_catalog.common import build_federal_record


PPC_RECORDS = [
    build_federal_record(
        law_key="ppc",
        record_id="ppc-34",
        section_number="34",
        section_title="Acts done by several persons in furtherance of common intention",
        summary=(
            "This section is commonly used where more than one person is treated as sharing liability because the act was done in furtherance of a common intention."
        ),
        tags=["common intention", "joint liability", "multiple accused"],
        aliases=["common intention", "mil kar jurm", "shared plan"],
        keywords=["several persons", "joint act", "shared intention"],
        related_sections=["PPC Section 109", "PPC Section 120B"],
        offence_group="joint_liability",
        provision_kind="general",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-107",
        section_number="107",
        section_title="Abetment of a thing",
        summary=(
            "This section gives the general concept of abetment, including instigating a person, engaging in conspiracy, or intentionally aiding the act."
        ),
        tags=["abetment", "instigation", "aiding offence"],
        aliases=["u ksana", "instigate crime", "madad ki jurm mein"],
        keywords=["abetment definition", "instigation", "intentional aid"],
        related_sections=["PPC Section 109", "PPC Section 120B"],
        offence_group="abetment_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-109",
        section_number="109",
        section_title="Punishment of abetment if the act abetted is committed",
        summary=(
            "This section generally applies where abetment is proved and the act that was abetted is actually committed, subject to the structure of the Code."
        ),
        tags=["abetment", "punishment", "instigation liability"],
        aliases=["punishment for abetment", "abetment saza"],
        keywords=["abetment punishment", "instigated offence", "aided offence punishment"],
        related_sections=["PPC Section 107", "PPC Section 34"],
        offence_group="abetment_offence",
        punishment_summary="Where the abetted act is committed, punishment may follow the applicable abetment framework in the Code.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-120b",
        section_number="120B",
        section_title="Punishment of criminal conspiracy",
        summary=(
            "This section covers punishment consequences where criminal conspiracy is established under the Code."
        ),
        tags=["criminal conspiracy", "agreement to commit offence", "punishment"],
        aliases=["saazish", "criminal conspiracy punishment"],
        keywords=["conspiracy punishment", "planned offence", "agreement to commit crime"],
        related_sections=["PPC Section 34", "PPC Section 107"],
        offence_group="conspiracy_offence",
        punishment_summary="Punishment depends on the nature of the conspiracy and the offence involved under the Code.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-141",
        section_number="141",
        section_title="Unlawful assembly",
        summary=(
            "This section gives the general framework for when an assembly of persons becomes unlawful because of a prohibited common object."
        ),
        tags=["unlawful assembly", "public order", "common object"],
        aliases=["illegal gathering", "mob gathering", "ghair qanooni ijtima"],
        keywords=["unlawful assembly definition", "common object", "public disorder gathering"],
        related_sections=["PPC Section 143", "PPC Section 149"],
        offence_group="public_order_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-143",
        section_number="143",
        section_title="Punishment for member of an unlawful assembly",
        summary=(
            "This section covers punishment that may apply to a person who is proved to be a member of an unlawful assembly."
        ),
        tags=["unlawful assembly", "public order", "punishment"],
        aliases=["unlawful assembly punishment", "illegal gathering punishment"],
        keywords=["member of unlawful assembly", "punishment for assembly", "mob case punishment"],
        related_sections=["PPC Section 141", "PPC Section 149"],
        offence_group="public_order_offence",
        punishment_summary="This section provides punishment for membership in an unlawful assembly.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-146",
        section_number="146",
        section_title="Rioting",
        summary=(
            "This section generally describes rioting in the context of unlawful assembly and the use of force or violence by the assembly or any member of it."
        ),
        tags=["rioting", "public disorder", "violence by assembly"],
        aliases=["riot", "hungama", "rioting definition"],
        keywords=["rioting meaning", "violent assembly", "mob violence"],
        related_sections=["PPC Section 141", "PPC Section 147"],
        offence_group="public_order_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-147",
        section_number="147",
        section_title="Punishment for rioting",
        summary=(
            "This section covers punishment consequences where rioting is established."
        ),
        tags=["rioting", "punishment", "public disorder"],
        aliases=["riot punishment", "rioting saza"],
        keywords=["punishment for rioting", "mob violence punishment"],
        related_sections=["PPC Section 146", "PPC Section 149"],
        offence_group="public_order_offence",
        punishment_summary="This section provides punishment where rioting is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-149",
        section_number="149",
        section_title="Every member of unlawful assembly guilty of offence committed in prosecution of common object",
        summary=(
            "This section is commonly used to extend liability where an offence is committed by a member of an unlawful assembly in prosecution of the common object."
        ),
        tags=["common object", "unlawful assembly", "joint liability"],
        aliases=["common object liability", "mob liability"],
        keywords=["every member guilty", "assembly liability", "common object offence"],
        related_sections=["PPC Section 141", "PPC Section 147"],
        offence_group="public_order_offence",
        provision_kind="general",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-182",
        section_number="182",
        section_title="False information, with intent to cause public servant to use lawful power to the injury of another person",
        summary=(
            "This section generally covers false information given to a public servant with the intent of causing the lawful power of that public servant to be used to another person's injury."
        ),
        tags=["false information", "public servant", "misuse of process"],
        aliases=["false complaint to police", "jhooti ittila", "wrong information to officer"],
        keywords=["false info to public servant", "misleading police", "false accusation through complaint"],
        related_sections=["PPC Section 211"],
        offence_group="false_reporting_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-186",
        section_number="186",
        section_title="Obstructing public servant in discharge of public functions",
        summary=(
            "This section generally applies where a person voluntarily obstructs a public servant while that public servant is discharging public functions."
        ),
        tags=["obstructing public servant", "public functions", "police obstruction"],
        aliases=["rukawat public servant", "obstructing officer", "police obstruction"],
        keywords=["obstruct public servant", "interfere with official duty", "stop police from work"],
        related_sections=["PPC Section 189"],
        offence_group="public_servant_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-211",
        section_number="211",
        section_title="False charge of offence made with intent to injure",
        summary=(
            "This section generally covers instituting or causing a false criminal charge with intent to injure another person."
        ),
        tags=["false charge", "malicious complaint", "injury through false accusation"],
        aliases=["jhoota muqadma", "false criminal case", "malicious prosecution style complaint"],
        keywords=["false charge of offence", "wrongly accused", "fabricated criminal allegation"],
        related_sections=["PPC Section 182"],
        offence_group="false_reporting_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-279",
        section_number="279",
        section_title="Rash driving or riding on a public way",
        summary=(
            "This section generally covers rash or negligent driving or riding on a public way where the conduct endangers human life or is likely to cause hurt or injury."
        ),
        tags=["rash driving", "public safety", "negligent driving"],
        aliases=["rash driving", "dangerous driving", "speeding dangerously"],
        keywords=["public way driving", "reckless driving", "hit due to rash driving"],
        related_sections=[],
        offence_group="public_safety_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-339",
        section_number="339",
        section_title="Wrongful restraint",
        summary=(
            "This provision generally applies where a person is voluntarily obstructed so as to prevent movement in a direction in which that person has a right to proceed."
        ),
        excerpt=(
            "A person may commit wrongful restraint where another is voluntarily obstructed and prevented from proceeding in a direction in which there is a right to proceed."
        ),
        tags=["wrongful restraint", "obstruction", "movement restriction"],
        aliases=["rasta roka", "blocked my way", "prevented me from going"],
        keywords=["stop someone from going", "restrained movement", "blocked road"],
        related_sections=["PPC Section 341", "PPC Section 340"],
        offence_group="restraint_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-340",
        section_number="340",
        section_title="Wrongful confinement",
        summary=(
            "This provision generally applies where wrongful restraint goes further and a person is kept within circumscribed limits so movement outside those limits is prevented."
        ),
        excerpt=(
            "A person may commit wrongful confinement where another is wrongfully restrained in such a manner as to prevent proceeding beyond certain circumscribed limits."
        ),
        tags=["wrongful confinement", "kept locked", "illegal confinement"],
        aliases=["band kar diya", "locked me in", "illegal confinement"],
        keywords=["kept in room", "could not leave", "confined person"],
        related_sections=["PPC Section 342", "PPC Section 339"],
        offence_group="confinement_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-341",
        section_number="341",
        section_title="Punishment for wrongful restraint",
        summary=(
            "This provision covers punishment that may apply where wrongful restraint is established."
        ),
        excerpt="This provision covers punishment that may apply where wrongful restraint is established.",
        tags=["wrongful restraint", "punishment", "obstruction"],
        aliases=["punishment for wrongful restraint", "rasta rokna saza"],
        keywords=["section 341", "restraint punishment"],
        related_sections=["PPC Section 339", "PPC Section 342"],
        offence_group="restraint_offence",
        punishment_summary="This section provides punishment where wrongful restraint is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-342",
        section_number="342",
        section_title="Punishment for wrongful confinement",
        summary=(
            "This provision covers punishment that may apply where wrongful confinement is established."
        ),
        excerpt="This provision covers punishment that may apply where wrongful confinement is established.",
        tags=["wrongful confinement", "punishment", "illegal detention by private person"],
        aliases=["punishment for wrongful confinement", "band karna saza"],
        keywords=["section 342", "confinement punishment"],
        related_sections=["PPC Section 340", "PPC Section 341"],
        offence_group="confinement_offence",
        punishment_summary="This section provides punishment where wrongful confinement is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-351",
        section_number="351",
        section_title="Assault",
        summary=(
            "This provision generally covers gestures or preparations that create an apprehension of immediate criminal force in the mind of another person."
        ),
        excerpt=(
            "Whoever makes a gesture, or preparation, intending or knowing it to be likely that such gesture or preparation will cause another person present to apprehend that criminal force is about to be used against that person, may commit assault."
        ),
        tags=["assault", "criminal force", "attack", "gesture causing apprehension"],
        aliases=["slap threat", "push attack", "physical assault", "maar peet", "attack"],
        keywords=["slapped me", "pushed me", "raised hand", "tried to hit"],
        related_sections=["PPC Section 352"],
        offence_group="assault_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-352",
        section_number="352",
        section_title="Punishment for assault or criminal force otherwise than on grave provocation",
        summary=(
            "This provision covers punishment that may apply where assault or criminal force is established and no more specific aggravated section is the better fit."
        ),
        excerpt=(
            "Whoever assaults or uses criminal force to any person, otherwise than on grave and sudden provocation, may be punished with short imprisonment, fine, or both."
        ),
        tags=["assault", "criminal force", "punishment", "physical attack"],
        aliases=["assault punishment", "criminal force punishment"],
        keywords=["punishment for assault", "saza for assault", "slap punishment"],
        related_sections=["PPC Section 351", "PPC Section 354"],
        offence_group="assault_offence",
        punishment_summary="The section provides punishment for assault or criminal force through short imprisonment, fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-354",
        section_number="354",
        section_title="Assault or criminal force to woman with intent to outrage her modesty",
        summary=(
            "This provision generally applies where assault or criminal force is used against a woman with intent to outrage, or with knowledge that it is likely to outrage, her modesty."
        ),
        excerpt=(
            "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that thereby her modesty will be outraged, may commit an offence under this section."
        ),
        tags=["woman", "modesty", "sexual harassment", "criminal force", "assault"],
        aliases=["touching woman", "grabbed a woman", "outrage modesty", "molestation"],
        keywords=["touched her inappropriately", "grabbed her", "physical sexual harassment"],
        related_sections=["PPC Section 509", "PPC Section 352"],
        offence_group="harassment_offence",
        punishment_summary="The punishment may extend to two years, or fine, or both.",
        provision_kind="aggravated_offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-378",
        section_number="378",
        section_title="Theft",
        summary=(
            "Theft generally means dishonestly taking movable property out of another person's possession without that person's consent."
        ),
        excerpt=(
            "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft."
        ),
        tags=["theft", "property", "dishonest taking", "movable property"],
        aliases=["stealing", "stolen property", "mobile snatching"],
        keywords=["property offence", "dishonestly take", "without consent"],
        related_sections=["PPC Section 379"],
        offence_group="theft_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-379",
        section_number="379",
        section_title="Punishment for theft",
        summary="This provision covers the punishment that may apply when theft is proved.",
        excerpt=(
            "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both."
        ),
        tags=["theft", "punishment", "fine", "imprisonment"],
        aliases=["theft penalty", "theft sentence"],
        keywords=["punishment for theft", "fine for theft"],
        related_sections=["PPC Section 378"],
        offence_group="theft_offence",
        punishment_summary="The punishment may extend to three years, fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-383",
        section_number="383",
        section_title="Extortion",
        summary=(
            "This provision generally applies where a person intentionally puts another in fear of injury in order to dishonestly obtain property or valuable security."
        ),
        excerpt=(
            "Extortion generally involves intentionally putting a person in fear of injury and thereby dishonestly inducing delivery of property or valuable security."
        ),
        tags=["extortion", "fear of injury", "property demand", "money by threat"],
        aliases=["bhatta", "extortion demand", "money by threat"],
        keywords=["threatened for money", "fear of injury", "demanded money"],
        related_sections=["PPC Section 384", "PPC Section 503"],
        offence_group="extortion_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-384",
        section_number="384",
        section_title="Punishment for extortion",
        summary=(
            "This provision covers punishment that may apply where extortion is established."
        ),
        excerpt="This provision covers punishment that may apply where extortion is established.",
        tags=["extortion", "punishment", "money by threat"],
        aliases=["extortion punishment", "bhatta saza"],
        keywords=["punishment for extortion", "section 384"],
        related_sections=["PPC Section 383", "PPC Section 503"],
        offence_group="extortion_offence",
        punishment_summary="The punishment may extend to three years, or fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-390",
        section_number="390",
        section_title="Robbery",
        summary=(
            "This provision generally explains when theft or extortion becomes robbery because of accompanying violence, attempted violence, or fear of instant death, hurt, or wrongful restraint."
        ),
        excerpt=(
            "Robbery generally covers theft or extortion aggravated by violence, attempted violence, or fear of instant harm or restraint."
        ),
        tags=["robbery", "violence", "theft with force", "snatching with violence"],
        aliases=["robbery definition", "dacoity type robbery", "snatching by force"],
        keywords=["robbery meaning", "stolen by force", "fear of instant hurt"],
        related_sections=["PPC Section 392", "PPC Section 383", "PPC Section 378"],
        offence_group="robbery_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-392",
        section_number="392",
        section_title="Punishment for robbery",
        summary=(
            "This provision covers punishment that may apply where robbery is established."
        ),
        excerpt="This provision covers punishment that may apply where robbery is established.",
        tags=["robbery", "punishment", "violent theft"],
        aliases=["robbery punishment", "saza for robbery"],
        keywords=["punishment for robbery", "section 392"],
        related_sections=["PPC Section 390"],
        offence_group="robbery_offence",
        punishment_summary="This section provides punishment where robbery is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-405",
        section_number="405",
        section_title="Criminal breach of trust",
        summary=(
            "This provision generally applies when a person entrusted with property or control over property dishonestly misappropriates it or uses it in violation of law or contract."
        ),
        excerpt=(
            "A person entrusted with property, or with dominion over property, who dishonestly misappropriates, converts, uses, or disposes of that property in violation of a legal direction or contract may commit criminal breach of trust."
        ),
        tags=["criminal breach of trust", "entrusted property", "misappropriation", "dishonest use"],
        aliases=["amanat mein khayanat", "breach of trust", "misuse of entrusted property"],
        keywords=["entrusted money", "misappropriation of property", "dishonest conversion"],
        related_sections=["PPC Section 406"],
        offence_group="breach_of_trust_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-406",
        section_number="406",
        section_title="Punishment for criminal breach of trust",
        summary=(
            "This provision covers punishment that may apply where criminal breach of trust is established."
        ),
        tags=["criminal breach of trust", "punishment", "entrusted property", "fine"],
        aliases=["amanat mein khayanat ki saza", "breach of trust punishment"],
        keywords=["punishment for breach of trust", "section 406"],
        related_sections=["PPC Section 405"],
        offence_group="breach_of_trust_offence",
        punishment_summary="The punishment may extend to seven years, fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-415",
        section_number="415",
        section_title="Cheating",
        summary=(
            "This provision generally applies where a person deceives another and dishonestly or fraudulently induces delivery of property, consent, or conduct causing damage."
        ),
        excerpt=(
            "Cheating generally involves deception that dishonestly or fraudulently induces a person to deliver property, consent, or act in a manner causing harm."
        ),
        tags=["cheating", "deception", "dishonest inducement", "fraud"],
        aliases=["fraud", "dhoka", "cheating definition"],
        keywords=["dishonest inducement", "deceived me", "fraudulent representation"],
        related_sections=["PPC Section 417", "PPC Section 420"],
        offence_group="fraud_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-417",
        section_number="417",
        section_title="Punishment for cheating",
        summary=(
            "This provision covers punishment that may apply where cheating is established."
        ),
        excerpt="This provision covers punishment that may apply where cheating is established.",
        tags=["cheating", "punishment", "fraud"],
        aliases=["cheating punishment", "dhoka saza"],
        keywords=["punishment for cheating", "section 417"],
        related_sections=["PPC Section 415", "PPC Section 420"],
        offence_group="fraud_offence",
        punishment_summary="The punishment may extend to one year, or fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-420",
        section_number="420",
        section_title="Cheating and dishonestly inducing delivery of property",
        summary=(
            "This section generally applies where cheating leads to dishonest inducement for delivery of property or alteration of a valuable security."
        ),
        excerpt=(
            "This section generally covers aggravated cheating linked to dishonest inducement involving property or valuable security."
        ),
        tags=["cheating", "delivery of property", "fraud", "valuable security"],
        aliases=["420", "section 420", "property fraud"],
        keywords=["dishonestly induced property", "fraud for money", "cheating for property"],
        related_sections=["PPC Section 415", "PPC Section 417"],
        offence_group="fraud_offence",
        punishment_summary="The punishment may extend to seven years and fine.",
        provision_kind="aggravated_offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-425",
        section_number="425",
        section_title="Mischief",
        summary=(
            "This provision generally covers causing wrongful loss or damage by destroying property or changing it so as to diminish its value or utility."
        ),
        excerpt=(
            "Mischief generally covers intentional acts causing wrongful loss or damage by destroying or changing property."
        ),
        tags=["mischief", "property damage", "wrongful loss"],
        aliases=["damage property", "tor phor", "destroyed my property"],
        keywords=["wrongful loss", "property damaged", "destroyed item"],
        related_sections=["PPC Section 426", "PPC Section 427"],
        offence_group="mischief_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-426",
        section_number="426",
        section_title="Punishment for mischief",
        summary=(
            "This provision covers punishment that may apply where basic mischief is established."
        ),
        excerpt="This provision covers punishment that may apply where basic mischief is established.",
        tags=["mischief", "punishment", "property damage"],
        aliases=["mischief punishment", "property damage punishment"],
        keywords=["punishment for mischief", "section 426"],
        related_sections=["PPC Section 425", "PPC Section 427"],
        offence_group="mischief_offence",
        punishment_summary="This section provides punishment where mischief is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-427",
        section_number="427",
        section_title="Mischief causing damage",
        summary=(
            "This section generally covers mischief involving a specified level of property damage and is commonly referenced where more than minor property loss is alleged."
        ),
        tags=["mischief", "property damage", "damage threshold"],
        aliases=["major property damage", "damage caused to property"],
        keywords=["mischief causing damage", "section 427", "serious property loss"],
        related_sections=["PPC Section 425", "PPC Section 426"],
        offence_group="mischief_offence",
        punishment_summary="This section provides punishment where mischief causes the specified level of damage.",
        provision_kind="aggravated_offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-441",
        section_number="441",
        section_title="Criminal trespass",
        summary=(
            "This provision generally applies where a person enters or remains on property with intent to commit an offence, intimidate, insult, or annoy the person in possession."
        ),
        excerpt=(
            "Criminal trespass generally involves entering or remaining on property with prohibited intent connected to offence, intimidation, insult, or annoyance."
        ),
        tags=["criminal trespass", "property entry", "illegal entry", "land dispute"],
        aliases=["trespass", "illegal entry", "ghair qanooni dakhla"],
        keywords=["entered my plot", "came onto property", "illegal land entry"],
        related_sections=["PPC Section 447", "PPC Section 442"],
        offence_group="trespass_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-442",
        section_number="442",
        section_title="House-trespass",
        summary=(
            "This provision generally applies where criminal trespass takes place by entering into or remaining in a building, tent, or vessel used as a human dwelling, place of worship, or place for custody of property."
        ),
        excerpt=(
            "Whoever commits criminal trespass by entering into or remaining in any building, tent, or vessel used as a human dwelling, or any building used as a place for worship or for custody of property, is said to commit house-trespass."
        ),
        tags=["house trespass", "home entry", "illegal house entry", "home invasion"],
        aliases=["entered my house", "entered my home", "broke into house", "ghar mein ghus gaya"],
        keywords=["house entry", "home intrusion", "break into my home"],
        related_sections=["PPC Section 448", "PPC Section 441"],
        offence_group="trespass_offence",
        provision_kind="aggravated_offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-447",
        section_number="447",
        section_title="Punishment for criminal trespass",
        summary=(
            "This provision covers punishment that may apply where criminal trespass is established."
        ),
        excerpt="This provision covers punishment that may apply where criminal trespass is established.",
        tags=["criminal trespass", "punishment", "illegal entry"],
        aliases=["criminal trespass punishment", "section 447"],
        keywords=["punishment for trespass", "illegal entry punishment"],
        related_sections=["PPC Section 441", "PPC Section 448"],
        offence_group="trespass_offence",
        punishment_summary="The punishment may extend to three months, or fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-448",
        section_number="448",
        section_title="Punishment for house-trespass",
        summary="This provision covers punishment that may apply where house-trespass is established.",
        excerpt=(
            "Whoever commits house-trespass may be punished with imprisonment which may extend to one year, or with fine, or with both."
        ),
        tags=["house trespass", "punishment", "home invasion", "illegal house entry"],
        aliases=["house trespass punishment", "home trespass punishment"],
        keywords=["punishment for house trespass", "section 448", "break into house punishment"],
        related_sections=["PPC Section 442", "PPC Section 441", "PPC Section 447"],
        offence_group="trespass_offence",
        punishment_summary="The punishment may extend to one year, fine, or both.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-499",
        section_number="499",
        section_title="Defamation",
        summary=(
            "This provision generally applies where words, signs, or visible representations are used to harm the reputation of a person, subject to statutory exceptions."
        ),
        excerpt=(
            "Defamation generally concerns imputations made by words, signs, or visible representations intending to harm or knowing it to be likely to harm reputation, subject to exceptions."
        ),
        tags=["defamation", "reputation", "false accusation", "public statement"],
        aliases=["badnami", "defame", "character assassination"],
        keywords=["harmed my reputation", "false statement", "public allegation"],
        related_sections=["PPC Section 500"],
        offence_group="defamation_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-500",
        section_number="500",
        section_title="Punishment for defamation",
        summary=(
            "This provision covers punishment that may apply where defamation is established."
        ),
        excerpt="This provision covers punishment that may apply where defamation is established.",
        tags=["defamation", "punishment", "reputation"],
        aliases=["defamation punishment", "badnami ki saza"],
        keywords=["punishment for defamation", "section 500"],
        related_sections=["PPC Section 499"],
        offence_group="defamation_offence",
        punishment_summary="This section provides punishment where defamation is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-503",
        section_number="503",
        section_title="Criminal intimidation",
        summary=(
            "This provision generally applies where a person threatens injury to body, reputation, or property with intent to cause alarm or compel action or inaction."
        ),
        excerpt=(
            "Criminal intimidation generally covers threats of injury intended to cause alarm or compel a person to do or omit an act."
        ),
        tags=["criminal intimidation", "threat", "fear", "coercion"],
        aliases=["dhamki", "threatened me", "intimidation"],
        keywords=["threat to body", "threat to reputation", "threat to property"],
        related_sections=["PPC Section 506", "PPC Section 384"],
        offence_group="threat_offence",
        provision_kind="definition",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-504",
        section_number="504",
        section_title="Intentional insult with intent to provoke breach of the peace",
        summary=(
            "This section generally covers intentional insult where the insult is intended, or known to be likely, to provoke a person into breaking the peace or committing another offence."
        ),
        tags=["intentional insult", "breach of peace", "provocation"],
        aliases=["provoked fight", "gaali de kar larai", "intentional insult"],
        keywords=["intent to provoke breach of peace", "abusive provocation", "insult leading to violence"],
        related_sections=["PPC Section 503", "PPC Section 506"],
        offence_group="public_order_offence",
        provision_kind="offence",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-506",
        section_number="506",
        section_title="Punishment for criminal intimidation",
        summary=(
            "This provision covers punishment that may apply where criminal intimidation is established."
        ),
        excerpt="This provision covers punishment that may apply where criminal intimidation is established.",
        tags=["criminal intimidation", "punishment", "threat"],
        aliases=["threat punishment", "dhamki ki saza"],
        keywords=["punishment for threat", "section 506"],
        related_sections=["PPC Section 503"],
        offence_group="threat_offence",
        punishment_summary="This section provides punishment where criminal intimidation is proved.",
        provision_kind="punishment",
    ),
    build_federal_record(
        law_key="ppc",
        record_id="ppc-509",
        section_number="509",
        section_title="Word, gesture or act intended to insult modesty of a woman",
        summary=(
            "This provision generally applies where words, sounds, gestures, acts, or intrusions upon privacy are used to insult the modesty of a woman."
        ),
        excerpt=(
            "This section generally covers insulting the modesty of a woman through words, gestures, sounds, acts, or privacy intrusion."
        ),
        tags=["woman", "insult modesty", "harassment", "privacy intrusion"],
        aliases=["harassing woman", "eve teasing", "verbal harassment"],
        keywords=["insult modesty", "intrusion of privacy", "harassment of woman"],
        related_sections=["PPC Section 354"],
        offence_group="harassment_offence",
        provision_kind="offence",
    ),
]
