from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.admin_auth import require_admin_auth, require_admin_write_access
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
from app.services.admin_audit_service import write_admin_audit_event

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
    result = validate_admin_source_draft(payload)
    write_admin_audit_event(
        kind="validation",
        title="Validated source draft",
        detail=(
            f"Validated draft for {result.preview.citation_label or result.preview.law_name}. "
            f"Readiness score {result.readiness_score} with {result.error_count} error(s) and {result.warning_count} warning(s)."
        ),
        status="blocked" if result.error_count > 0 else "validated",
        citation_label=result.preview.citation_label or None,
        record_id=payload.id,
        metadata={
            "readiness_score": result.readiness_score,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
        },
    )
    return result


@router.post("/admin/sources/review", response_model=AdminSourceDraftReviewResponse)
def admin_source_review(
    payload: AdminSourceDraftInput,
    _: object = Depends(require_admin_write_access),
) -> AdminSourceDraftReviewResponse:
    result = review_admin_source_draft(payload)
    write_admin_audit_event(
        kind="review",
        title="Reviewed source draft",
        detail=(
            f"Reviewed draft for {payload.citation_label or payload.law_name or 'untitled draft'}. "
            f"Review status {result.review_status} with {result.blocker_count} blocker(s) and {result.warning_count} warning(s)."
        ),
        status=result.review_status,
        citation_label=payload.citation_label or None,
        record_id=payload.id,
        metadata={
            "review_status": result.review_status,
            "blocker_count": result.blocker_count,
            "warning_count": result.warning_count,
            "publish_mode": result.publish_mode,
        },
    )
    return result


@router.post("/admin/sources/publish-preview", response_model=AdminSourcePublishPreviewResponse)
def admin_source_publish_preview(
    payload: AdminSourceDraftInput,
    _: object = Depends(require_admin_write_access),
) -> AdminSourcePublishPreviewResponse:
    result = build_admin_source_publish_preview(payload)
    write_admin_audit_event(
        kind="publish_preview",
        title="Built publish preview",
        detail=(
            f"Built publish preview for {payload.citation_label or payload.law_name or 'untitled draft'}. "
            f"Status {result.publish_status} with {len(result.blockers)} blocker(s) and {len(result.warnings)} warning(s)."
        ),
        status=result.publish_status,
        citation_label=payload.citation_label or None,
        record_id=payload.id,
        metadata={
            "publish_status": result.publish_status,
            "publish_mode": result.publish_mode,
            "blocker_count": len(result.blockers),
            "warning_count": len(result.warnings),
        },
    )
    return result




@router.get("/admin/retrieval-readiness", response_model=AdminRetrievalReadinessResponse)
def admin_retrieval_readiness() -> AdminRetrievalReadinessResponse:
    return get_admin_retrieval_readiness()


@router.post("/admin/retrieval-readiness/refresh", response_model=AdminRetrievalRefreshResponse)
def admin_retrieval_refresh(
    payload: AdminRetrievalRefreshRequest,
    _: object = Depends(require_admin_write_access),
) -> AdminRetrievalRefreshResponse:
    return refresh_admin_retrieval_metadata(payload)


@router.post("/admin/retrieval-probe", response_model=AdminRetrievalProbeResponse)
def admin_retrieval_probe(payload: AdminRetrievalProbeRequest) -> AdminRetrievalProbeResponse:
    return run_admin_retrieval_probe(payload)


@router.get("/admin/embedding-readiness", response_model=AdminEmbeddingReadinessResponse)
def admin_embedding_readiness() -> AdminEmbeddingReadinessResponse:
    return get_admin_embedding_readiness()


@router.post("/admin/embedding-readiness/run", response_model=AdminEmbeddingRunResponse)
def admin_embedding_refresh(
    payload: AdminEmbeddingRunRequest,
    _: object = Depends(require_admin_write_access),
) -> AdminEmbeddingRunResponse:
    return run_admin_embedding_refresh(payload)


@router.get("/admin/workspace", response_model=AdminWorkspaceResponse)
def admin_workspace() -> AdminWorkspaceResponse:
    return get_admin_workspace()


