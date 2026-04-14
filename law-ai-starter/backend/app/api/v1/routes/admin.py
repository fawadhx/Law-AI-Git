from fastapi import APIRouter, HTTPException

from app.schemas.admin import (
    AdminPublishExecutionResponse,
    AdminPublishQueueRecord,
    AdminRetrievalReadinessResponse,
    AdminRetrievalRefreshRequest,
    AdminRetrievalRefreshResponse,
    AdminSourceCatalogResponse,
    AdminSourceDetailResponse,
    AdminSourceDraftInput,
    AdminSourceDraftReviewResponse,
    AdminSourceDraftValidationResponse,
    AdminSourcePublishPreviewResponse,
    AdminSummaryResponse,
    AdminActivityFeedResponse,
    AdminWorkspaceDraftDetailResponse,
    AdminWorkspaceDraftSaveRequest,
    AdminWorkspaceResponse,
    AdminWorkspaceStageRequest,
)
from app.services.admin_service import (
    build_admin_source_publish_preview,
    build_admin_workspace_publish_package,
    delete_admin_workspace_draft,
    delete_admin_workspace_publish_package,
    get_admin_activity_feed,
    get_admin_source_catalog,
    get_admin_source_detail,
    get_admin_summary,
    get_admin_retrieval_readiness,
    refresh_admin_retrieval_metadata,
    get_admin_workspace,
    get_admin_workspace_draft,
    publish_admin_workspace_package,
    review_admin_source_draft,
    save_admin_workspace_draft,
    validate_admin_source_draft,
)

router = APIRouter()


@router.get("/admin/summary", response_model=AdminSummaryResponse)
def admin_summary() -> AdminSummaryResponse:
    return get_admin_summary()


@router.get("/admin/sources", response_model=AdminSourceCatalogResponse)
def admin_sources() -> AdminSourceCatalogResponse:
    return get_admin_source_catalog()


@router.get("/admin/sources/{source_id}", response_model=AdminSourceDetailResponse)
def admin_source_detail(source_id: str) -> AdminSourceDetailResponse:
    detail = get_admin_source_detail(source_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Source record not found.")
    return detail


@router.post("/admin/sources/validate", response_model=AdminSourceDraftValidationResponse)
def admin_source_validate(payload: AdminSourceDraftInput) -> AdminSourceDraftValidationResponse:
    return validate_admin_source_draft(payload)


@router.post("/admin/sources/review", response_model=AdminSourceDraftReviewResponse)
def admin_source_review(payload: AdminSourceDraftInput) -> AdminSourceDraftReviewResponse:
    return review_admin_source_draft(payload)


@router.post("/admin/sources/publish-preview", response_model=AdminSourcePublishPreviewResponse)
def admin_source_publish_preview(payload: AdminSourceDraftInput) -> AdminSourcePublishPreviewResponse:
    return build_admin_source_publish_preview(payload)




@router.get("/admin/retrieval-readiness", response_model=AdminRetrievalReadinessResponse)
def admin_retrieval_readiness() -> AdminRetrievalReadinessResponse:
    return get_admin_retrieval_readiness()


@router.post("/admin/retrieval-readiness/refresh", response_model=AdminRetrievalRefreshResponse)
def admin_retrieval_refresh(payload: AdminRetrievalRefreshRequest) -> AdminRetrievalRefreshResponse:
    return refresh_admin_retrieval_metadata(payload)


@router.get("/admin/workspace", response_model=AdminWorkspaceResponse)
def admin_workspace() -> AdminWorkspaceResponse:
    return get_admin_workspace()


@router.post("/admin/workspace/drafts/save", response_model=AdminWorkspaceDraftDetailResponse)
def admin_workspace_save_draft(payload: AdminWorkspaceDraftSaveRequest) -> AdminWorkspaceDraftDetailResponse:
    return save_admin_workspace_draft(payload)


@router.get("/admin/workspace/drafts/{workspace_draft_id}", response_model=AdminWorkspaceDraftDetailResponse)
def admin_workspace_get_draft(workspace_draft_id: str) -> AdminWorkspaceDraftDetailResponse:
    detail = get_admin_workspace_draft(workspace_draft_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Workspace draft not found.")
    return detail


@router.delete("/admin/workspace/drafts/{workspace_draft_id}")
def admin_workspace_delete_draft(workspace_draft_id: str) -> dict[str, bool]:
    deleted = delete_admin_workspace_draft(workspace_draft_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workspace draft not found.")
    return {"ok": True}


@router.post("/admin/workspace/publish-packages/stage", response_model=AdminPublishQueueRecord)
def admin_workspace_stage_publish(payload: AdminWorkspaceStageRequest) -> AdminPublishQueueRecord:
    return build_admin_workspace_publish_package(payload)


@router.delete("/admin/workspace/publish-packages/{package_id}")
def admin_workspace_delete_publish_package(package_id: str) -> dict[str, bool]:
    deleted = delete_admin_workspace_publish_package(package_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publish package not found.")
    return {"ok": True}


@router.get("/admin/activity", response_model=AdminActivityFeedResponse)
def admin_activity() -> AdminActivityFeedResponse:
    return get_admin_activity_feed()


@router.post("/admin/workspace/publish-packages/{package_id}/publish", response_model=AdminPublishExecutionResponse)
def admin_workspace_publish_package(package_id: str) -> AdminPublishExecutionResponse:
    try:
        result = publish_admin_workspace_package(package_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Publish package not found.")
    return result
