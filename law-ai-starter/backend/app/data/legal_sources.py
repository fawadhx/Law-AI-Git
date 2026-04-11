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
    ),
    LegalSourceRecord(
        id="ppc-379",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="379",
        section_title="Punishment for theft",
        summary=(
            "This provision covers the punishment that may apply when theft is proved."
        ),
        excerpt=(
            "Whoever commits theft shall be punished with imprisonment of either "
            "description for a term which may extend to three years, or with fine, "
            "or with both."
        ),
        citation_label="PPC Section 379",
        tags=["theft", "punishment", "fine", "imprisonment"],
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
    ),
    LegalSourceRecord(
        id="ppc-500",
        source_title="Pakistan Penal Code, 1860",
        law_name="Pakistan Penal Code",
        section_number="500",
        section_title="Punishment for defamation",
        summary=(
            "This provision covers the punishment that may apply in defamation matters."
        ),
        excerpt=(
            "Whoever defames another shall be punished with simple imprisonment for a term "
            "which may extend to two years, or with fine, or with both."
        ),
        citation_label="PPC Section 500",
        tags=["defamation", "punishment", "fine", "simple imprisonment"],
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
    ),
]