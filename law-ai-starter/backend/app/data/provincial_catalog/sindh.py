from app.data.provincial_catalog.common import build_provincial_source_record


SINDH_RECORDS = [
    build_provincial_source_record(
        province_key="sindh",
        record_id="prov-sindh-catalog",
        section_title="Official Sindh legislation repository",
        summary=(
            "Use this source-reference record when a question clearly asks for Sindh provincial law or the Sindh Code. "
            "It supports province-aware matching without pretending to provide unverified provincial sections."
        ),
        aliases=["Sindh law", "Sindh Act", "Sindh provincial law", "Sindh legal source"],
        keywords=["Sindh Code", "Sindh laws", "Sindh legislation", "Sindh statute"],
        tags=["province filter", "official source"],
    ),
]
