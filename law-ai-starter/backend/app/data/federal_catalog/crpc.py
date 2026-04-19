from app.data.federal_catalog.common import build_federal_record


CRPC_RECORDS = [
    build_federal_record(
        law_key="crpc",
        record_id="crpc-46",
        section_number="46",
        section_title="Arrest how made",
        summary=(
            "This provision gives the general framework for how an arrest is made, including physical submission or touch-based custody when required by law."
        ),
        excerpt=(
            "This section sets out the general legal manner in which arrest may be effected and read together with other arrest-and-detention safeguards."
        ),
        tags=["arrest procedure", "how arrest is made", "custody"],
        aliases=["how police arrest", "arrest procedure", "arrest ka tareeqa"],
        keywords=["arrest how made", "physical custody", "submission to custody"],
        related_sections=["CrPC Section 54", "CrPC Section 61"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-47",
        section_number="47",
        section_title="Search of place entered by person sought to be arrested",
        summary=(
            "This section generally deals with entry and search of a place when a person sought to be arrested is believed to have entered or to be inside that place."
        ),
        tags=["search for arrest", "entry of place", "arrest search powers"],
        aliases=["search house for accused", "entered place to arrest", "police search for arrest"],
        keywords=["place entered by person sought to be arrested", "search place after accused enters", "entry for arrest"],
        related_sections=["CrPC Section 46", "CrPC Section 54"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-51",
        section_number="51",
        section_title="Search of arrested person",
        summary=(
            "This section generally addresses the search of an arrested person and the handling of articles found in that search."
        ),
        tags=["search of arrested person", "custodial search", "articles seized on arrest"],
        aliases=["search after arrest", "custody search", "search my pockets after arrest"],
        keywords=["search arrested person", "articles found on accused", "personal search after arrest"],
        related_sections=["CrPC Section 46", "CrPC Section 54"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-54",
        section_number="54",
        section_title="Arrest without warrant",
        summary=(
            "This provision is one of the key procedural sections on when police may arrest without a warrant in specified circumstances."
        ),
        excerpt=(
            "This section sets out the circumstances in which police may arrest without a warrant and should be read with later custody and remand safeguards."
        ),
        tags=["arrest without warrant", "police powers", "cognizable case"],
        aliases=["without warrant arrest", "police picked me up", "bina warrant giraftari"],
        keywords=["arrest without warrant", "police powers", "cognizable offence arrest"],
        related_sections=["CrPC Section 46", "CrPC Section 61", "CrPC Section 167"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-61",
        section_number="61",
        section_title="Person arrested not to be detained more than twenty-four hours",
        summary=(
            "This section is commonly cited for the 24-hour custody rule requiring production before a Magistrate unless lawful detention authority exists otherwise."
        ),
        excerpt=(
            "This section is the well-known CrPC safeguard against keeping an arrested person in police custody beyond twenty-four hours except according to law."
        ),
        tags=["24 hours", "production before magistrate", "detention limit"],
        aliases=["24 hour rule", "detained more than 24 hours", "magistrate within 24 hours"],
        keywords=["twenty four hours", "illegal detention", "produce before magistrate"],
        related_sections=["CrPC Section 54", "CrPC Section 167"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-154",
        section_number="154",
        section_title="Information in cognizable cases",
        summary=(
            "This section is the core FIR-registration provision for information relating to cognizable offences."
        ),
        excerpt=(
            "This section governs recording information relating to cognizable offences and is central to FIR questions."
        ),
        tags=["FIR", "cognizable case", "police report", "first information report"],
        aliases=["register fir", "fir likhwana", "police refused fir"],
        keywords=["information in cognizable cases", "FIR registration", "cognizable offence report"],
        related_sections=["CrPC Section 155", "CrPC Section 156", "CrPC Section 157"],
        offence_group="fir_reporting",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-155",
        section_number="155",
        section_title="Information as to non-cognizable cases and investigation of such cases",
        summary=(
            "This section addresses how non-cognizable information is handled and the limits on investigation without proper authorization."
        ),
        excerpt=(
            "This section is commonly used where a matter is treated as non-cognizable rather than as an FIR-driven cognizable case."
        ),
        tags=["non-cognizable", "NC report", "police reporting", "investigation limit"],
        aliases=["nc report", "non cognizable case", "police said no FIR"],
        keywords=["non cognizable information", "section 155", "investigation of such cases"],
        related_sections=["CrPC Section 154", "CrPC Section 156"],
        offence_group="fir_reporting",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-156",
        section_number="156",
        section_title="Police officer's power to investigate cognizable case",
        summary=(
            "This section gives the general investigative authority in cognizable cases, subject to the rest of the procedural scheme."
        ),
        excerpt=(
            "This section governs police investigation power in cognizable cases and is frequently linked to FIR and early-investigation questions."
        ),
        tags=["investigation", "cognizable case", "police powers"],
        aliases=["police investigation power", "after FIR investigation", "tahqiqaat"],
        keywords=["power to investigate", "cognizable investigation", "section 156"],
        related_sections=["CrPC Section 154", "CrPC Section 157", "CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-157",
        section_number="157",
        section_title="Procedure for investigation",
        summary=(
            "This section generally covers the early procedural steps to be taken by police after information of a cognizable offence is received."
        ),
        tags=["investigation procedure", "early police steps", "cognizable inquiry"],
        aliases=["initial investigation steps", "police procedure after FIR", "case scene investigation"],
        keywords=["procedure for investigation", "section 157", "steps after cognizable information"],
        related_sections=["CrPC Section 154", "CrPC Section 156", "CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-160",
        section_number="160",
        section_title="Police officer's power to require attendance of witnesses",
        summary=(
            "This section generally deals with the power to require attendance of persons acquainted with the facts of a case during investigation, subject to legal limits."
        ),
        tags=["witness attendance", "investigation", "police notice"],
        aliases=["called to police station", "investigation witness notice", "attendance of witness"],
        keywords=["attendance of witnesses", "section 160", "police can call witness"],
        related_sections=["CrPC Section 161", "CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-164",
        section_number="164",
        section_title="Recording of confessions and statements",
        summary=(
            "This section is commonly cited where a Magistrate records a confession or statement during investigation according to legal safeguards."
        ),
        tags=["confession", "magistrate statement", "recording statement"],
        aliases=["164 statement", "confession before magistrate", "magistrate statement"],
        keywords=["recording confession", "section 164", "statement before magistrate"],
        related_sections=["CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-167",
        section_number="167",
        section_title="Procedure when investigation cannot be completed in twenty-four hours",
        summary=(
            "This section is central to remand questions. It applies where police say investigation cannot be completed within twenty-four hours and seek further lawful detention through the Magistrate."
        ),
        tags=["remand", "24 hours", "magistrate", "investigation not completed"],
        aliases=["police remand", "judicial remand", "section 167 remand"],
        keywords=["investigation cannot be completed in 24 hours", "remand procedure", "magistrate remand"],
        related_sections=["CrPC Section 61", "CrPC Section 173"],
        offence_group="arrest_detention",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-169",
        section_number="169",
        section_title="Release of accused when evidence deficient",
        summary=(
            "This section generally applies where the investigating officer considers the evidence insufficient and releases the accused according to the Code."
        ),
        tags=["release of accused", "insufficient evidence", "investigation outcome"],
        aliases=["evidence deficient release", "not enough evidence release", "release after investigation"],
        keywords=["release when evidence deficient", "section 169", "insufficient evidence"],
        related_sections=["CrPC Section 170", "CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-170",
        section_number="170",
        section_title="Cases to be sent to Magistrate when evidence is sufficient",
        summary=(
            "This section generally applies where the police consider there to be sufficient evidence or reasonable ground and forward the accused according to law."
        ),
        tags=["sufficient evidence", "send to magistrate", "challan pathway"],
        aliases=["case sent to magistrate", "enough evidence case", "forward accused to court"],
        keywords=["evidence sufficient", "section 170", "forward accused"],
        related_sections=["CrPC Section 169", "CrPC Section 173"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
    build_federal_record(
        law_key="crpc",
        record_id="crpc-173",
        section_number="173",
        section_title="Report of police officer on completion of investigation",
        summary=(
            "This section is commonly associated with the police report or challan submitted after completion of investigation."
        ),
        tags=["challan", "final report", "completion of investigation"],
        aliases=["police report", "challan", "final investigation report"],
        keywords=["report on completion of investigation", "section 173", "police challan"],
        related_sections=["CrPC Section 156", "CrPC Section 169", "CrPC Section 170"],
        offence_group="investigation",
        provision_kind="procedure",
    ),
]
