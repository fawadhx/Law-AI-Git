from dataclasses import dataclass

from app.schemas.legal_source import LegalSourceRecord


@dataclass(frozen=True)
class RetrievalScoreComponent:
    name: str
    score: int
    reason: str


OFFICIAL_TRUST_LEVELS = {
    "official_repository",
    "official_gazette",
    "official_provincial_repository",
}


def metadata_quality_components(record: LegalSourceRecord) -> list[RetrievalScoreComponent]:
    """Reward records that are easier to verify and explain to users."""
    components: list[RetrievalScoreComponent] = []

    if record.source_trust_level in OFFICIAL_TRUST_LEVELS:
        components.append(
            RetrievalScoreComponent(
                "source_quality",
                2,
                "Official or official-repository provenance is available.",
            )
        )
    elif record.source_trust_level:
        components.append(
            RetrievalScoreComponent(
                "source_quality",
                1,
                "Source-trust metadata is available.",
            )
        )

    completeness = 0
    if record.source_url:
        completeness += 1
    if record.official_citation:
        completeness += 1
    if record.source_last_verified:
        completeness += 1
    if record.law_type:
        completeness += 1

    if completeness:
        components.append(
            RetrievalScoreComponent(
                "metadata_completeness",
                min(3, completeness),
                "Structured citation/source metadata is present.",
            )
        )

    return components


def components_for_relevance_anchor(
    components: list[RetrievalScoreComponent],
    *,
    has_relevance_anchor: bool,
) -> list[RetrievalScoreComponent]:
    """Prevent provenance metadata from making an otherwise irrelevant record match."""
    if has_relevance_anchor:
        return components

    allowed_without_anchor = {"jurisdiction", "jurisdiction_mismatch", "provincial_scope"}
    return [component for component in components if component.name in allowed_without_anchor]


def jurisdiction_components(
    *,
    record: LegalSourceRecord,
    province_hint: str | None,
    provincial_query: bool,
) -> list[RetrievalScoreComponent]:
    components: list[RetrievalScoreComponent] = []

    if province_hint and record.province == province_hint:
        components.append(
            RetrievalScoreComponent(
                "jurisdiction",
                8,
                f"Query names {province_hint}, matching this provincial record.",
            )
        )
    elif province_hint and record.government_level == "provincial":
        components.append(
            RetrievalScoreComponent(
                "jurisdiction_mismatch",
                -5,
                "Query names a different province, so this provincial record is deprioritized.",
            )
        )
    elif province_hint and record.government_level == "federal":
        components.append(
            RetrievalScoreComponent(
                "federal_for_province_query",
                -2,
                "Query is province-specific, so federal records are slightly deprioritized.",
            )
        )

    if provincial_query and record.government_level == "provincial":
        components.append(
            RetrievalScoreComponent(
                "provincial_scope",
                3,
                "Query has provincial wording and this is a provincial record.",
            )
        )

    return components


def record_type_components(
    *,
    record: LegalSourceRecord,
    signals: dict[str, bool],
    intent: dict[str, bool],
) -> list[RetrievalScoreComponent]:
    components: list[RetrievalScoreComponent] = []

    if intent.get("punishment_focus") and record.provision_kind == "punishment":
        components.append(
            RetrievalScoreComponent(
                "record_type",
                5,
                "Question asks about punishment and this is a punishment record.",
            )
        )
    elif intent.get("definition_focus") and record.provision_kind in {"definition", "offence", "general"}:
        components.append(
            RetrievalScoreComponent(
                "record_type",
                3,
                "Question asks for meaning/coverage and this is a primary explanatory record.",
            )
        )

    if signals.get("fir") and record.provision_kind == "procedure":
        components.append(
            RetrievalScoreComponent(
                "procedure_type",
                3,
                "FIR/reporting wording aligns with a procedure record.",
            )
        )

    if record.provision_kind == "source_reference" and not signals.get("provincial"):
        components.append(
            RetrievalScoreComponent(
                "source_reference_guardrail",
                -4,
                "Source-reference records should not dominate non-provincial legal questions.",
            )
        )

    return components


def category_components(
    *,
    record: LegalSourceRecord,
    signals: dict[str, bool],
) -> list[RetrievalScoreComponent]:
    components: list[RetrievalScoreComponent] = []
    category = (record.law_category or "").lower()

    if signals.get("online") and ("cyber" in category or record.law_name == "Prevention of Electronic Crimes Act"):
        components.append(
            RetrievalScoreComponent("category", 4, "Online/cyber wording aligns with cyber-law category.")
        )
    if signals.get("police") and ("procedure" in category or record.law_name == "Code of Criminal Procedure"):
        components.append(
            RetrievalScoreComponent("category", 4, "Police/procedure wording aligns with criminal procedure.")
        )
    if any(signals.get(key) for key in ["property", "fraud", "threat", "assault", "trespass", "mischief"]) and "criminal" in category:
        components.append(
            RetrievalScoreComponent("category", 3, "Criminal-law issue wording aligns with this record category.")
        )

    return components


def sum_components(components: list[RetrievalScoreComponent]) -> int:
    return sum(component.score for component in components)