@router.post("/admin/workspace/drafts/save", response_model=AdminWorkspaceDraftDetailResponse)
def admin_workspace_save_draft(
    payload: AdminWorkspaceDraftSaveRequest,
    _: object = Depends(require_admin_write_access),
) -> AdminWorkspaceDraftDetailResponse:
    result = save_admin_workspace_draft(payload)
    write_admin_audit_event(
        kind="workspace_save",
        title="Saved workspace draft",
        detail=(
            f"Saved workspace draft {result.workspace_draft.workspace_draft_id} for {result.workspace_draft.citation_label or result.workspace_draft.title}. "
            f"Version {result.workspace_draft.version} with review status {result.workspace_draft.review_status}."
        ),
        status="saved",
        citation_label=result.workspace_draft.citation_label or None,
        record_id=result.workspace_draft.workspace_draft_id,
        metadata={
            "workspace_draft_id": result.workspace_draft.workspace_draft_id,
            "version": result.workspace_draft.version,
            "review_status": result.workspace_draft.review_status,
        },
    )
    return result


@router.get("/admin/workspace/drafts/{workspace_draft_id}", response_model=AdminWorkspaceDraftDetailResponse)
def admin_workspace_get_draft(workspace_draft_id: str) -> AdminWorkspaceDraftDetailResponse:
    detail = get_admin_workspace_draft(workspace_draft_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Workspace draft not found.")
    return detail


@router.delete("/admin/workspace/drafts/{workspace_draft_id}")
def admin_workspace_delete_draft(
    workspace_draft_id: str,
    _: object = Depends(require_admin_write_access),
) -> dict[str, bool]:
    deleted = delete_admin_workspace_draft(workspace_draft_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workspace draft not found.")
    write_admin_audit_event(
        kind="workspace_delete",
        title="Deleted workspace draft",
        detail=f"Deleted workspace draft {workspace_draft_id}.",
        status="deleted",
        record_id=workspace_draft_id,
        metadata={"workspace_draft_id": workspace_draft_id},
    )
    return {"ok": True}


@router.post("/admin/workspace/publish-packages/stage", response_model=AdminPublishQueueRecord)
def admin_workspace_stage_publish(
    payload: AdminWorkspaceStageRequest,
    _: object = Depends(require_admin_write_access),
) -> AdminPublishQueueRecord:
    try:
        result = build_admin_workspace_publish_package(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    write_admin_audit_event(
        kind="stage_publish",
        title="Staged publish package",
        detail=(
            f"Staged publish package {result.package_id} for {result.citation_label or result.title}. "
            f"Mode {result.publish_mode} with {result.blocker_count} blocker(s) and {result.warning_count} warning(s)."
        ),
        status=result.publish_status,
        citation_label=result.citation_label or None,
        record_id=result.package_id,
        metadata={
            "package_id": result.package_id,
            "publish_mode": result.publish_mode,
            "blocker_count": result.blocker_count,
            "warning_count": result.warning_count,
        },
    )
    return result


@router.delete("/admin/workspace/publish-packages/{package_id}")
def admin_workspace_delete_publish_package(
    package_id: str,
    _: object = Depends(require_admin_write_access),
) -> dict[str, bool]:
    deleted = delete_admin_workspace_publish_package(package_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publish package not found.")
    write_admin_audit_event(
        kind="stage_delete",
        title="Deleted staged publish package",
        detail=f"Deleted staged publish package {package_id}.",
        status="deleted",
        record_id=package_id,
        metadata={"package_id": package_id},
    )
    return {"ok": True}


@router.get("/admin/activity", response_model=AdminActivityFeedResponse)
def admin_activity() -> AdminActivityFeedResponse:
    return get_admin_activity_feed()


@router.post("/admin/workspace/publish-packages/{package_id}/publish", response_model=AdminPublishExecutionResponse)
def admin_workspace_publish_package(
    package_id: str,
    _: object = Depends(require_admin_write_access),
) -> AdminPublishExecutionResponse:
    try:
        result = publish_admin_workspace_package(package_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Publish package not found.")
    return result
