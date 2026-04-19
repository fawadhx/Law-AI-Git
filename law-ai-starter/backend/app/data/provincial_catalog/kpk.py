from app.data.provincial_catalog.common import build_provincial_source_record


KPK_RECORDS = [
    build_provincial_source_record(
        province_key="kpk",
        record_id="prov-kpk-catalog",
        section_title="Official Khyber Pakhtunkhwa legislation repository",
        summary=(
            "Use this source-reference record when a question clearly asks for Khyber Pakhtunkhwa provincial law. "
            "It helps retrieval distinguish KP-only context from federal law."
        ),
        aliases=["KPK law", "KP law", "Khyber Pakhtunkhwa law", "KP provincial law"],
        keywords=["KP Code", "Khyber Pakhtunkhwa legislation", "KPK laws", "KP statutes"],
        tags=["province filter", "official source"],
    ),
]
