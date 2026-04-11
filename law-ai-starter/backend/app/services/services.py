from app.schemas.admin import (
    AdminRoadmapItem,
    AdminStat,
    AdminStatusCard,
    AdminSummaryResponse,
)


def get_admin_summary() -> AdminSummaryResponse:
    return AdminSummaryResponse(
        stats=[
            AdminStat(
                value="128",
                title="Source records",
                description="Total legal source records tracked in the admin layer.",
            ),
            AdminStat(
                value="18",
                title="Authority mappings",
                description="Structured rank and authority mappings configured.",
            ),
            AdminStat(
                value="06",
                title="Prompt rules",
                description="Prompt policy groups for safe legal-information responses.",
            ),
            AdminStat(
                value="03",
                title="Draft modules",
                description="Upcoming modules prepared for future implementation.",
            ),
        ],
        control_areas=[
            AdminRoadmapItem(
                title="Legal source records",
                text="Upload, store, edit, review, and version structured legal source records.",
            ),
            AdminRoadmapItem(
                title="Prompt and policy controls",
                text="Manage system instructions, disclaimers, and response safety behavior.",
            ),
            AdminRoadmapItem(
                title="Authority mappings",
                text="Maintain officer-rank summaries, powers, and limitations.",
            ),
            AdminRoadmapItem(
                title="Future retrieval controls",
                text="Prepare retrieval configuration, source quality checks, and review workflows.",
            ),
        ],
        status_cards=[
            AdminStatusCard(
                title="Source status",
                content="Core law source management is planned but not yet connected to real database records.",
            ),
            AdminStatusCard(
                title="Prompt status",
                content="Prompt control is currently conceptual and will later move into backend-managed policy records.",
            ),
        ],
        workflow_steps=[
            "Review legal source entries before publishing them to production.",
            "Maintain disclaimers and legal-information boundaries centrally.",
            "Version prompt policies and authority records for traceability.",
            "Prepare future review states such as draft, reviewed, approved, and archived.",
        ],
        roadmap_items=[
            AdminRoadmapItem(
                title="Source upload manager",
                text="Upload and normalize legal documents into structured internal records.",
            ),
            AdminRoadmapItem(
                title="Prompt policy editor",
                text="Manage system disclaimers, classifications, and response control logic.",
            ),
            AdminRoadmapItem(
                title="Authority records panel",
                text="Edit officer-rank summaries, powers, and limitations from admin UI.",
            ),
            AdminRoadmapItem(
                title="Review workflow",
                text="Move source records through draft, review, approval, and archive stages.",
            ),
            AdminRoadmapItem(
                title="Audit trail",
                text="Track source changes, policy edits, and future admin activity logs.",
            ),
            AdminRoadmapItem(
                title="Role-based access",
                text="Limit admin features by role before any production deployment.",
            ),
        ],
        admin_boundary=(
            "This admin screen is a prototype control panel. Authentication, access control, "
            "upload workflows, audit logging, and source approval logic should be added before "
            "treating it as a real production admin system."
        ),
    )