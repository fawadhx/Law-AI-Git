from app.data.provincial_catalog.common import build_provincial_source_record


BALOCHISTAN_RECORDS = [
    build_provincial_source_record(
        province_key="balochistan",
        record_id="prov-balochistan-catalog",
        section_title="Official Balochistan legislation repository",
        summary=(
            "Use this source-reference record when a question clearly asks for Balochistan provincial law or Balochistan-only legislation. "
            "It preserves province-aware routing without inventing section-level content."
        ),
        aliases=["Balochistan law", "Balochistan Act", "Balochistan provincial law"],
        keywords=["Balochistan Code", "Balochistan laws", "Balochistan legislation"],
        tags=["province filter", "official source"],
    ),
]
