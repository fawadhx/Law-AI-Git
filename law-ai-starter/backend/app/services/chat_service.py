from app.schemas.chat import Citation, ChatQueryResponse


LEGAL_DISCLAIMER = (
    "This system is intended for legal information and public awareness only. "
    "It should not be treated as a substitute for professional legal advice or representation."
)


def generate_mock_legal_response(question: str) -> ChatQueryResponse:
    normalized_question = question.strip()

    answer = (
        "This is a mock legal-information response. The real version should classify the query, "
        "retrieve the most relevant legal sections, identify overlapping provisions, and return "
        f"a citation-grounded explanation. Your current question was: '{normalized_question}'."
    )

    citations = [
        Citation(
            title="Sample Penal Provision",
            section="Section 101",
            note="Placeholder citation for development. Replace with actual legal source records.",
        ),
        Citation(
            title="Sample Procedural Provision",
            section="Section 12",
            note="Placeholder related section showing how overlapping laws may be displayed.",
        ),
    ]

    return ChatQueryResponse(
        answer=answer,
        citations=citations,
        disclaimer=LEGAL_DISCLAIMER,
    )