from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
def admin_overview() -> dict[str, object]:
    return {
        "status": "starter",
        "message": "Admin routes are scaffolded. Add authentication before using these in production.",
        "modules": ["sources", "prompts", "mappings", "audit"],
    }
