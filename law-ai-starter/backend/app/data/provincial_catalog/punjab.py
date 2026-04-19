from app.data.provincial_catalog.common import build_provincial_source_record


PUNJAB_RECORDS = [
    build_provincial_source_record(
        province_key="punjab",
        record_id="prov-punjab-catalog",
        section_title="Official Punjab legislation repository",
        summary=(
            "Use this source-reference record when a question clearly asks for Punjab provincial law or a Punjab-only legal source. "
            "It helps retrieval keep Punjab context separate from federal law."
        ),
        aliases=["Punjab law", "Punjab Act", "Punjab provincial law", "Punjab legal source"],
        keywords=["Punjab laws online", "Punjab legislation", "Punjab code", "Punjab statutes"],
        tags=["province filter", "official source"],
    ),
]
