from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.admin_auth import require_admin_auth
from app.schemas.admin import (
    AdminPublishExecutionResponse,
    AdminPublishQueueRecord,
    AdminRetrievalReadinessResponse,
    AdminRetrievalProbeRequest,
    AdminRetrievalProbeResponse,
    AdminEmbeddingReadinessResponse,
    AdminEmbeddingRunRequest,
    AdminEmbeddingRunResponse,
    AdminIngestionBatchPreviewRequest,
    AdminIngestionBatchPreviewResponse,
    AdminIngestionPreviewRequest,
    AdminIngestionPreviewResponse,
    AdminRetrievalRefreshRequest,
    AdminRetrievalRefreshResponse,
    AdminSourceCatalogResponse,
    AdminSourceCreateResponse,
    AdminSourceDeleteResponse,
    AdminSourceDetailResponse,
    AdminSourceUpdateResponse,
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
    create_admin_source_record,
    delete_admin_source_record,
    get_admin_source_detail,
    preview_admin_ingestion,
    preview_admin_ingestion_batch,
    update_admin_source_record,
    get_admin_summary,
    get_admin_retrieval_readiness,
    run_admin_retrieval_probe,
    get_admin_embedding_readiness,
    refresh_admin_retrieval_metadata,
    run_admin_embedding_refresh,
    get_admin_workspace,
    get_admin_workspace_draft,
    publish_admin_workspace_package,
    review_admin_source_draft,
    save_admin_workspace_draft,
    validate_admin_source_draft,
)

router = APIRouter(dependencies=[Depends(require_admin_auth)])


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


@router.post("/admin/retrieval-probe", response_model=AdminRetrievalProbeResponse)
def admin_retrieval_probe(payload: AdminRetrievalProbeRequest) -> AdminRetrievalProbeResponse:
    return run_admin_retrieval_probe(payload)


@router.get("/admin/embedding-readiness", response_model=AdminEmbeddingReadinessResponse)
def admin_embedding_readiness() -> AdminEmbeddingReadinessResponse:
    return get_admin_embedding_readiness()


@router.post("/admin/embedding-readiness/run", response_model=AdminEmbeddingRunResponse)
def admin_embedding_refresh(payload: AdminEmbeddingRunRequest) -> AdminEmbeddingRunResponse:
    return run_admin_embedding_refresh(payload)


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
