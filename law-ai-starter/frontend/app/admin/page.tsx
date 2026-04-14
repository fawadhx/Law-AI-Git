"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

type AdminStat = {
  value: string;
  title: string;
  description: string;
};

type AdminStatusCard = {
  title: string;
  content: string;
};

type AdminRoadmapItem = {
  title: string;
  text: string;
};

type AdminCatalogSourceInfo = {
  active_source: string;
  source_label: string;
  database_ready: boolean;
  foundation_stage: string;
  active_record_count: number;
  persisted_record_count: number;
  detail: string;
};

type AdminSummaryResponse = {
  stats: AdminStat[];
  control_areas: AdminRoadmapItem[];
  status_cards: AdminStatusCard[];
  workflow_steps: string[];
  roadmap_items: AdminRoadmapItem[];
  admin_boundary: string;
  catalog_source?: AdminCatalogSourceInfo | null;
};

type AdminSourceRecord = {
  id: string;
  citation_label: string;
  source_title: string;
  law_name: string;
  section_number: string;
  section_title: string;
  summary: string;
  jurisdiction: string;
  provision_kind: string;
  offence_group: string | null;
  related_sections: string[];
  tags: string[];
  punishment_summary: string | null;
  admin_note: string;
};

type AdminSourceCatalogSummary = {
  total_records: number;
  law_count: number;
  offence_group_count: number;
  punishment_record_count: number;
  procedure_record_count: number;
};

type AdminSourceCatalogResponse = {
  summary: AdminSourceCatalogSummary;
  items: AdminSourceRecord[];
  available_laws: string[];
  available_groups: string[];
  available_kinds: string[];
  workflow_note: string;
  catalog_source?: AdminCatalogSourceInfo | null;
};

type AdminLinkedRecord = {
  id: string;
  citation_label: string;
  law_name: string;
  section_number: string;
  section_title: string;
  provision_kind: string;
  relationship_label: string;
  summary: string;
};

type AdminSourceDetailRecord = AdminSourceRecord & {
  excerpt: string;
  aliases: string[];
  keywords: string[];
  searchable_terms: string[];
  related_record_count: number;
  same_group_record_count: number;
  same_law_record_count: number;
};

type AdminSourceDetailResponse = {
  item: AdminSourceDetailRecord;
  companion_records: AdminLinkedRecord[];
  same_group_records: AdminLinkedRecord[];
  same_law_records: AdminLinkedRecord[];
  workflow_note: string;
  catalog_source?: AdminCatalogSourceInfo | null;
};


type AdminDraftForm = {
  id: string;
  source_title: string;
  law_name: string;
  section_number: string;
  section_title: string;
  summary: string;
  excerpt: string;
  citation_label: string;
  jurisdiction: string;
  provision_kind: string;
  offence_group: string;
  punishment_summary: string;
  tags_text: string;
  aliases_text: string;
  keywords_text: string;
  related_sections_text: string;
};

type AdminDraftValidationIssue = {
  field: string;
  level: string;
  message: string;
};

type AdminDraftSectionCheck = {
  existing: string[];
  missing: string[];
};

type AdminSourceDraftPreview = {
  citation_label: string;
  law_name: string;
  section_number: string;
  section_title: string;
  provision_kind: string;
  offence_group: string | null;
  related_sections: string[];
  tags: string[];
  aliases: string[];
  keywords: string[];
  searchable_terms: string[];
  admin_note: string;
};

type AdminSourceDraftValidationResponse = {
  preview: AdminSourceDraftPreview;
  readiness_score: number;
  issue_count: number;
  error_count: number;
  warning_count: number;
  issues: AdminDraftValidationIssue[];
  related_section_check: AdminDraftSectionCheck;
  workflow_note: string;
};


type AdminDraftFieldChange = {
  field: string;
  label: string;
  before: string | null;
  after: string | null;
  changed: boolean;
};

type AdminReviewChecklistItem = {
  key: string;
  title: string;
  status: string;
  detail: string;
};

type AdminSourceDraftReviewResponse = {
  review_status: string;
  approval_label: string;
  readiness_score: number;
  blocker_count: number;
  warning_count: number;
  publish_mode: string;
  changed_field_count: number;
  changed_fields: AdminDraftFieldChange[];
  checklist: AdminReviewChecklistItem[];
  workflow_note: string;
};

type AdminSourcePublishPreviewResponse = {
  publish_status: string;
  publish_mode: string;
  target_record_id: string | null;
  changed_field_count: number;
  searchable_term_count: number;
  linked_section_count: number;
  companion_hit_count: number;
  same_group_context_count: number;
  same_law_context_count: number;
  blockers: string[];
  warnings: string[];
  recommended_actions: string[];
  changed_fields: AdminDraftFieldChange[];
  workflow_note: string;
};

type AdminWorkspaceDraftRecord = {
  workspace_draft_id: string;
  title: string;
  citation_label: string;
  law_name: string;
  section_number: string;
  publish_mode: string;
  source_record_id: string | null;
  version: number;
  readiness_score: number;
  review_status: string;
  publish_status: string;
  blocker_count: number;
  warning_count: number;
  changed_field_count: number;
  saved_at: string;
};

type AdminWorkspaceDraftDetailResponse = {
  workspace_draft: AdminWorkspaceDraftRecord;
  payload: {
    id?: string | null;
    source_title: string;
    law_name: string;
    section_number: string;
    section_title: string;
    summary: string;
    excerpt: string;
    citation_label: string;
    jurisdiction: string;
    provision_kind: string;
    offence_group?: string | null;
    punishment_summary?: string | null;
    tags: string[];
    aliases: string[];
    keywords: string[];
    related_sections: string[];
  };
  validation: AdminSourceDraftValidationResponse;
  review: AdminSourceDraftReviewResponse;
  publish_preview: AdminSourcePublishPreviewResponse;
  workflow_note: string;
};

type AdminPublishQueueRecord = {
  package_id: string;
  workspace_draft_id: string | null;
  title: string;
  citation_label: string;
  publish_mode: string;
  target_record_id: string | null;
  review_status: string;
  publish_status: string;
  blocker_count: number;
  warning_count: number;
  changed_field_count: number;
  staged_at: string;
  summary_line: string;
};

type AdminWorkspaceResponse = {
  saved_draft_count: number;
  staged_publish_count: number;
  ready_draft_count: number;
  blocked_item_count: number;
  session_publish_count: number;
  drafts: AdminWorkspaceDraftRecord[];
  publish_queue: AdminPublishQueueRecord[];
  workflow_note: string;
};

type AdminActivityRecord = {
  activity_id: string;
  kind: string;
  title: string;
  detail: string;
  status: string;
  citation_label: string | null;
  record_id: string | null;
  created_at: string;
};

type AdminActivityFeedResponse = {
  total_events: number;
  publish_event_count: number;
  latest_publish_label: string | null;
  items: AdminActivityRecord[];
  workflow_note: string;
};

type AdminPublishExecutionResponse = {
  publish_status: string;
  package_id: string;
  published_record_id: string;
  citation_label: string;
  publish_mode: string;
  changed_field_count: number;
  catalog_record_count: number;
  activity: AdminActivityRecord;
  workflow_note: string;
};

type AdminRetrievalProbeRecord = {
  record_id: string;
  citation_label: string;
  law_name: string;
  section_number: string;
  category: string;
  keyword_score: number;
  vector_similarity: number | null;
  vector_bonus: number;
  final_score: number;
  selected: boolean;
  exact_section_match: boolean;
  excerpt: string;
};

type AdminRetrievalProbeResponse = {
  query: string;
  active_source: string;
  source_label: string;
  vector_retrieval_active: boolean;
  vector_query_top_k: number;
  keyword_candidate_count: number;
  vector_candidate_count: number;
  selected_count: number;
  records: AdminRetrievalProbeRecord[];
  workflow_note: string;
};

type AdminRetrievalReadinessRecord = {
  record_id: string;
  citation_label: string;
  law_name: string;
  section_number: string;
  embedding_status: string;
  has_retrieval_document: boolean;
  has_retrieval_fingerprint: boolean;
  fingerprint_status: string;
  refresh_needed: boolean;
};

type AdminRetrievalReadinessResponse = {
  active_source: string;
  source_label: string;
  database_ready: boolean;
  foundation_stage: string;
  persisted_record_count: number;
  active_record_count: number;
  embedding_ready_count: number;
  embedding_pending_count: number;
  stale_count: number;
  missing_document_count: number;
  missing_fingerprint_count: number;
  refresh_needed_count: number;
  vector_candidate_count: number;
  sample_records: AdminRetrievalReadinessRecord[];
  workflow_note: string;
};

type AdminRetrievalRefreshResponse = {
  refresh_applied: boolean;
  active_source: string;
  source_label: string;
  refreshed_count: number;
  unchanged_count: number;
  pending_marked_count: number;
  persisted_record_count: number;
  embedding_ready_count: number;
  embedding_pending_count: number;
  sample_records: AdminRetrievalReadinessRecord[];
  workflow_note: string;
};

type AdminEmbeddingReadinessRecord = {
  record_id: string;
  citation_label: string;
  law_name: string;
  section_number: string;
  embedding_status: string;
  has_vector: boolean;
  fingerprint_match: boolean;
  model_name: string | null;
  dimensions: number | null;
  refresh_needed: boolean;
  last_error: string | null;
};

type AdminEmbeddingReadinessResponse = {
  provider_ready: boolean;
  api_key_configured: boolean;
  active_source: string;
  source_label: string;
  database_ready: boolean;
  foundation_stage: string;
  persisted_record_count: number;
  vector_row_count: number;
  ready_vector_count: number;
  pending_count: number;
  error_count: number;
  runnable_count: number;
  sample_records: AdminEmbeddingReadinessRecord[];
  workflow_note: string;
};

type AdminEmbeddingRunResponse = {
  run_attempted: boolean;
  provider_ready: boolean;
  api_key_configured: boolean;
  active_source: string;
  source_label: string;
  database_ready: boolean;
  foundation_stage: string;
  persisted_record_count: number;
  vector_row_count: number;
  ready_vector_count: number;
  pending_count: number;
  error_count: number;
  runnable_count: number;
  processed_count: number;
  success_count: number;
  skipped_count: number;
  sample_records: AdminEmbeddingReadinessRecord[];
  workflow_note: string;
};


const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

const pageWrap: React.CSSProperties = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top, rgba(45,78,180,0.20), transparent 24%), linear-gradient(180deg, #071226 0%, #09152b 100%)",
  color: "#f4f7ff",
  padding: "32px 0 72px",
};

const containerStyle: React.CSSProperties = {
  maxWidth: "1360px",
  margin: "0 auto",
  padding: "0 24px",
};

const cardStyle: React.CSSProperties = {
  background: "rgba(18, 28, 58, 0.92)",
  border: "1px solid rgba(120, 150, 255, 0.16)",
  borderRadius: "22px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.22)",
};

const softCardStyle: React.CSSProperties = {
  background: "rgba(10, 19, 43, 0.95)",
  border: "1px solid rgba(132, 151, 220, 0.14)",
  borderRadius: "18px",
  padding: "18px",
};

const secondaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "14px",
  padding: "14px 20px",
  background: "transparent",
  color: "#dfe7ff",
  fontWeight: 700,
  fontSize: "15px",
  cursor: "pointer",
  textDecoration: "none",
  border: "1px solid rgba(150, 170, 255, 0.26)",
};

const fieldStyle: React.CSSProperties = {
  width: "100%",
  borderRadius: "14px",
  border: "1px solid rgba(136, 159, 232, 0.18)",
  background: "rgba(8, 15, 35, 0.96)",
  color: "#eef3ff",
  padding: "14px 15px",
  fontSize: "14px",
  outline: "none",
};

const badge = (tone: "blue" | "green" | "pink" = "blue"): React.CSSProperties => ({
  display: "inline-flex",
  alignItems: "center",
  gap: "6px",
  padding: "7px 11px",
  borderRadius: "999px",
  fontSize: "12px",
  fontWeight: 700,
  border:
    tone === "green"
      ? "1px solid rgba(104, 216, 169, 0.22)"
      : tone === "pink"
        ? "1px solid rgba(255, 160, 180, 0.22)"
        : "1px solid rgba(126, 162, 255, 0.22)",
  background:
    tone === "green"
      ? "rgba(104, 216, 169, 0.10)"
      : tone === "pink"
        ? "rgba(255, 160, 180, 0.10)"
        : "rgba(126, 162, 255, 0.12)",
  color:
    tone === "green" ? "#bdf3d8" : tone === "pink" ? "#ffd7e2" : "#b9caff",
});

const chipStyle: React.CSSProperties = {
  padding: "6px 10px",
  borderRadius: "999px",
  background: "rgba(126, 162, 255, 0.10)",
  border: "1px solid rgba(126, 162, 255, 0.16)",
  color: "#dce6ff",
  fontSize: "12px",
  fontWeight: 600,
};

function prettyKind(value: string) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

function toneFromStatus(value: string): "blue" | "green" | "pink" {
  const lowered = value.toLowerCase();
  if (lowered.includes("block") || lowered.includes("error")) return "pink";
  if (lowered.includes("ready") || lowered.includes("pass")) return "green";
  return "blue";
}

function draftFormToPayload(draftForm: AdminDraftForm) {
  return {
    id: draftForm.id || undefined,
    source_title: draftForm.source_title,
    law_name: draftForm.law_name,
    section_number: draftForm.section_number,
    section_title: draftForm.section_title,
    summary: draftForm.summary,
    excerpt: draftForm.excerpt,
    citation_label: draftForm.citation_label,
    jurisdiction: draftForm.jurisdiction,
    provision_kind: draftForm.provision_kind,
    offence_group: draftForm.offence_group || null,
    punishment_summary: draftForm.punishment_summary || null,
    tags: textToList(draftForm.tags_text),
    aliases: textToList(draftForm.aliases_text),
    keywords: textToList(draftForm.keywords_text),
    related_sections: textToList(draftForm.related_sections_text),
  };
}

function listToText(values: string[]) {
  return values.join(", ");
}

function textToList(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function createEmptyDraftForm(): AdminDraftForm {
  return {
    id: "",
    source_title: "",
    law_name: "",
    section_number: "",
    section_title: "",
    summary: "",
    excerpt: "",
    citation_label: "",
    jurisdiction: "Pakistan",
    provision_kind: "general",
    offence_group: "",
    punishment_summary: "",
    tags_text: "",
    aliases_text: "",
    keywords_text: "",
    related_sections_text: "",
  };
}

function detailToDraft(detail: AdminSourceDetailResponse): AdminDraftForm {
  return {
    id: detail.item.id,
    source_title: detail.item.source_title,
    law_name: detail.item.law_name,
    section_number: detail.item.section_number,
    section_title: detail.item.section_title,
    summary: detail.item.summary,
    excerpt: detail.item.excerpt,
    citation_label: detail.item.citation_label,
    jurisdiction: detail.item.jurisdiction,
    provision_kind: detail.item.provision_kind,
    offence_group: detail.item.offence_group || "",
    punishment_summary: detail.item.punishment_summary || "",
    tags_text: listToText(detail.item.tags),
    aliases_text: listToText(detail.item.aliases),
    keywords_text: listToText(detail.item.keywords),
    related_sections_text: listToText(detail.item.related_sections),
  };
}



function payloadToDraftForm(payload: AdminWorkspaceDraftDetailResponse["payload"]): AdminDraftForm {
  return {
    id: payload.id || "",
    source_title: payload.source_title,
    law_name: payload.law_name,
    section_number: payload.section_number,
    section_title: payload.section_title,
    summary: payload.summary,
    excerpt: payload.excerpt,
    citation_label: payload.citation_label,
    jurisdiction: payload.jurisdiction,
    provision_kind: payload.provision_kind,
    offence_group: payload.offence_group || "",
    punishment_summary: payload.punishment_summary || "",
    tags_text: listToText(payload.tags),
    aliases_text: listToText(payload.aliases),
    keywords_text: listToText(payload.keywords),
    related_sections_text: listToText(payload.related_sections),
  };
}

function detailListCard(
  title: string,
  description: string,
  tone: "blue" | "green" | "pink" = "blue",
) {
  return (
    <div style={softCardStyle}>
      <div style={{ ...badge(tone), marginBottom: "10px" }}>{title}</div>
      <div style={{ color: "#dbe4ff", lineHeight: 1.65 }}>{description}</div>
    </div>
  );
}

export default function AdminPage() {
  const [summary, setSummary] = useState<AdminSummaryResponse | null>(null);
  const [catalog, setCatalog] = useState<AdminSourceCatalogResponse | null>(null);
  const [detail, setDetail] = useState<AdminSourceDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState("");
  const [search, setSearch] = useState("");
  const [selectedLaw, setSelectedLaw] = useState("all");
  const [selectedKind, setSelectedKind] = useState("all");
  const [selectedGroup, setSelectedGroup] = useState("all");
  const [selectedSourceId, setSelectedSourceId] = useState("");
  const [draftForm, setDraftForm] = useState<AdminDraftForm | null>(null);
  const [createForm, setCreateForm] = useState<AdminDraftForm>(createEmptyDraftForm());
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState("");
  const [createResult, setCreateResult] = useState<AdminSourceCreateResponse | null>(null);
  const [createTemplateNote, setCreateTemplateNote] = useState("");
  const [ingestionSourceTitle, setIngestionSourceTitle] = useState("Pakistan Penal Code");
  const [ingestionLawName, setIngestionLawName] = useState("Pakistan Penal Code");
  const [ingestionJurisdiction, setIngestionJurisdiction] = useState("Pakistan");
  const [ingestionCitationHint, setIngestionCitationHint] = useState("");
  const [ingestionRawText, setIngestionRawText] = useState("");
  const [ingestionLoading, setIngestionLoading] = useState(false);
  const [ingestionError, setIngestionError] = useState("");
  const [ingestionPreview, setIngestionPreview] = useState<AdminIngestionPreviewResponse | null>(null);
  const [ingestionBatchLoading, setIngestionBatchLoading] = useState(false);
  const [ingestionBatchError, setIngestionBatchError] = useState("");
  const [ingestionBatchMaxCandidates, setIngestionBatchMaxCandidates] = useState("5");
  const [ingestionBatchPreview, setIngestionBatchPreview] = useState<AdminIngestionBatchPreviewResponse | null>(null);
  const [persistUpdateLoading, setPersistUpdateLoading] = useState(false);
  const [persistUpdateError, setPersistUpdateError] = useState("");
  const [persistUpdateResult, setPersistUpdateResult] = useState<AdminSourceUpdateResponse | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState("");
  const [deleteResult, setDeleteResult] = useState<AdminSourceDeleteResponse | null>(null);
  const [draftLoading, setDraftLoading] = useState(false);
  const [draftError, setDraftError] = useState("");
  const [draftValidation, setDraftValidation] = useState<AdminSourceDraftValidationResponse | null>(null);
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewError, setReviewError] = useState("");
  const [draftReview, setDraftReview] = useState<AdminSourceDraftReviewResponse | null>(null);
  const [publishLoading, setPublishLoading] = useState(false);
  const [publishError, setPublishError] = useState("");
  const [publishPreview, setPublishPreview] = useState<AdminSourcePublishPreviewResponse | null>(null);
  const [workspace, setWorkspace] = useState<AdminWorkspaceResponse | null>(null);
  const [workspaceLoading, setWorkspaceLoading] = useState(true);
  const [workspaceError, setWorkspaceError] = useState("");
  const [workspaceDraftId, setWorkspaceDraftId] = useState("");
  const [workspaceBusy, setWorkspaceBusy] = useState(false);
  const [workspaceActionError, setWorkspaceActionError] = useState("");
  const [activity, setActivity] = useState<AdminActivityFeedResponse | null>(null);
  const [activityLoading, setActivityLoading] = useState(true);
  const [activityError, setActivityError] = useState("");
  const [probeQuery, setProbeQuery] = useState("Can police arrest someone without warrant for online blackmail?");
  const [probeResult, setProbeResult] = useState<AdminRetrievalProbeResponse | null>(null);
  const [probeLoading, setProbeLoading] = useState(false);
  const [probeError, setProbeError] = useState("");
  const [retrievalReadiness, setRetrievalReadiness] = useState<AdminRetrievalReadinessResponse | null>(null);
  const [retrievalReadinessLoading, setRetrievalReadinessLoading] = useState(true);
  const [retrievalReadinessError, setRetrievalReadinessError] = useState("");
  const [retrievalRefreshLoading, setRetrievalRefreshLoading] = useState(false);
  const [retrievalRefreshNote, setRetrievalRefreshNote] = useState("");
  const [embeddingReadiness, setEmbeddingReadiness] = useState<AdminEmbeddingReadinessResponse | null>(null);
  const [embeddingReadinessLoading, setEmbeddingReadinessLoading] = useState(true);
  const [embeddingReadinessError, setEmbeddingReadinessError] = useState("");
  const [embeddingRunLoading, setEmbeddingRunLoading] = useState(false);
  const [embeddingRunLimit, setEmbeddingRunLimit] = useState("10");
  const [embeddingRunNote, setEmbeddingRunNote] = useState("");
  const [selectedEmbeddingRunLoading, setSelectedEmbeddingRunLoading] = useState(false);
  const [selectedEmbeddingRunNote, setSelectedEmbeddingRunNote] = useState("");
  const [selectedEmbeddingRunError, setSelectedEmbeddingRunError] = useState("");

  async function loadAdminSnapshot(preferredSourceId?: string) {
    try {
      setLoading(true);
      setError("");

      const [summaryResponse, sourcesResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/admin/summary`, {
          method: "GET",
          cache: "no-store",
        }),
        fetch(`${API_BASE_URL}/api/v1/admin/sources`, {
          method: "GET",
          cache: "no-store",
        }),
      ]);

      if (!summaryResponse.ok) {
        throw new Error(`Summary request failed with status ${summaryResponse.status}`);
      }

      if (!sourcesResponse.ok) {
        throw new Error(`Source catalog request failed with status ${sourcesResponse.status}`);
      }

      const [summaryResult, catalogResult]: [AdminSummaryResponse, AdminSourceCatalogResponse] = await Promise.all([
        summaryResponse.json(),
        sourcesResponse.json(),
      ]);

      setSummary(summaryResult);
      setCatalog(catalogResult);

      if (catalogResult.items.length === 0) {
        setSelectedSourceId("");
        setDetail(null);
        return;
      }

      const preferredStillExists = preferredSourceId
        ? catalogResult.items.some((item) => item.id === preferredSourceId)
        : false;
      const currentStillExists = catalogResult.items.some((item) => item.id === selectedSourceId);
      const nextSelected = preferredStillExists
        ? preferredSourceId || catalogResult.items[0].id
        : currentStillExists
          ? selectedSourceId
          : catalogResult.items[0].id;

      setSelectedSourceId(nextSelected);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || "Failed to load admin workspace.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function loadWorkspace() {
    try {
      setWorkspaceLoading(true);
      setWorkspaceError("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace`, {
        method: "GET",
        cache: "no-store",
      });
      if (!response.ok) {
        throw new Error(`Workspace request failed with status ${response.status}`);
      }
      const result: AdminWorkspaceResponse = await response.json();
      setWorkspace(result);
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceError(err.message || "Failed to load workspace shelf.");
      }
    } finally {
      setWorkspaceLoading(false);
    }
  }

  async function loadActivity() {
    try {
      setActivityLoading(true);
      setActivityError("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/activity`, {
        method: "GET",
        cache: "no-store",
      });
      if (!response.ok) {
        throw new Error(`Activity request failed with status ${response.status}`);
      }
      const result: AdminActivityFeedResponse = await response.json();
      setActivity(result);
    } catch (err) {
      if (err instanceof Error) {
        setActivityError(err.message || "Failed to load admin activity.");
      }
    } finally {
      setActivityLoading(false);
    }
  }

  async function runRetrievalProbe(nextQuery?: string) {
    const query = (nextQuery ?? probeQuery).trim();
    if (!query) {
      setProbeError("Enter a retrieval query first.");
      return;
    }

    try {
      setProbeLoading(true);
      setProbeError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/retrieval-probe`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          limit: 6,
        }),
      });

      if (!response.ok) {
        throw new Error(`Retrieval probe failed with status ${response.status}`);
      }

      const result: AdminRetrievalProbeResponse = await response.json();
      setProbeResult(result);
    } catch (err) {
      if (err instanceof Error) {
        setProbeError(err.message || "Failed to run retrieval probe.");
      }
    } finally {
      setProbeLoading(false);
    }
  }

  async function loadRetrievalReadiness() {
    try {
      setRetrievalReadinessLoading(true);
      setRetrievalReadinessError("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/retrieval-readiness`, {
        method: "GET",
        cache: "no-store",
      });
      if (!response.ok) {
        throw new Error(`Retrieval readiness failed with status ${response.status}`);
      }
      const result: AdminRetrievalReadinessResponse = await response.json();
      setRetrievalReadiness(result);
    } catch (err) {
      if (err instanceof Error) {
        setRetrievalReadinessError(err.message || "Failed to load retrieval readiness.");
      }
    } finally {
      setRetrievalReadinessLoading(false);
    }
  }

  async function runRetrievalRefresh(forceAll = false) {
    try {
      setRetrievalRefreshLoading(true);
      setRetrievalRefreshNote("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/retrieval-readiness/refresh`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          force_all: forceAll,
        }),
      });
      if (!response.ok) {
        throw new Error(`Retrieval refresh failed with status ${response.status}`);
      }
      const result: AdminRetrievalRefreshResponse = await response.json();
      setRetrievalRefreshNote(result.workflow_note);
      await Promise.all([loadRetrievalReadiness(), loadAdminSnapshot(), loadWorkspace()]);
    } catch (err) {
      if (err instanceof Error) {
        setRetrievalReadinessError(err.message || "Failed to refresh retrieval metadata.");
      }
    } finally {
      setRetrievalRefreshLoading(false);
    }
  }

  async function loadEmbeddingReadiness() {
    try {
      setEmbeddingReadinessLoading(true);
      setEmbeddingReadinessError("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/embedding-readiness`, {
        method: "GET",
        cache: "no-store",
      });
      if (!response.ok) {
        throw new Error(`Embedding readiness failed with status ${response.status}`);
      }
      const result: AdminEmbeddingReadinessResponse = await response.json();
      setEmbeddingReadiness(result);
    } catch (err) {
      if (err instanceof Error) {
        setEmbeddingReadinessError(err.message || "Failed to load embedding readiness.");
      }
    } finally {
      setEmbeddingReadinessLoading(false);
    }
  }

  async function runEmbeddingGeneration() {
    const parsedLimit = Math.max(1, Number.parseInt(embeddingRunLimit || "10", 10) || 10);

    try {
      setEmbeddingRunLoading(true);
      setEmbeddingRunNote("");
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/embedding-readiness/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          limit: parsedLimit,
          record_ids: [],
        }),
      });
      if (!response.ok) {
        throw new Error(`Embedding run failed with status ${response.status}`);
      }
      const result: AdminEmbeddingRunResponse = await response.json();
      setEmbeddingRunNote(result.workflow_note);
      await Promise.all([loadEmbeddingReadiness(), loadRetrievalReadiness(), loadAdminSnapshot()]);
    } catch (err) {
      if (err instanceof Error) {
        setEmbeddingReadinessError(err.message || "Failed to run embedding generation.");
      }
    } finally {
      setEmbeddingRunLoading(false);
    }
  }

  async function runSelectedEmbeddingGeneration() {
    if (!selectedSourceId) {
      return;
    }

    try {
      setSelectedEmbeddingRunLoading(true);
      setSelectedEmbeddingRunNote("");
      setSelectedEmbeddingRunError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/embedding-readiness/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          limit: 1,
          record_ids: [selectedSourceId],
        }),
      });

      if (!response.ok) {
        throw new Error(`Selected embedding run failed with status ${response.status}`);
      }

      const result: AdminEmbeddingRunResponse = await response.json();
      setSelectedEmbeddingRunNote(result.workflow_note);

      await Promise.all([
        loadEmbeddingReadiness(),
        loadRetrievalReadiness(),
        loadAdminSnapshot(selectedSourceId),
        loadSourceDetail(selectedSourceId),
        loadActivity(),
      ]);
    } catch (err) {
      if (err instanceof Error) {
        setSelectedEmbeddingRunError(err.message || "Failed to run selected embedding refresh.");
      }
    } finally {
      setSelectedEmbeddingRunLoading(false);
    }
  }

  useEffect(() => {
    loadAdminSnapshot();
    loadWorkspace();
    loadActivity();
    loadRetrievalReadiness();
    loadEmbeddingReadiness();
    runRetrievalProbe("Can police arrest someone without warrant for online blackmail?");
  }, []);

  const filteredItems = useMemo(() => {
    if (!catalog) {
      return [];
    }

    const searchTerm = search.trim().toLowerCase();

    return catalog.items.filter((item) => {
      const matchesSearch =
        searchTerm.length === 0 ||
        [
          item.citation_label,
          item.law_name,
          item.section_number,
          item.section_title,
          item.summary,
          item.offence_group || "",
          item.provision_kind,
          item.tags.join(" "),
          item.related_sections.join(" "),
        ]
          .join(" ")
          .toLowerCase()
          .includes(searchTerm);

      const matchesLaw = selectedLaw === "all" || item.law_name === selectedLaw;
      const matchesKind = selectedKind === "all" || item.provision_kind === selectedKind;
      const matchesGroup =
        selectedGroup === "all" || (item.offence_group || "ungrouped") === selectedGroup;

      return matchesSearch && matchesLaw && matchesKind && matchesGroup;
    });
  }, [catalog, search, selectedLaw, selectedKind, selectedGroup]);

  useEffect(() => {
    if (filteredItems.length === 0) {
      setSelectedSourceId("");
      setDetail(null);
      return;
    }

    const currentStillVisible = filteredItems.some((item) => item.id === selectedSourceId);
    if (!currentStillVisible) {
      setSelectedSourceId(filteredItems[0].id);
    }
  }, [filteredItems, selectedSourceId]);

  async function loadSourceDetail(recordId: string) {
    try {
      setDetailLoading(true);
      setDetailError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/sources/${recordId}`, {
        method: "GET",
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`Detail request failed with status ${response.status}`);
      }

      const result: AdminSourceDetailResponse = await response.json();
      setDetail(result);
    } catch (err) {
      if (err instanceof Error) {
        setDetailError(err.message || "Failed to load source detail.");
      }
    } finally {
      setDetailLoading(false);
    }
  }

  useEffect(() => {
    if (!selectedSourceId) {
      return;
    }

    loadSourceDetail(selectedSourceId);
  }, [selectedSourceId]);

  useEffect(() => {
    if (!detail) {
      return;
    }

    setWorkspaceDraftId("");
    setWorkspaceDraftId("");
    setDraftForm(detailToDraft(detail));
    setDraftValidation(null);
    setDraftError("");
    setDraftReview(null);
    setReviewError("");
    setPublishPreview(null);
    setPublishError("");
    setPersistUpdateResult(null);
    setPersistUpdateError("");
    setDeleteResult(null);
    setDeleteError("");
    setSelectedEmbeddingRunNote("");
    setSelectedEmbeddingRunError("");
  }, [detail]);

  async function validateDraft() {
    if (!draftForm) {
      return;
    }

    try {
      setDraftLoading(true);
      setDraftError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/sources/validate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(draftFormToPayload(draftForm)),
      });

      if (!response.ok) {
        throw new Error(`Draft validation failed with status ${response.status}`);
      }

      const result: AdminSourceDraftValidationResponse = await response.json();
      setDraftValidation(result);
    } catch (err) {
      if (err instanceof Error) {
        setDraftError(err.message || "Failed to validate draft.");
      }
    } finally {
      setDraftLoading(false);
    }
  }

  async function runDraftReview() {
    if (!draftForm) {
      return;
    }

    try {
      setReviewLoading(true);
      setReviewError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/sources/review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(draftFormToPayload(draftForm)),
      });

      if (!response.ok) {
        throw new Error(`Draft review failed with status ${response.status}`);
      }

      const result: AdminSourceDraftReviewResponse = await response.json();
      setDraftReview(result);
    } catch (err) {
      if (err instanceof Error) {
        setReviewError(err.message || "Failed to run draft review.");
      }
    } finally {
      setReviewLoading(false);
    }
  }

  async function buildPublishPreview() {
    if (!draftForm) {
      return;
    }

    try {
      setPublishLoading(true);
      setPublishError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/sources/publish-preview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(draftFormToPayload(draftForm)),
      });

      if (!response.ok) {
        throw new Error(`Publish preview failed with status ${response.status}`);
      }

      const result: AdminSourcePublishPreviewResponse = await response.json();
      setPublishPreview(result);
    } catch (err) {
      if (err instanceof Error) {
        setPublishError(err.message || "Failed to build publish preview.");
      }
    } finally {
      setPublishLoading(false);
    }
  }


  async function saveDraftToWorkspace() {
    if (!draftForm) {
      return;
    }

    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/drafts/save`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          workspace_draft_id: workspaceDraftId || undefined,
          draft: draftFormToPayload(draftForm),
        }),
      });

      if (!response.ok) {
        throw new Error(`Workspace draft save failed with status ${response.status}`);
      }

      const result: AdminWorkspaceDraftDetailResponse = await response.json();
      setWorkspaceDraftId(result.workspace_draft.workspace_draft_id);
      setDraftForm(payloadToDraftForm(result.payload));
      setDraftValidation(result.validation);
      setDraftReview(result.review);
      setPublishPreview(result.publish_preview);
      await loadWorkspace();
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to save workspace draft.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  async function loadWorkspaceDraft(workspaceId: string) {
    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/drafts/${workspaceId}`, {
        method: "GET",
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`Workspace draft load failed with status ${response.status}`);
      }

      const result: AdminWorkspaceDraftDetailResponse = await response.json();
      setWorkspaceDraftId(result.workspace_draft.workspace_draft_id);
      setDraftForm(payloadToDraftForm(result.payload));
      setDraftValidation(result.validation);
      setDraftReview(result.review);
      setPublishPreview(result.publish_preview);
      setDraftError("");
      setReviewError("");
      setPublishError("");
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to load workspace draft.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  async function stagePublishPackage() {
    if (!draftForm) {
      return;
    }

    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/publish-packages/stage`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          workspace_draft_id: workspaceDraftId || undefined,
          draft: draftFormToPayload(draftForm),
        }),
      });

      if (!response.ok) {
        throw new Error(`Publish package staging failed with status ${response.status}`);
      }

      await response.json();
      await loadWorkspace();
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to stage publish package.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  async function publishStagedPackage(packageId: string) {
    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/publish-packages/${packageId}/publish`, {
        method: "POST",
      });

      if (!response.ok) {
        const fallbackText = await response.text();
        throw new Error(fallbackText || `Publish failed with status ${response.status}`);
      }

      const result: AdminPublishExecutionResponse = await response.json();
      await Promise.all([
        loadAdminSnapshot(result.published_record_id),
        loadWorkspace(),
        loadActivity(),
      ]);
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to publish staged package.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  async function deleteWorkspaceDraft(workspaceId: string) {
    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/drafts/${workspaceId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Workspace draft delete failed with status ${response.status}`);
      }

      if (workspaceDraftId === workspaceId) {
        setWorkspaceDraftId("");
      }
      await loadWorkspace();
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to delete workspace draft.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  async function deletePublishPackage(packageId: string) {
    try {
      setWorkspaceBusy(true);
      setWorkspaceActionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/workspace/publish-packages/${packageId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Publish package delete failed with status ${response.status}`);
      }

      await loadWorkspace();
    } catch (err) {
      if (err instanceof Error) {
        setWorkspaceActionError(err.message || "Failed to delete publish package.");
      }
    } finally {
      setWorkspaceBusy(false);
    }
  }

  function updateDraftField(field: keyof AdminDraftForm, value: string) {
    setDraftForm((current) => (current ? { ...current, [field]: value } : current));
    setDraftValidation(null);
    setDraftReview(null);
    setPublishPreview(null);
    setDraftError("");
    setReviewError("");
    setPublishError("");
    setWorkspaceActionError("");
  }

  function updateCreateField(field: keyof AdminDraftForm, value: string) {
    setCreateForm((current) => ({
      ...current,
      [field]: value,
    }));
    setCreateTemplateNote("");
  }

  function copyDraftToCreateForm() {
    if (!draftForm) {
      return;
    }

    setCreateForm({
      ...draftForm,
      id: "",
      citation_label: "",
    });
    setCreateResult(null);
    setCreateError("");
    setCreateTemplateNote(
      "Loaded the current source draft into the create workflow as a template. Review id and citation label before saving."
    );
  }

  async function runIngestionPreview() {
    if (!ingestionRawText.trim()) {
      setIngestionError("Paste legal source text first, then run ingestion preview.");
      return;
    }

    try {
      setIngestionLoading(true);
      setIngestionError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/ingestion/preview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          source_title: ingestionSourceTitle,
          law_name: ingestionLawName,
          jurisdiction: ingestionJurisdiction,
          citation_hint: ingestionCitationHint,
          raw_text: ingestionRawText,
        }),
      });

      if (!response.ok) {
        throw new Error(`Ingestion preview failed with status ${response.status}`);
      }

      const result: AdminIngestionPreviewResponse = await response.json();
      setIngestionPreview(result);
      setIngestionBatchError("");
      setCreateForm(result.draft);
      setCreateResult(null);
      setCreateError("");
      setCreateTemplateNote(
        "Loaded parsed ingestion preview into the create form. Review the extracted fields, then save the new source record."
      );
    } catch (err) {
      if (err instanceof Error) {
        setIngestionError(err.message || "Failed to build ingestion preview.");
      }
    } finally {
      setIngestionLoading(false);
    }
  }

  function loadIngestionCandidateIntoCreateForm(item: AdminIngestionPreviewResponse) {
    setCreateForm(item.draft);
    setCreateResult(null);
    setCreateError("");
    setCreateTemplateNote(
      "Loaded an ingestion candidate into the create form. Review extracted fields and duplicate warnings before saving."
    );
  }

  async function runBatchIngestionPreview() {
    if (!ingestionRawText.trim()) {
      setIngestionBatchError("Paste legal source text first, then run batch preview.");
      return;
    }

    try {
      setIngestionBatchLoading(true);
      setIngestionBatchError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/ingestion/batch-preview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          source_title: ingestionSourceTitle,
          law_name: ingestionLawName,
          jurisdiction: ingestionJurisdiction,
          citation_hint: ingestionCitationHint,
          raw_text: ingestionRawText,
          max_candidates: Math.max(1, Number.parseInt(ingestionBatchMaxCandidates || "5", 10) || 5),
        }),
      });

      if (!response.ok) {
        throw new Error(`Batch ingestion preview failed with status ${response.status}`);
      }

      const result: AdminIngestionBatchPreviewResponse = await response.json();
      setIngestionBatchPreview(result);
      if (result.items.length > 0) {
        loadIngestionCandidateIntoCreateForm(result.items[0]);
      }
    } catch (err) {
      if (err instanceof Error) {
        setIngestionBatchError(err.message || "Failed to build batch ingestion preview.");
      }
    } finally {
      setIngestionBatchLoading(false);
    }
  }

  async function submitCreateRecord() {
    try {
      setCreateLoading(true);
      setCreateError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/source-records`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(draftFormToPayload(createForm)),
      });

      if (!response.ok) {
        throw new Error(`Create source request failed with status ${response.status}`);
      }

      const result: AdminSourceCreateResponse = await response.json();
      setCreateResult(result);

      if (result.create_status === "created" && result.record_id) {
        await Promise.all([
          loadAdminSnapshot(result.record_id),
          loadRetrievalReadiness(),
          loadEmbeddingReadiness(),
          loadActivity(),
        ]);
        setCreateForm(createEmptyDraftForm());
        setCreateTemplateNote("");
      }
    } catch (err) {
      if (err instanceof Error) {
        setCreateError(err.message || "Failed to create source record.");
      }
    } finally {
      setCreateLoading(false);
    }
  }

  async function submitPersistedUpdate() {
    if (!draftForm || !selectedSourceId) {
      return;
    }

    try {
      setPersistUpdateLoading(true);
      setPersistUpdateError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/source-records/${selectedSourceId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(draftFormToPayload(draftForm)),
      });

      if (!response.ok) {
        throw new Error(`Persisted update failed with status ${response.status}`);
      }

      const result: AdminSourceUpdateResponse = await response.json();
      setPersistUpdateResult(result);

      if (result.update_status === "updated" && selectedSourceId) {
        await Promise.all([
          loadAdminSnapshot(selectedSourceId),
          loadSourceDetail(selectedSourceId),
          loadRetrievalReadiness(),
          loadEmbeddingReadiness(),
          loadActivity(),
        ]);
      }
    } catch (err) {
      if (err instanceof Error) {
        setPersistUpdateError(err.message || "Failed to save persisted update.");
      }
    } finally {
      setPersistUpdateLoading(false);
    }
  }

  async function submitDeleteSource() {
    if (!selectedSourceId) {
      return;
    }

    const confirmation = window.confirm("Delete this legal source record from the active store?");
    if (!confirmation) {
      return;
    }

    try {
      setDeleteLoading(true);
      setDeleteError("");

      const response = await fetch(`${API_BASE_URL}/api/v1/admin/source-records/${selectedSourceId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Delete request failed with status ${response.status}`);
      }

      const result: AdminSourceDeleteResponse = await response.json();
      setDeleteResult(result);

      if (result.delete_status === "deleted") {
        await Promise.all([
          loadAdminSnapshot(),
          loadRetrievalReadiness(),
          loadEmbeddingReadiness(),
          loadActivity(),
        ]);
      }
    } catch (err) {
      if (err instanceof Error) {
        setDeleteError(err.message || "Failed to delete source record.");
      }
    } finally {
      setDeleteLoading(false);
    }
  }

  function resetDraftFromSelected() {
    if (!detail) {
      return;
    }
    setDraftForm(detailToDraft(detail));
    setDraftValidation(null);
    setDraftError("");
    setDraftReview(null);
    setReviewError("");
    setPublishPreview(null);
    setPublishError("");
  }

  function startBlankDraft() {
    setWorkspaceDraftId("");
    setDraftForm({
      id: "",
      source_title: "",
      law_name: "Pakistan Penal Code",
      section_number: "",
      section_title: "",
      summary: "",
      excerpt: "",
      citation_label: "",
      jurisdiction: "Pakistan",
      provision_kind: "general",
      offence_group: "",
      punishment_summary: "",
      tags_text: "",
      aliases_text: "",
      keywords_text: "",
      related_sections_text: "",
    });
    setDraftValidation(null);
    setDraftError("");
    setDraftReview(null);
    setReviewError("");
    setPublishPreview(null);
    setPublishError("");
    setWorkspaceActionError("");
  }

  const filteredPunishmentCount = filteredItems.filter(
    (item) => item.provision_kind === "punishment",
  ).length;

  const filteredProcedureCount = filteredItems.filter(
    (item) => item.provision_kind === "procedure",
  ).length;

  const filteredLawCount = new Set(filteredItems.map((item) => item.law_name)).size;

  const selectedRecordVisible = filteredItems.some((item) => item.id === selectedSourceId);

  return (
    <main style={pageWrap}>
      <div style={containerStyle}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "16px",
            marginBottom: "28px",
            flexWrap: "wrap",
          }}
        >
          <div>
            <div style={{ ...badge(), marginBottom: "12px" }}>Admin source workspace</div>

            <h1
              style={{
                fontSize: "44px",
                lineHeight: 1.08,
                letterSpacing: "-1px",
                margin: "0 0 10px",
              }}
            >
              Admin Panel
            </h1>

            <p
              style={{
                margin: 0,
                maxWidth: "900px",
                color: "#c8d6f7",
                fontSize: "18px",
                lineHeight: 1.65,
              }}
            >
              The admin workspace now supports a real source-detail flow plus a prototype review gate. You can filter the live
              prototype catalog, select one record, edit a draft, validate it, compare change scope,
              and build a publish preview before later real save and approval workflows are introduced.
            </p>
          </div>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <Link href="/" style={secondaryButton}>
              Back to Homepage
            </Link>
            <Link href="/chat" style={secondaryButton}>
              Open Chat
            </Link>
          </div>
        </div>

        {loading && (
          <div style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
            Loading admin workspace...
          </div>
        )}

        {error && (
          <div
            style={{
              ...cardStyle,
              padding: "24px",
              marginBottom: "24px",
              border: "1px solid rgba(255, 120, 120, 0.25)",
              color: "#ffe1e1",
            }}
          >
            Failed to load admin workspace: {error}
          </div>
        )}

        {summary && catalog && (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
                gap: "18px",
                marginBottom: "24px",
              }}
            >
              {summary.stats.map((item) => (
                <div key={item.title} style={softCardStyle}>
                  <div
                    style={{
                      fontSize: "34px",
                      fontWeight: 800,
                      marginBottom: "8px",
                      color: "#ffffff",
                    }}
                  >
                    {item.value}
                  </div>
                  <div
                    style={{
                      fontSize: "16px",
                      fontWeight: 700,
                      marginBottom: "8px",
                      color: "#dfe7ff",
                    }}
                  >
                    {item.title}
                  </div>
                  <div
                    style={{
                      color: "#c6d3f3",
                      lineHeight: 1.6,
                      fontSize: "14px",
                    }}
                  >
                    {item.description}
                  </div>
                </div>
              ))}
            </div>

            {summary.catalog_source && (
              <div style={{ ...cardStyle, padding: "22px", marginBottom: "24px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: "16px", flexWrap: "wrap", marginBottom: "14px" }}>
                  <div>
                    <div style={{ ...badge(summary.catalog_source.active_source === "database" ? "green" : "blue"), marginBottom: "10px" }}>
                      {summary.catalog_source.source_label}
                    </div>
                    <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "8px" }}>
                      Active source store
                    </div>
                    <div style={{ color: "#d6e2ff", lineHeight: 1.7, maxWidth: "900px" }}>
                      {summary.catalog_source.detail}
                    </div>
                  </div>

                  <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignContent: "flex-start" }}>
                    <div style={chipStyle}>Stage: {prettyKind(summary.catalog_source.foundation_stage)}</div>
                    <div style={chipStyle}>Active records: {summary.catalog_source.active_record_count}</div>
                    <div style={chipStyle}>Persisted rows: {summary.catalog_source.persisted_record_count}</div>
                  </div>
                </div>
              </div>
            )}

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                gap: "24px",
                alignItems: "start",
                marginBottom: "24px",
              }}
            >
              <section style={{ ...cardStyle, padding: "24px" }}>
                <div style={{ ...badge(), marginBottom: "12px" }}>Connected now</div>
                <div
                  style={{
                    fontSize: "26px",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Source management snapshot
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
                    gap: "12px",
                    marginBottom: "18px",
                  }}
                >
                  <div style={softCardStyle}>
                    <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                      Records in view
                    </div>
                    <div style={{ fontSize: "28px", fontWeight: 800 }}>{filteredItems.length}</div>
                  </div>
                  <div style={softCardStyle}>
                    <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                      Laws in view
                    </div>
                    <div style={{ fontSize: "28px", fontWeight: 800 }}>{filteredLawCount}</div>
                  </div>
                  <div style={softCardStyle}>
                    <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                      Punishment records
                    </div>
                    <div style={{ fontSize: "28px", fontWeight: 800 }}>{filteredPunishmentCount}</div>
                  </div>
                  <div style={softCardStyle}>
                    <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                      Procedure records
                    </div>
                    <div style={{ fontSize: "28px", fontWeight: 800 }}>{filteredProcedureCount}</div>
                  </div>
                </div>

                {catalog.catalog_source && (
                  <div style={{ ...softCardStyle, marginBottom: "16px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", flexWrap: "wrap", marginBottom: "8px" }}>
                      <div style={{ fontWeight: 700, color: "#ffffff" }}>Catalog source</div>
                      <div style={badge(catalog.catalog_source.active_source === "database" ? "green" : "blue")}>
                        {catalog.catalog_source.source_label}
                      </div>
                    </div>
                    <div style={{ color: "#d6e2ff", lineHeight: 1.7, marginBottom: "8px" }}>
                      {catalog.catalog_source.detail}
                    </div>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      <div style={chipStyle}>Active {catalog.catalog_source.active_record_count}</div>
                      <div style={chipStyle}>Persisted {catalog.catalog_source.persisted_record_count}</div>
                      <div style={chipStyle}>{prettyKind(catalog.catalog_source.foundation_stage)}</div>
                    </div>
                  </div>
                )}

                <div style={{ color: "#d6e2ff", lineHeight: 1.7, marginBottom: "16px" }}>
                  {catalog.workflow_note}
                </div>

                <div style={{ display: "grid", gap: "14px" }}>
                  {summary.control_areas.map((item) => (
                    <div key={item.title} style={softCardStyle}>
                      <div
                        style={{
                          fontSize: "16px",
                          fontWeight: 700,
                          marginBottom: "8px",
                          color: "#ffffff",
                        }}
                      >
                        {item.title}
                      </div>
                      <div style={{ color: "#c6d3f3", lineHeight: 1.65 }}>{item.text}</div>
                    </div>
                  ))}
                </div>
              </section>

              <section style={{ ...cardStyle, padding: "24px" }}>
                <div style={{ ...badge("green"), marginBottom: "12px" }}>Current status</div>
                <div
                  style={{
                    fontSize: "26px",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Prototype governance overview
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                    gap: "16px",
                    marginBottom: "18px",
                  }}
                >
                  {summary.status_cards.map((item) => (
                    <div key={item.title} style={softCardStyle}>
                      <div
                        style={{
                          fontSize: "13px",
                          fontWeight: 700,
                          letterSpacing: "1px",
                          textTransform: "uppercase",
                          color: "#a9c1ff",
                          marginBottom: "8px",
                        }}
                      >
                        {item.title}
                      </div>
                      <div style={{ color: "#f4f7ff", lineHeight: 1.7 }}>{item.content}</div>
                    </div>
                  ))}
                </div>

                <div style={{ ...softCardStyle, marginBottom: "18px" }}>
                  <div
                    style={{
                      fontSize: "13px",
                      fontWeight: 700,
                      letterSpacing: "1px",
                      textTransform: "uppercase",
                      color: "#a9c1ff",
                      marginBottom: "12px",
                    }}
                  >
                    Recommended admin workflow
                  </div>

                  <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                    {summary.workflow_steps.map((item, index) => (
                      <div key={item} style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                        <div
                          style={{
                            minWidth: "30px",
                            height: "30px",
                            borderRadius: "999px",
                            background: "rgba(126, 162, 255, 0.18)",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            fontWeight: 700,
                            color: "#dfe7ff",
                            fontSize: "14px",
                          }}
                        >
                          {index + 1}
                        </div>
                        <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(58, 22, 32, 0.75), rgba(45, 18, 26, 0.78))",
                    border: "1px solid rgba(255, 150, 170, 0.18)",
                    borderRadius: "18px",
                    padding: "18px",
                  }}
                >
                  <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>
                    Important admin boundary
                  </div>
                  <div style={{ color: "#ffe7ec", lineHeight: 1.7, fontSize: "15px" }}>
                    {summary.admin_boundary}
                  </div>
                </div>
              </section>
            </div>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge("green"), marginBottom: "12px" }}>Phase 6 create workflow</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
                Create a persisted legal source record
              </div>

              <div style={{ color: "#dbe4ff", lineHeight: 1.7, marginBottom: "18px", maxWidth: "980px" }}>
                This is the first database-backed creation form for admin. Submit a new legal source draft here and the backend will validate it, build retrieval metadata, and save it to the database when persistence is available.
              </div>

              <div style={{ ...softCardStyle, display: "grid", gap: "14px", marginBottom: "18px" }}>
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
                  <div style={badge("green")}>Phase 7 ingestion preview</div>
                  <div style={{ color: "#dbe4ff" }}>Paste legal text and turn it into a draft-ready create form.</div>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px" }}>
                  <div>
                    <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Source title</div>
                    <input value={ingestionSourceTitle} onChange={(event) => setIngestionSourceTitle(event.target.value)} style={fieldStyle} placeholder="Pakistan Penal Code" />
                  </div>
                  <div>
                    <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Law name</div>
                    <input value={ingestionLawName} onChange={(event) => setIngestionLawName(event.target.value)} style={fieldStyle} placeholder="Pakistan Penal Code" />
                  </div>
                  <div>
                    <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Jurisdiction</div>
                    <input value={ingestionJurisdiction} onChange={(event) => setIngestionJurisdiction(event.target.value)} style={fieldStyle} placeholder="Pakistan" />
                  </div>
                  <div>
                    <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Citation hint</div>
                    <input value={ingestionCitationHint} onChange={(event) => setIngestionCitationHint(event.target.value)} style={fieldStyle} placeholder="optional override" />
                  </div>
                </div>

                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Pasted legal text</div>
                  <textarea
                    value={ingestionRawText}
                    onChange={(event) => setIngestionRawText(event.target.value)}
                    rows={8}
                    style={{ ...fieldStyle, resize: "vertical", minHeight: "180px" }}
                    placeholder="Paste a legal section, article, or source excerpt here..."
                  />
                </div>

                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
                  <button type="button" onClick={runIngestionPreview} style={secondaryButton} disabled={ingestionLoading}>
                    {ingestionLoading ? "Previewing..." : "Preview ingestion"}
                  </button>
                  <button type="button" onClick={runBatchIngestionPreview} style={secondaryButton} disabled={ingestionBatchLoading}>
                    {ingestionBatchLoading ? "Splitting..." : "Preview batch"}
                  </button>
                  <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                    <div style={{ color: "#a9c1ff", fontSize: "13px" }}>Max candidates</div>
                    <input
                      value={ingestionBatchMaxCandidates}
                      onChange={(event) => setIngestionBatchMaxCandidates(event.target.value)}
                      style={{ ...fieldStyle, width: "90px" }}
                      placeholder="5"
                    />
                  </div>
                </div>

                {ingestionError && (
                  <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                    {ingestionError}
                  </div>
                )}

                {ingestionBatchError && (
                  <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                    {ingestionBatchError}
                  </div>
                )}

                {ingestionBatchPreview && (
                  <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                      <div style={badge("green")}>Batch preview</div>
                      <div style={{ color: "#dbe4ff" }}>{ingestionBatchPreview.workflow_note}</div>
                    </div>

                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      <div style={chipStyle}>Items {ingestionBatchPreview.item_count}</div>
                    </div>

                    <div style={{ display: "grid", gap: "10px" }}>
                      {ingestionBatchPreview.items.map((item, index) => (
                        <div key={`${item.draft.section_number}-${index}`} style={{ ...glassCardStyle, display: "grid", gap: "8px" }}>
                          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                            <div style={chipStyle}>Candidate {index + 1}</div>
                            <div style={chipStyle}>Section {item.extracted_section_number || "—"}</div>
                            <div style={chipStyle}>Readiness {item.validation.readiness_score}</div>
                            <div style={chipStyle}>Duplicates {item.duplicate_candidates.length}</div>
                          </div>
                          <div style={{ color: "#ffffff", fontWeight: 600 }}>{item.extracted_section_title || item.draft.section_title || "Untitled section"}</div>
                          <div style={{ color: "#dbe4ff" }}>{item.draft.citation_label || item.draft.law_name}</div>
                          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                            <div style={chipStyle}>Kind: {item.draft.provision_kind || "—"}</div>
                            <div style={chipStyle}>Group: {item.draft.offence_group || "—"}</div>
                            <div style={chipStyle}>Related: {item.draft.related_sections_text || "—"}</div>
                          </div>
                          <div>
                            <button type="button" onClick={() => loadIngestionCandidateIntoCreateForm(item)} style={secondaryButton}>
                              Load candidate into create form
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {ingestionPreview && (
                  <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      <div style={chipStyle}>Readiness {ingestionPreview.validation.readiness_score}</div>
                      <div style={chipStyle}>Issues {ingestionPreview.validation.issue_count}</div>
                      <div style={chipStyle}>Errors {ingestionPreview.validation.error_count}</div>
                      <div style={chipStyle}>Warnings {ingestionPreview.validation.warning_count}</div>
                    </div>

                    <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{ingestionPreview.workflow_note}</div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "10px" }}>
                      <div style={chipStyle}>Extracted title: {ingestionPreview.extracted_title || "—"}</div>
                      <div style={chipStyle}>Section number: {ingestionPreview.extracted_section_number || "—"}</div>
                      <div style={chipStyle}>Section title: {ingestionPreview.extracted_section_title || "—"}</div>
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "10px" }}>
                      <div style={chipStyle}>Provision kind: {ingestionPreview.draft.provision_kind || "—"}</div>
                      <div style={chipStyle}>Offence group: {ingestionPreview.draft.offence_group || "—"}</div>
                      <div style={chipStyle}>Related sections: {ingestionPreview.draft.related_sections_text || "—"}</div>
                    </div>

                    {ingestionPreview.draft.punishment_summary && (
                      <div style={{ ...softCardStyle, color: "#dbe4ff", lineHeight: 1.7 }}>
                        <strong style={{ color: "#ffffff" }}>Punishment hint:</strong> {ingestionPreview.draft.punishment_summary}
                      </div>
                    )}

                    {ingestionPreview.duplicate_candidates.length > 0 && (
                      <div style={{ ...softCardStyle, display: "grid", gap: "12px", border: "1px solid rgba(255, 184, 77, 0.25)" }}>
                        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                          <div style={badge("yellow")}>Possible duplicates</div>
                          <div style={{ color: "#ffe8bf" }}>
                            Review these before saving the new source record.
                          </div>
                        </div>

                        <div style={{ display: "grid", gap: "10px" }}>
                          {ingestionPreview.duplicate_candidates.map((candidate) => (
                            <div key={candidate.record_id} style={{ ...glassCardStyle, display: "grid", gap: "8px" }}>
                              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                                <div style={chipStyle}>{candidate.citation_label}</div>
                                <div style={chipStyle}>Record id: {candidate.record_id}</div>
                              </div>
                              <div style={{ color: "#ffffff", fontWeight: 600 }}>{candidate.section_title || "Untitled section"}</div>
                              <div style={{ color: "#dbe4ff" }}>{candidate.law_name}</div>
                              <div style={{ color: "#ffe8bf" }}>Match reason: {candidate.match_reason}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px", marginBottom: "16px" }}>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Optional custom id</div>
                  <input value={createForm.id} onChange={(event) => updateCreateField("id", event.target.value)} style={fieldStyle} placeholder="auto-generated if empty" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Source title</div>
                  <input value={createForm.source_title} onChange={(event) => updateCreateField("source_title", event.target.value)} style={fieldStyle} placeholder="Pakistan Penal Code" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Law name</div>
                  <input value={createForm.law_name} onChange={(event) => updateCreateField("law_name", event.target.value)} style={fieldStyle} placeholder="Pakistan Penal Code" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Section number</div>
                  <input value={createForm.section_number} onChange={(event) => updateCreateField("section_number", event.target.value)} style={fieldStyle} placeholder="503" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Section title</div>
                  <input value={createForm.section_title} onChange={(event) => updateCreateField("section_title", event.target.value)} style={fieldStyle} placeholder="Criminal intimidation" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Citation label</div>
                  <input value={createForm.citation_label} onChange={(event) => updateCreateField("citation_label", event.target.value)} style={fieldStyle} placeholder="Pakistan Penal Code s. 503" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Jurisdiction</div>
                  <input value={createForm.jurisdiction} onChange={(event) => updateCreateField("jurisdiction", event.target.value)} style={fieldStyle} placeholder="Pakistan" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Provision kind</div>
                  <select value={createForm.provision_kind} onChange={(event) => updateCreateField("provision_kind", event.target.value)} style={fieldStyle}>
                    <option value="general">General</option>
                    <option value="punishment">Punishment</option>
                    <option value="procedure">Procedure</option>
                    <option value="authority">Authority</option>
                    <option value="bailability">Bailability</option>
                    <option value="fir_rule">FIR Rule</option>
                    <option value="reporting">Reporting</option>
                  </select>
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Offence group</div>
                  <input value={createForm.offence_group} onChange={(event) => updateCreateField("offence_group", event.target.value)} style={fieldStyle} placeholder="Threats and intimidation" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Tags</div>
                  <input value={createForm.tags_text} onChange={(event) => updateCreateField("tags_text", event.target.value)} style={fieldStyle} placeholder="threat, intimidation" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Aliases</div>
                  <input value={createForm.aliases_text} onChange={(event) => updateCreateField("aliases_text", event.target.value)} style={fieldStyle} placeholder="criminal threat" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Keywords</div>
                  <input value={createForm.keywords_text} onChange={(event) => updateCreateField("keywords_text", event.target.value)} style={fieldStyle} placeholder="blackmail, threat, fear" />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Related sections</div>
                  <input value={createForm.related_sections_text} onChange={(event) => updateCreateField("related_sections_text", event.target.value)} style={fieldStyle} placeholder="506" />
                </div>
              </div>

              <div style={{ display: "grid", gap: "12px", marginBottom: "16px" }}>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Summary</div>
                  <textarea value={createForm.summary} onChange={(event) => updateCreateField("summary", event.target.value)} rows={3} style={{ ...fieldStyle, resize: "vertical", minHeight: "92px" }} />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Excerpt</div>
                  <textarea value={createForm.excerpt} onChange={(event) => updateCreateField("excerpt", event.target.value)} rows={4} style={{ ...fieldStyle, resize: "vertical", minHeight: "110px" }} />
                </div>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Punishment summary</div>
                  <textarea value={createForm.punishment_summary} onChange={(event) => updateCreateField("punishment_summary", event.target.value)} rows={2} style={{ ...fieldStyle, resize: "vertical", minHeight: "74px" }} />
                </div>
              </div>

              <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "16px" }}>
                <button type="button" onClick={() => submitCreateRecord()} style={secondaryButton} disabled={createLoading}>
                  {createLoading ? "Creating..." : "Create source record"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setCreateForm(createEmptyDraftForm());
                    setCreateResult(null);
                    setCreateError("");
                    setCreateTemplateNote("");
                  }}
                  style={secondaryButton}
                  disabled={createLoading}
                >
                  Reset form
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setCreateForm({
                      id: "",
                      source_title: "Pakistan Penal Code",
                      law_name: "Pakistan Penal Code",
                      section_number: "503",
                      section_title: "Criminal intimidation",
                      summary: "Defines criminal intimidation and threat-based conduct used to cause alarm or compel action.",
                      excerpt: "Whoever threatens another with injury to person, reputation, or property...",
                      citation_label: "Pakistan Penal Code s. 503",
                      jurisdiction: "Pakistan",
                      provision_kind: "general",
                      offence_group: "Threats and intimidation",
                      punishment_summary: "Punishment is addressed in the linked punishment provision.",
                      tags_text: "threat, intimidation",
                      aliases_text: "criminal threat",
                      keywords_text: "blackmail, threat, fear",
                      related_sections_text: "506",
                    });
                    setCreateTemplateNote("");
                  }}
                  style={secondaryButton}
                  disabled={createLoading}
                >
                  Load sample
                </button>
              </div>

              {createTemplateNote && (
                <div style={{ ...softCardStyle, color: "#dbe4ff", lineHeight: 1.7, marginBottom: "16px" }}>
                  {createTemplateNote}
                </div>
              )}

              {createError && (
                <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1", marginBottom: "16px" }}>
                  {createError}
                </div>
              )}

              {createResult && (
                <div style={{ display: "grid", gap: "14px" }}>
                  <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                    <div style={badge(createResult.create_status === "created" ? "green" : "pink")}>
                      {prettyKind(createResult.create_status)}
                    </div>
                    <div style={badge(createResult.save_mode === "database" ? "green" : "blue")}>
                      Save mode: {prettyKind(createResult.save_mode)}
                    </div>
                    {createResult.record_id && <div style={badge()}>Record id: {createResult.record_id}</div>}
                  </div>

                  <div style={softCardStyle}>
                    <div style={{ color: "#dbe4ff", lineHeight: 1.7, marginBottom: "10px" }}>{createResult.workflow_note}</div>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      <div style={chipStyle}>Readiness {createResult.validation.readiness_score}</div>
                      <div style={chipStyle}>Issues {createResult.validation.issue_count}</div>
                      <div style={chipStyle}>Errors {createResult.validation.error_count}</div>
                      <div style={chipStyle}>Warnings {createResult.validation.warning_count}</div>
                    </div>
                  </div>

                  {createResult.validation.issues.length > 0 && (
                    <div style={{ display: "grid", gap: "10px" }}>
                      {createResult.validation.issues.map((issue, index) => (
                        <div key={`${issue.field}-${index}`} style={softCardStyle}>
                          <div style={{ ...badge(issue.level === "error" ? "pink" : "blue"), marginBottom: "8px" }}>
                            {issue.level.toUpperCase()}
                          </div>
                          <div style={{ fontWeight: 700, marginBottom: "6px" }}>{issue.field}</div>
                          <div style={{ color: "#dbe4ff", lineHeight: 1.65 }}>{issue.message}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge(), marginBottom: "12px" }}>Phase 4 detail workflow</div>
              <div
                style={{
                  fontSize: "26px",
                  fontWeight: 700,
                  marginBottom: "16px",
                }}
              >
                Source catalog + record detail
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))",
                  gap: "12px",
                  marginBottom: "18px",
                }}
              >
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>
                    Search records
                  </div>
                  <input
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                    placeholder="Search section, law, title, tags..."
                    style={fieldStyle}
                  />
                </div>

                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>
                    Law filter
                  </div>
                  <select
                    value={selectedLaw}
                    onChange={(event) => setSelectedLaw(event.target.value)}
                    style={fieldStyle}
                  >
                    <option value="all">All laws</option>
                    {catalog.available_laws.map((law) => (
                      <option key={law} value={law}>
                        {law}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>
                    Provision kind
                  </div>
                  <select
                    value={selectedKind}
                    onChange={(event) => setSelectedKind(event.target.value)}
                    style={fieldStyle}
                  >
                    <option value="all">All kinds</option>
                    {catalog.available_kinds.map((kind) => (
                      <option key={kind} value={kind}>
                        {prettyKind(kind)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>
                    Offence group
                  </div>
                  <select
                    value={selectedGroup}
                    onChange={(event) => setSelectedGroup(event.target.value)}
                    style={fieldStyle}
                  >
                    <option value="all">All groups</option>
                    {catalog.available_groups.map((group) => (
                      <option key={group} value={group}>
                        {prettyKind(group)}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "10px",
                  marginBottom: "18px",
                }}
              >
                <div style={badge()}>{filteredItems.length} records</div>
                <div style={badge("green")}>{filteredLawCount} laws visible</div>
                <div style={badge()}>{filteredPunishmentCount} punishment sections</div>
                <div style={badge()}>{filteredProcedureCount} procedure sections</div>
                {selectedRecordVisible && detail && (
                  <div style={badge("pink")}>Selected: {detail.item.citation_label}</div>
                )}
              </div>

              {filteredItems.length === 0 ? (
                <div style={softCardStyle}>
                  No source records matched the current filters. Try clearing one or more filters.
                </div>
              ) : (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
                    gap: "18px",
                    alignItems: "start",
                  }}
                >
                  <div style={{ display: "grid", gap: "14px" }}>
                    {filteredItems.map((item) => {
                      const isSelected = item.id === selectedSourceId;

                      return (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => setSelectedSourceId(item.id)}
                          style={{
                            ...softCardStyle,
                            textAlign: "left",
                            cursor: "pointer",
                            border: isSelected
                              ? "1px solid rgba(126, 162, 255, 0.46)"
                              : "1px solid rgba(132, 151, 220, 0.14)",
                            boxShadow: isSelected
                              ? "0 0 0 1px rgba(126, 162, 255, 0.16), 0 10px 24px rgba(24, 42, 92, 0.28)"
                              : "none",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "space-between",
                              gap: "12px",
                              marginBottom: "12px",
                              flexWrap: "wrap",
                            }}
                          >
                            <div style={{ ...badge(), fontSize: "11px" }}>{item.citation_label}</div>
                            <div style={{ ...badge("green"), fontSize: "11px" }}>
                              {prettyKind(item.provision_kind)}
                            </div>
                          </div>

                          <div style={{ fontSize: "19px", fontWeight: 700, marginBottom: "8px" }}>
                            {item.section_title}
                          </div>

                          <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "10px" }}>
                            {item.law_name} • Section {item.section_number}
                          </div>

                          <div style={{ color: "#dbe4ff", lineHeight: 1.65, marginBottom: "14px" }}>
                            {item.summary}
                          </div>

                          <div style={{ display: "grid", gap: "10px", marginBottom: "12px" }}>
                            <div style={{ color: "#c7d6ff", fontSize: "13px" }}>
                              <strong style={{ color: "#ffffff" }}>Admin note:</strong> {item.admin_note}
                            </div>
                            <div style={{ color: "#c7d6ff", fontSize: "13px" }}>
                              <strong style={{ color: "#ffffff" }}>Group:</strong>{" "}
                              {item.offence_group ? prettyKind(item.offence_group) : "Unassigned"}
                            </div>
                            {item.related_sections.length > 0 && (
                              <div style={{ color: "#c7d6ff", fontSize: "13px" }}>
                                <strong style={{ color: "#ffffff" }}>Related:</strong>{" "}
                                {item.related_sections.join(", ")}
                              </div>
                            )}
                            {item.punishment_summary && (
                              <div style={{ color: "#c7d6ff", fontSize: "13px" }}>
                                <strong style={{ color: "#ffffff" }}>Punishment note:</strong>{" "}
                                {item.punishment_summary}
                              </div>
                            )}
                          </div>

                          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                            {item.tags.slice(0, 5).map((tag) => (
                              <span key={`${item.id}-${tag}`} style={chipStyle}>
                                {tag}
                              </span>
                            ))}
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  <div style={{ ...cardStyle, padding: "22px", position: "sticky", top: "20px" }}>
                    <div style={{ ...badge("green"), marginBottom: "12px" }}>Selected record</div>

                    {!selectedRecordVisible && (
                      <div style={softCardStyle}>
                        The previously selected record is hidden by the current filters. Pick another
                        record from the list.
                      </div>
                    )}

                    {detailLoading && (
                      <div style={{ ...softCardStyle, color: "#dbe4ff" }}>Loading detail view...</div>
                    )}

                    {detailError && (
                      <div
                        style={{
                          ...softCardStyle,
                          border: "1px solid rgba(255, 120, 120, 0.25)",
                          color: "#ffe1e1",
                        }}
                      >
                        Failed to load detail: {detailError}
                      </div>
                    )}

                    {!detailLoading && !detailError && detail && selectedRecordVisible && (
                      <div style={{ display: "grid", gap: "16px" }}>
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            gap: "12px",
                            flexWrap: "wrap",
                          }}
                        >
                          <div style={{ ...badge(), fontSize: "11px" }}>{detail.item.citation_label}</div>
                          <div style={{ ...badge("green"), fontSize: "11px" }}>
                            {prettyKind(detail.item.provision_kind)}
                          </div>
                        </div>

                        <div>
                          <div
                            style={{
                              fontSize: "28px",
                              fontWeight: 800,
                              lineHeight: 1.15,
                              marginBottom: "8px",
                            }}
                          >
                            {detail.item.section_title}
                          </div>
                          <div style={{ color: "#aac0ff", fontSize: "14px", marginBottom: "10px" }}>
                            {detail.item.law_name} • Section {detail.item.section_number} • {detail.item.source_title}
                          </div>
                          <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{detail.item.summary}</div>
                        </div>

                        <div
                          style={{
                            display: "grid",
                            gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                            gap: "12px",
                          }}
                        >
                          <div style={softCardStyle}>
                            <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                              Linked sections
                            </div>
                            <div style={{ fontSize: "28px", fontWeight: 800 }}>
                              {detail.item.related_record_count}
                            </div>
                          </div>
                          <div style={softCardStyle}>
                            <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                              Same group
                            </div>
                            <div style={{ fontSize: "28px", fontWeight: 800 }}>
                              {detail.item.same_group_record_count}
                            </div>
                          </div>
                          <div style={softCardStyle}>
                            <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>
                              Same law
                            </div>
                            <div style={{ fontSize: "28px", fontWeight: 800 }}>
                              {detail.item.same_law_record_count}
                            </div>
                          </div>
                        </div>

                        <div style={softCardStyle}>
                          <div
                            style={{
                              fontSize: "13px",
                              fontWeight: 700,
                              letterSpacing: "1px",
                              textTransform: "uppercase",
                              color: "#a9c1ff",
                              marginBottom: "12px",
                            }}
                          >
                            Excerpt preview
                          </div>
                          <div
                            style={{
                              borderLeft: "3px solid rgba(126, 162, 255, 0.35)",
                              paddingLeft: "14px",
                              color: "#f0f5ff",
                              lineHeight: 1.8,
                              whiteSpace: "pre-wrap",
                            }}
                          >
                            {detail.item.excerpt}
                          </div>
                        </div>

                        <div style={{ display: "grid", gap: "12px" }}>
                          {detailListCard("Admin note", detail.item.admin_note)}
                          {detail.item.punishment_summary &&
                            detailListCard(
                              "Punishment note",
                              detail.item.punishment_summary,
                              "pink",
                            )}
                        </div>

                        <div style={softCardStyle}>
                          <div
                            style={{
                              fontSize: "13px",
                              fontWeight: 700,
                              letterSpacing: "1px",
                              textTransform: "uppercase",
                              color: "#a9c1ff",
                              marginBottom: "12px",
                            }}
                          >
                            Searchable wording
                          </div>
                          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                            {detail.item.searchable_terms.length > 0 ? (
                              detail.item.searchable_terms.map((term) => (
                                <span key={`${detail.item.id}-${term}`} style={chipStyle}>
                                  {term}
                                </span>
                              ))
                            ) : (
                              <span style={{ color: "#c6d3f3" }}>No extra searchable terms yet.</span>
                            )}
                          </div>
                        </div>

                        <div
                          style={{
                            display: "grid",
                            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                            gap: "12px",
                          }}
                        >
                          <div style={softCardStyle}>
                            <div
                              style={{
                                fontSize: "13px",
                                fontWeight: 700,
                                letterSpacing: "1px",
                                textTransform: "uppercase",
                                color: "#a9c1ff",
                                marginBottom: "10px",
                              }}
                            >
                              Aliases
                            </div>
                            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                              {detail.item.aliases.length > 0 ? (
                                detail.item.aliases.map((alias) => (
                                  <span key={`${detail.item.id}-alias-${alias}`} style={chipStyle}>
                                    {alias}
                                  </span>
                                ))
                              ) : (
                                <span style={{ color: "#c6d3f3" }}>No aliases added.</span>
                              )}
                            </div>
                          </div>

                          <div style={softCardStyle}>
                            <div
                              style={{
                                fontSize: "13px",
                                fontWeight: 700,
                                letterSpacing: "1px",
                                textTransform: "uppercase",
                                color: "#a9c1ff",
                                marginBottom: "10px",
                              }}
                            >
                              Keywords
                            </div>
                            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                              {detail.item.keywords.length > 0 ? (
                                detail.item.keywords.map((keyword) => (
                                  <span key={`${detail.item.id}-keyword-${keyword}`} style={chipStyle}>
                                    {keyword}
                                  </span>
                                ))
                              ) : (
                                <span style={{ color: "#c6d3f3" }}>No keywords added.</span>
                              )}
                            </div>
                          </div>
                        </div>

                        <div style={softCardStyle}>
                          <div
                            style={{
                              fontSize: "13px",
                              fontWeight: 700,
                              letterSpacing: "1px",
                              textTransform: "uppercase",
                              color: "#a9c1ff",
                              marginBottom: "10px",
                            }}
                          >
                            Metadata snapshot
                          </div>
                          <div style={{ display: "grid", gap: "8px", color: "#dbe4ff", lineHeight: 1.65 }}>
                            <div>
                              <strong style={{ color: "#ffffff" }}>Jurisdiction:</strong>{" "}
                              {detail.item.jurisdiction}
                            </div>
                            <div>
                              <strong style={{ color: "#ffffff" }}>Offence group:</strong>{" "}
                              {detail.item.offence_group ? prettyKind(detail.item.offence_group) : "Unassigned"}
                            </div>
                            <div>
                              <strong style={{ color: "#ffffff" }}>Related sections:</strong>{" "}
                              {detail.item.related_sections.length > 0
                                ? detail.item.related_sections.join(", ")
                                : "None linked yet"}
                            </div>
                            <div>
                              <strong style={{ color: "#ffffff" }}>Tags:</strong>{" "}
                              {detail.item.tags.length > 0 ? detail.item.tags.join(", ") : "No tags added"}
                            </div>
                          </div>
                        </div>

                        {[ 
                          {
                            title: "Companion records",
                            items: detail.companion_records,
                            empty: "No direct companion records are linked yet.",
                          },
                          {
                            title: "Same-group context",
                            items: detail.same_group_records,
                            empty: "No same-group context records are available.",
                          },
                          {
                            title: "Same-law context",
                            items: detail.same_law_records,
                            empty: "No additional same-law records are available.",
                          },
                        ].map((group) => (
                          <div key={group.title} style={softCardStyle}>
                            <div
                              style={{
                                fontSize: "13px",
                                fontWeight: 700,
                                letterSpacing: "1px",
                                textTransform: "uppercase",
                                color: "#a9c1ff",
                                marginBottom: "12px",
                              }}
                            >
                              {group.title}
                            </div>

                            {group.items.length === 0 ? (
                              <div style={{ color: "#c6d3f3" }}>{group.empty}</div>
                            ) : (
                              <div style={{ display: "grid", gap: "10px" }}>
                                {group.items.map((item) => (
                                  <button
                                    key={item.id}
                                    type="button"
                                    onClick={() => setSelectedSourceId(item.id)}
                                    style={{
                                      ...softCardStyle,
                                      padding: "14px",
                                      textAlign: "left",
                                      cursor: "pointer",
                                    }}
                                  >
                                    <div
                                      style={{
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "space-between",
                                        gap: "10px",
                                        flexWrap: "wrap",
                                        marginBottom: "8px",
                                      }}
                                    >
                                      <div style={{ ...badge(), fontSize: "11px" }}>
                                        {item.citation_label}
                                      </div>
                                      <div style={{ ...badge("green"), fontSize: "11px" }}>
                                        {item.relationship_label}
                                      </div>
                                    </div>
                                    <div style={{ fontWeight: 700, fontSize: "16px", marginBottom: "6px" }}>
                                      {item.section_title}
                                    </div>
                                    <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                                      {item.law_name} • Section {item.section_number} • {prettyKind(item.provision_kind)}
                                    </div>
                                    <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item.summary}</div>
                                  </button>
                                ))}
                              </div>
                            )}
                          </div>
                        ))}

                        <div
                          style={{
                            background:
                              "linear-gradient(180deg, rgba(20, 36, 74, 0.96), rgba(12, 21, 45, 0.96))",
                            border: "1px solid rgba(126, 162, 255, 0.18)",
                            borderRadius: "18px",
                            padding: "18px",
                          }}
                        >
                          <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>
                            Detail workflow note
                          </div>
                          <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{detail.workflow_note}</div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge(), marginBottom: "12px" }}>Phase 4 workspace shelf</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
                Saved drafts + staged publish packages
              </div>

              {workspaceLoading ? (
                <div style={softCardStyle}>Loading workspace shelf...</div>
              ) : workspaceError ? (
                <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                  Failed to load workspace shelf: {workspaceError}
                </div>
              ) : (
                <div style={{ display: "grid", gap: "18px" }}>
                  {workspaceActionError && (
                    <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                      Workspace action failed: {workspaceActionError}
                    </div>
                  )}

                  {workspace && (
                    <>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "12px" }}>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Saved drafts</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{workspace.saved_draft_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Staged packages</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{workspace.staged_publish_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Ready drafts</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{workspace.ready_draft_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Blocked items</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{workspace.blocked_item_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Session publishes</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{workspace.session_publish_count}</div>
                        </div>
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{workspace.workflow_note}</div>

                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "18px", alignItems: "start" }}>
                        <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "12px", flexWrap: "wrap" }}>
                            <div style={{ ...badge("green") }}>Saved drafts</div>
                            {workspaceBusy && <div style={{ color: "#aac0ff", fontSize: "13px" }}>Updating workspace…</div>}
                          </div>
                          {workspace.drafts.length === 0 ? (
                            <div style={{ color: "#c6d3f3", lineHeight: 1.65 }}>
                              No workspace drafts saved yet. Save the current draft to keep a reusable snapshot before real persistence exists.
                            </div>
                          ) : (
                            workspace.drafts.map((item) => (
                              <div key={item.workspace_draft_id} style={{ ...softCardStyle, padding: "14px", border: item.workspace_draft_id === workspaceDraftId ? "1px solid rgba(126, 162, 255, 0.32)" : undefined }}>
                                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap", marginBottom: "8px" }}>
                                  <div style={{ color: "#ffffff", fontWeight: 700 }}>{item.title}</div>
                                  <div style={badge(toneFromStatus(item.review_status))}>{prettyKind(item.review_status)}</div>
                                </div>
                                <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                                  {item.citation_label || `${item.law_name} • Section ${item.section_number}`} • v{item.version}
                                </div>
                                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "10px" }}>
                                  <span style={chipStyle}>Score {item.readiness_score}</span>
                                  <span style={chipStyle}>{item.changed_field_count} changed</span>
                                  <span style={chipStyle}>{item.warning_count} warnings</span>
                                  <span style={chipStyle}>{item.blocker_count} blockers</span>
                                </div>
                                <div style={{ color: "#c6d3f3", fontSize: "13px", marginBottom: "10px" }}>Saved {item.saved_at}</div>
                                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                                  <button type="button" onClick={() => loadWorkspaceDraft(item.workspace_draft_id)} style={secondaryButton}>
                                    Load draft
                                  </button>
                                  <button type="button" onClick={() => deleteWorkspaceDraft(item.workspace_draft_id)} style={secondaryButton}>
                                    Delete
                                  </button>
                                </div>
                              </div>
                            ))
                          )}
                        </div>

                        <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                          <div style={{ ...badge() }}>Staged publish packages</div>
                          {workspace.publish_queue.length === 0 ? (
                            <div style={{ color: "#c6d3f3", lineHeight: 1.65 }}>
                              No publish packages are staged yet. Save or review a draft, then stage a publish package to create a handoff artifact for later real approval workflows.
                            </div>
                          ) : (
                            workspace.publish_queue.map((item) => (
                              <div key={item.package_id} style={{ ...softCardStyle, padding: "14px" }}>
                                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap", marginBottom: "8px" }}>
                                  <div style={{ color: "#ffffff", fontWeight: 700 }}>{item.title}</div>
                                  <div style={badge(toneFromStatus(item.publish_status))}>{prettyKind(item.publish_status)}</div>
                                </div>
                                <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                                  {item.citation_label || "Draft package"} • {prettyKind(item.publish_mode)}
                                </div>
                                <div style={{ color: "#dbe4ff", lineHeight: 1.65, marginBottom: "10px" }}>{item.summary_line}</div>
                                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "10px" }}>
                                  <span style={chipStyle}>{item.changed_field_count} changed</span>
                                  <span style={chipStyle}>{item.warning_count} warnings</span>
                                  <span style={chipStyle}>{item.blocker_count} blockers</span>
                                </div>
                                <div style={{ color: "#c6d3f3", fontSize: "13px", marginBottom: "10px" }}>Staged {item.staged_at}</div>
                                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                                  <button
                                    type="button"
                                    onClick={() => publishStagedPackage(item.package_id)}
                                    style={secondaryButton}
                                    disabled={workspaceBusy || item.publish_status === "blocked"}
                                  >
                                    {workspaceBusy ? "Working..." : "Publish to live catalog"}
                                  </button>
                                  <button type="button" onClick={() => deletePublishPackage(item.package_id)} style={secondaryButton}>
                                    Remove package
                                  </button>
                                </div>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge("green"), marginBottom: "12px" }}>Phase 5 data operations</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
                Retrieval metadata and embedding controls
              </div>

              <div style={{ color: "#dbe4ff", lineHeight: 1.7, marginBottom: "18px", maxWidth: "980px" }}>
                Use these controls to refresh persisted retrieval metadata and generate embeddings directly from the admin dashboard, without leaving the UI.
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "18px" }}>
                <div style={{ ...softCardStyle, padding: "18px" }}>
                  <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "12px" }}>Retrieval readiness</div>

                  {retrievalReadinessLoading ? (
                    <div style={{ color: "#dbe4ff" }}>Loading retrieval readiness...</div>
                  ) : retrievalReadinessError ? (
                    <div style={{ color: "#ffe1e1" }}>{retrievalReadinessError}</div>
                  ) : retrievalReadiness ? (
                    <div style={{ display: "grid", gap: "12px" }}>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: "10px" }}>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Persisted records</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{retrievalReadiness.persisted_record_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Refresh needed</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{retrievalReadiness.refresh_needed_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Missing fingerprints</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{retrievalReadiness.missing_fingerprint_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Vector candidates</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{retrievalReadiness.vector_candidate_count}</div>
                        </div>
                      </div>

                      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                        <button type="button" onClick={() => loadRetrievalReadiness()} style={secondaryButton} disabled={retrievalReadinessLoading}>
                          Reload readiness
                        </button>
                        <button type="button" onClick={() => runRetrievalRefresh(false)} style={secondaryButton} disabled={retrievalRefreshLoading}>
                          {retrievalRefreshLoading ? "Refreshing..." : "Refresh changed records"}
                        </button>
                        <button type="button" onClick={() => runRetrievalRefresh(true)} style={secondaryButton} disabled={retrievalRefreshLoading}>
                          Force full refresh
                        </button>
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{retrievalReadiness.workflow_note}</div>
                      {retrievalRefreshNote && <div style={{ color: "#b8f7d4" }}>{retrievalRefreshNote}</div>}

                      <div style={{ display: "grid", gap: "10px" }}>
                        {retrievalReadiness.sample_records.map((item) => (
                          <div key={item.record_id} style={{ ...softCardStyle, padding: "14px" }}>
                            <div style={{ fontWeight: 700, marginBottom: "6px" }}>
                              {item.citation_label} · {item.law_name} {item.section_number}
                            </div>
                            <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                              Fingerprint: {item.fingerprint_status} · Retrieval doc: {item.has_retrieval_document ? "Yes" : "No"}
                            </div>
                            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                              <div style={badge(item.refresh_needed ? "green" : "blue")}>
                                {item.refresh_needed ? "Refresh needed" : "Up to date"}
                              </div>
                              <div style={badge(item.has_retrieval_fingerprint ? "green" : "blue")}>
                                {item.has_retrieval_fingerprint ? "Fingerprint ready" : "Fingerprint missing"}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>

                <div style={{ ...softCardStyle, padding: "18px" }}>
                  <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "12px" }}>Embedding readiness</div>

                  {embeddingReadinessLoading ? (
                    <div style={{ color: "#dbe4ff" }}>Loading embedding readiness...</div>
                  ) : embeddingReadinessError ? (
                    <div style={{ color: "#ffe1e1" }}>{embeddingReadinessError}</div>
                  ) : embeddingReadiness ? (
                    <div style={{ display: "grid", gap: "12px" }}>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: "10px" }}>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Ready vectors</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{embeddingReadiness.ready_vector_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Runnable</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{embeddingReadiness.runnable_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Vector rows</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{embeddingReadiness.vector_row_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Errors</div>
                          <div style={{ fontSize: "24px", fontWeight: 800 }}>{embeddingReadiness.error_count}</div>
                        </div>
                      </div>

                      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
                        <input
                          type="number"
                          min="1"
                          value={embeddingRunLimit}
                          onChange={(event) => setEmbeddingRunLimit(event.target.value)}
                          style={{ ...fieldStyle, width: "110px" }}
                        />
                        <button type="button" onClick={() => loadEmbeddingReadiness()} style={secondaryButton} disabled={embeddingReadinessLoading}>
                          Reload readiness
                        </button>
                        <button type="button" onClick={() => runEmbeddingGeneration()} style={secondaryButton} disabled={embeddingRunLoading}>
                          {embeddingRunLoading ? "Running..." : "Run embedding batch"}
                        </button>
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{embeddingReadiness.workflow_note}</div>
                      {embeddingRunNote && <div style={{ color: "#b8f7d4" }}>{embeddingRunNote}</div>}

                      <div style={{ display: "grid", gap: "10px" }}>
                        {embeddingReadiness.sample_records.map((item) => (
                          <div key={item.record_id} style={{ ...softCardStyle, padding: "14px" }}>
                            <div style={{ fontWeight: 700, marginBottom: "6px" }}>
                              {item.citation_label} · {item.law_name} {item.section_number}
                            </div>
                            <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                              Model: {item.model_name ?? "—"} · Dimensions: {item.dimensions ?? "—"}
                            </div>
                            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                              <div style={badge(item.has_vector ? "green" : "blue")}>
                                {item.has_vector ? "Vector stored" : "Vector missing"}
                              </div>
                              <div style={badge(item.fingerprint_match ? "green" : "blue")}>
                                {item.fingerprint_match ? "Fingerprint match" : "Fingerprint mismatch"}
                              </div>
                              {item.last_error && <div style={badge("pink")}>Has error</div>}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge("green"), marginBottom: "12px" }}>Phase 5 retrieval probe</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
                Hybrid retrieval inspection
              </div>

              <div style={{ color: "#dbe4ff", lineHeight: 1.7, marginBottom: "16px", maxWidth: "980px" }}>
                Test any legal query from admin and inspect how keyword scoring and vector similarity combine before the final records are selected for chat context.
              </div>

              <div style={{ display: "grid", gap: "14px", marginBottom: "18px" }}>
                <div>
                  <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Probe query</div>
                  <textarea
                    value={probeQuery}
                    onChange={(event) => setProbeQuery(event.target.value)}
                    rows={3}
                    style={{ ...fieldStyle, resize: "vertical", minHeight: "96px" }}
                    placeholder="Ask a legal retrieval question to inspect ranking."
                  />
                </div>

                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  <button type="button" onClick={() => runRetrievalProbe()} style={secondaryButton} disabled={probeLoading}>
                    {probeLoading ? "Running probe..." : "Run retrieval probe"}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      const sample = "Can police arrest someone without warrant for online blackmail?";
                      setProbeQuery(sample);
                      runRetrievalProbe(sample);
                    }}
                    style={secondaryButton}
                    disabled={probeLoading}
                  >
                    Load sample query
                  </button>
                </div>

                {probeError && (
                  <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                    Failed to run probe: {probeError}
                  </div>
                )}
              </div>

              {probeResult && (
                <div style={{ display: "grid", gap: "18px" }}>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px" }}>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Active source</div>
                      <div style={{ fontSize: "16px", fontWeight: 700 }}>{probeResult.source_label}</div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Vector retrieval</div>
                      <div style={{ fontSize: "16px", fontWeight: 700 }}>
                        {probeResult.vector_retrieval_active ? "Active" : "Fallback only"}
                      </div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Keyword candidates</div>
                      <div style={{ fontSize: "28px", fontWeight: 800 }}>{probeResult.keyword_candidate_count}</div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Vector candidates</div>
                      <div style={{ fontSize: "28px", fontWeight: 800 }}>{probeResult.vector_candidate_count}</div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Selected for chat</div>
                      <div style={{ fontSize: "28px", fontWeight: 800 }}>{probeResult.selected_count}</div>
                    </div>
                  </div>

                  <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{probeResult.workflow_note}</div>

                  <div style={{ display: "grid", gap: "12px" }}>
                    {probeResult.records.length === 0 ? (
                      <div style={softCardStyle}>No retrieval candidates were returned for this query.</div>
                    ) : (
                      probeResult.records.map((item) => (
                        <div key={item.record_id} style={{ ...softCardStyle, padding: "16px" }}>
                          <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", flexWrap: "wrap", marginBottom: "10px" }}>
                            <div>
                              <div style={{ fontWeight: 700, color: "#ffffff", marginBottom: "6px" }}>
                                {item.citation_label} · {item.law_name} {item.section_number}
                              </div>
                              <div style={{ color: "#aac0ff", fontSize: "13px" }}>
                                {prettyKind(item.category)}
                              </div>
                            </div>
                            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                              <div style={badge(item.selected ? "green" : "blue")}>
                                {item.selected ? "Selected" : "Candidate"}
                              </div>
                              {item.exact_section_match && <div style={badge("green")}>Exact section match</div>}
                            </div>
                          </div>

                          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "10px", marginBottom: "12px" }}>
                            <div style={softCardStyle}>
                              <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Keyword score</div>
                              <div style={{ fontSize: "22px", fontWeight: 800 }}>{item.keyword_score}</div>
                            </div>
                            <div style={softCardStyle}>
                              <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Vector bonus</div>
                              <div style={{ fontSize: "22px", fontWeight: 800 }}>{item.vector_bonus}</div>
                            </div>
                            <div style={softCardStyle}>
                              <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Final score</div>
                              <div style={{ fontSize: "22px", fontWeight: 800 }}>{item.final_score}</div>
                            </div>
                            <div style={softCardStyle}>
                              <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "6px" }}>Vector similarity</div>
                              <div style={{ fontSize: "22px", fontWeight: 800 }}>
                                {item.vector_similarity === null ? "—" : item.vector_similarity.toFixed(3)}
                              </div>
                            </div>
                          </div>

                          <div style={{ color: "#dbe4ff", lineHeight: 1.7, whiteSpace: "pre-wrap" }}>
                            {item.excerpt}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge(), marginBottom: "12px" }}>Phase 4 activity feed</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
                Session publish activity
              </div>

              {activityLoading ? (
                <div style={softCardStyle}>Loading admin activity...</div>
              ) : activityError ? (
                <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                  Failed to load admin activity: {activityError}
                </div>
              ) : activity ? (
                <div style={{ display: "grid", gap: "18px" }}>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px" }}>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Session events</div>
                      <div style={{ fontSize: "28px", fontWeight: 800 }}>{activity.total_events}</div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Publish events</div>
                      <div style={{ fontSize: "28px", fontWeight: 800 }}>{activity.publish_event_count}</div>
                    </div>
                    <div style={softCardStyle}>
                      <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Latest publish</div>
                      <div style={{ fontSize: "15px", fontWeight: 700, lineHeight: 1.5 }}>{activity.latest_publish_label || "No publish yet"}</div>
                    </div>
                  </div>

                  <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{activity.workflow_note}</div>

                  <div style={{ display: "grid", gap: "12px" }}>
                    {activity.items.length === 0 ? (
                      <div style={softCardStyle}>No session activity yet. Publish a staged package to create the first live-catalog event.</div>
                    ) : (
                      activity.items.map((item) => (
                        <div key={item.activity_id} style={{ ...softCardStyle, padding: "14px" }}>
                          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap", marginBottom: "8px" }}>
                            <div style={{ color: "#ffffff", fontWeight: 700 }}>{item.title}</div>
                            <div style={badge(toneFromStatus(item.status))}>{prettyKind(item.status)}</div>
                          </div>
                          <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "8px" }}>
                            {item.kind.replaceAll("_", " ")}
                            {item.citation_label ? ` • ${item.citation_label}` : ""}
                          </div>
                          <div style={{ color: "#dbe4ff", lineHeight: 1.65, marginBottom: "8px" }}>{item.detail}</div>
                          <div style={{ color: "#c6d3f3", fontSize: "13px" }}>{item.created_at}</div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              ) : null}
            </section>

            <section style={{ ...cardStyle, padding: "24px", marginBottom: "24px" }}>
              <div style={{ ...badge("green"), marginBottom: "12px" }}>Phase 4 draft workflow</div>
              <div style={{ fontSize: "26px", fontWeight: 700, marginBottom: "16px" }}>
Working draft editor + review gate + publish preview
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
                  gap: "18px",
                  alignItems: "start",
                }}
              >
                <div style={{ ...softCardStyle, display: "grid", gap: "14px" }}>
                  <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>
                    Edit a working draft safely, validate it, run a review gate, build a publish preview, and save reusable workspace snapshots. Once a staged package is ready, you can now publish it into the live in-memory catalog for the current session.
                  </div>

                  {workspaceDraftId && <div style={{ ...badge("green"), width: "fit-content" }}>Active workspace draft</div>}

                  <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                    <button type="button" onClick={validateDraft} style={secondaryButton} disabled={!draftForm || draftLoading}>
                      {draftLoading ? "Validating..." : "Validate draft"}
                    </button>
                    <button type="button" onClick={runDraftReview} style={secondaryButton} disabled={!draftForm || reviewLoading}>
                      {reviewLoading ? "Reviewing..." : "Run review gate"}
                    </button>
                    <button type="button" onClick={buildPublishPreview} style={secondaryButton} disabled={!draftForm || publishLoading}>
                      {publishLoading ? "Building..." : "Build publish preview"}
                    </button>
                    <button type="button" onClick={submitPersistedUpdate} style={secondaryButton} disabled={!draftForm || !selectedSourceId || persistUpdateLoading}>
                      {persistUpdateLoading ? "Saving..." : "Save persisted edit"}
                    </button>
                    <button type="button" onClick={submitDeleteSource} style={secondaryButton} disabled={!selectedSourceId || deleteLoading}>
                      {deleteLoading ? "Deleting..." : "Delete source"}
                    </button>
                    <button type="button" onClick={runSelectedEmbeddingGeneration} style={secondaryButton} disabled={!selectedSourceId || selectedEmbeddingRunLoading}>
                      {selectedEmbeddingRunLoading ? "Running..." : "Run selected embedding"}
                    </button>
                    <button type="button" onClick={copyDraftToCreateForm} style={secondaryButton} disabled={!draftForm}>
                      Copy to create form
                    </button>
                    <button type="button" onClick={saveDraftToWorkspace} style={secondaryButton} disabled={!draftForm || workspaceBusy}>
                      {workspaceBusy ? "Working..." : workspaceDraftId ? "Update workspace draft" : "Save to workspace"}
                    </button>
                    <button type="button" onClick={stagePublishPackage} style={secondaryButton} disabled={!draftForm || workspaceBusy}>
                      {workspaceBusy ? "Working..." : "Stage publish package"}
                    </button>
                    <button type="button" onClick={resetDraftFromSelected} style={secondaryButton} disabled={!detail}>
                      Reset from selected
                    </button>
                    <button type="button" onClick={startBlankDraft} style={secondaryButton}>
                      Start blank draft
                    </button>
                  </div>

                  {!draftForm ? (
                    <div style={softCardStyle}>Select a record to load an editable draft, or start with a blank draft.</div>
                  ) : (
                    <>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px" }}>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Source title</div>
                          <input value={draftForm.source_title} onChange={(event) => updateDraftField("source_title", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Law name</div>
                          <input value={draftForm.law_name} onChange={(event) => updateDraftField("law_name", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Section number</div>
                          <input value={draftForm.section_number} onChange={(event) => updateDraftField("section_number", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Provision kind</div>
                          <select value={draftForm.provision_kind} onChange={(event) => updateDraftField("provision_kind", event.target.value)} style={fieldStyle}>
                            {catalog.available_kinds.map((kind) => (
                              <option key={kind} value={kind}>{prettyKind(kind)}</option>
                            ))}
                            {!catalog.available_kinds.includes("general") && <option value="general">General</option>}
                          </select>
                        </div>
                      </div>

                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px" }}>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Section title</div>
                          <input value={draftForm.section_title} onChange={(event) => updateDraftField("section_title", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Citation label</div>
                          <input value={draftForm.citation_label} onChange={(event) => updateDraftField("citation_label", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Jurisdiction</div>
                          <input value={draftForm.jurisdiction} onChange={(event) => updateDraftField("jurisdiction", event.target.value)} style={fieldStyle} />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Offence group</div>
                          <input value={draftForm.offence_group} onChange={(event) => updateDraftField("offence_group", event.target.value)} style={fieldStyle} placeholder="e.g. theft" />
                        </div>
                      </div>

                      <div>
                        <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Summary</div>
                        <textarea value={draftForm.summary} onChange={(event) => updateDraftField("summary", event.target.value)} style={{ ...fieldStyle, minHeight: "110px", resize: "vertical" }} />
                      </div>

                      <div>
                        <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Excerpt</div>
                        <textarea value={draftForm.excerpt} onChange={(event) => updateDraftField("excerpt", event.target.value)} style={{ ...fieldStyle, minHeight: "140px", resize: "vertical" }} />
                      </div>

                      <div>
                        <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Punishment summary</div>
                        <input value={draftForm.punishment_summary} onChange={(event) => updateDraftField("punishment_summary", event.target.value)} style={fieldStyle} placeholder="Optional unless this is a punishment record" />
                      </div>

                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px" }}>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Tags</div>
                          <input value={draftForm.tags_text} onChange={(event) => updateDraftField("tags_text", event.target.value)} style={fieldStyle} placeholder="comma, separated, tags" />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Aliases</div>
                          <input value={draftForm.aliases_text} onChange={(event) => updateDraftField("aliases_text", event.target.value)} style={fieldStyle} placeholder="plain-language aliases" />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Keywords</div>
                          <input value={draftForm.keywords_text} onChange={(event) => updateDraftField("keywords_text", event.target.value)} style={fieldStyle} placeholder="search keywords" />
                        </div>
                        <div>
                          <div style={{ color: "#a9c1ff", fontSize: "13px", marginBottom: "8px" }}>Related sections</div>
                          <input value={draftForm.related_sections_text} onChange={(event) => updateDraftField("related_sections_text", event.target.value)} style={fieldStyle} placeholder="379, 380, 381" />
                        </div>
                      </div>
                    </>
                  )}
                </div>

                <div style={{ ...softCardStyle, display: "grid", gap: "14px", position: "sticky", top: "20px" }}>
                  <div style={{ ...badge("pink") }}>Validation preview</div>
                  <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>
                    This prototype check flags missing fields, weak retrieval metadata, and broken section linkages before later save/review workflows exist.
                  </div>

                  {draftError && (
                    <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                      Failed to validate draft: {draftError}
                    </div>
                  )}

                  {persistUpdateError && (
                    <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                      Failed to save persisted update: {persistUpdateError}
                    </div>
                  )}

                  {persistUpdateResult && (
                    <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                        <div style={badge(persistUpdateResult.update_status === "updated" ? "green" : "pink")}>
                          {prettyKind(persistUpdateResult.update_status)}
                        </div>
                        <div style={badge(persistUpdateResult.save_mode === "database" ? "green" : "blue")}>
                          Save mode: {prettyKind(persistUpdateResult.save_mode)}
                        </div>
                        <div style={badge(persistUpdateResult.retrieval_changed ? "green" : "blue")}>
                          {persistUpdateResult.retrieval_changed ? "Retrieval changed" : "Retrieval unchanged"}
                        </div>
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>
                        {persistUpdateResult.workflow_note}
                      </div>

                      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                        <div style={chipStyle}>Readiness {persistUpdateResult.validation.readiness_score}</div>
                        <div style={chipStyle}>Issues {persistUpdateResult.validation.issue_count}</div>
                        <div style={chipStyle}>Errors {persistUpdateResult.validation.error_count}</div>
                        <div style={chipStyle}>Warnings {persistUpdateResult.validation.warning_count}</div>
                      </div>
                    </div>
                  )}

                  {deleteError && (
                    <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                      Failed to delete source record: {deleteError}
                    </div>
                  )}

                  {deleteResult && (
                    <div style={{ ...softCardStyle, display: "grid", gap: "12px" }}>
                      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                        <div style={badge(deleteResult.delete_status === "deleted" ? "green" : "pink")}>
                          {prettyKind(deleteResult.delete_status)}
                        </div>
                        <div style={badge(deleteResult.save_mode === "database" ? "green" : "blue")}>
                          Save mode: {prettyKind(deleteResult.save_mode)}
                        </div>
                        {deleteResult.record_id && <div style={badge()}>Record id: {deleteResult.record_id}</div>}
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>
                        {deleteResult.workflow_note}
                      </div>

                      {deleteResult.deleted_title && (
                        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                          <div style={chipStyle}>Deleted title</div>
                          <div style={chipStyle}>{deleteResult.deleted_title}</div>
                        </div>
                      )}
                    </div>
                  )}

                  {selectedEmbeddingRunError && (
                    <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                      Failed to run selected embedding refresh: {selectedEmbeddingRunError}
                    </div>
                  )}

                  {selectedEmbeddingRunNote && (
                    <div style={{ ...softCardStyle, color: "#dbe4ff", lineHeight: 1.7 }}>{selectedEmbeddingRunNote}</div>
                  )}

                  {!draftValidation ? (
                    <div style={softCardStyle}>Run validation to see readiness, issue list, section-link checks, and a normalized preview.</div>
                  ) : (
                    <>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "12px" }}>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Readiness</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftValidation.readiness_score}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Errors</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftValidation.error_count}</div>
                        </div>
                        <div style={softCardStyle}>
                          <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Warnings</div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftValidation.warning_count}</div>
                        </div>
                      </div>

                      <div style={softCardStyle}>
                        <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                          Normalized preview
                        </div>
                        <div style={{ display: "grid", gap: "8px", color: "#dbe4ff", lineHeight: 1.65 }}>
                          <div><strong style={{ color: "#ffffff" }}>Citation:</strong> {draftValidation.preview.citation_label}</div>
                          <div><strong style={{ color: "#ffffff" }}>Law / section:</strong> {draftValidation.preview.law_name} • Section {draftValidation.preview.section_number}</div>
                          <div><strong style={{ color: "#ffffff" }}>Title:</strong> {draftValidation.preview.section_title}</div>
                          <div><strong style={{ color: "#ffffff" }}>Kind:</strong> {prettyKind(draftValidation.preview.provision_kind)}</div>
                          <div><strong style={{ color: "#ffffff" }}>Admin note:</strong> {draftValidation.preview.admin_note}</div>
                        </div>
                      </div>

                      <div style={softCardStyle}>
                        <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                          Draft issues
                        </div>
                        {draftValidation.issues.length === 0 ? (
                          <div style={{ color: "#bdf3d8" }}>No draft issues found. This draft looks structurally strong for the current prototype rules.</div>
                        ) : (
                          <div style={{ display: "grid", gap: "10px" }}>
                            {draftValidation.issues.map((issue, index) => (
                              <div key={`${issue.field}-${index}`} style={{ ...softCardStyle, padding: "14px", border: issue.level === "error" ? "1px solid rgba(255, 120, 120, 0.22)" : "1px solid rgba(255, 196, 102, 0.20)" }}>
                                <div style={{ display: "flex", gap: "10px", alignItems: "center", flexWrap: "wrap", marginBottom: "6px" }}>
                                  <div style={issue.level === "error" ? badge("pink") : badge("green")}>{issue.level.toUpperCase()}</div>
                                  <div style={{ color: "#dfe7ff", fontWeight: 700 }}>{issue.field}</div>
                                </div>
                                <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{issue.message}</div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      <div style={softCardStyle}>
                        <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                          Related section check
                        </div>
                        <div style={{ display: "grid", gap: "10px" }}>
                          <div style={{ color: "#dbe4ff" }}>
                            <strong style={{ color: "#ffffff" }}>Existing:</strong>{" "}
                            {draftValidation.related_section_check.existing.length > 0 ? draftValidation.related_section_check.existing.join(", ") : "None confirmed"}
                          </div>
                          <div style={{ color: "#dbe4ff" }}>
                            <strong style={{ color: "#ffffff" }}>Missing:</strong>{" "}
                            {draftValidation.related_section_check.missing.length > 0 ? draftValidation.related_section_check.missing.join(", ") : "No missing links"}
                          </div>
                        </div>
                      </div>

                      <div style={softCardStyle}>
                        <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                          Searchable terms preview
                        </div>
                        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                          {draftValidation.preview.searchable_terms.length > 0 ? draftValidation.preview.searchable_terms.map((term) => (
                            <span key={term} style={chipStyle}>{term}</span>
                          )) : <span style={{ color: "#c6d3f3" }}>No searchable terms available yet.</span>}
                        </div>
                      </div>



                      {reviewError && (
                        <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                          Failed to run review gate: {reviewError}
                        </div>
                      )}

                      {!draftReview ? (
                        <div style={softCardStyle}>Run the review gate to see blockers, warnings, and changed-field scope before publish preview.</div>
                      ) : (
                        <>
                          <div style={softCardStyle}>
                            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap", marginBottom: "12px" }}>
                              <div style={{ ...badge(toneFromStatus(draftReview.review_status)) }}>{prettyKind(draftReview.review_status)}</div>
                              <div style={{ color: "#dfe7ff", fontWeight: 700 }}>{draftReview.approval_label}</div>
                            </div>
                            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: "12px" }}>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Review score</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftReview.readiness_score}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Blockers</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftReview.blocker_count}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Warnings</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftReview.warning_count}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Changed fields</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{draftReview.changed_field_count}</div>
                              </div>
                            </div>
                          </div>

                          <div style={softCardStyle}>
                            <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                              Review checklist
                            </div>
                            <div style={{ display: "grid", gap: "10px" }}>
                              {draftReview.checklist.map((item) => (
                                <div key={item.key} style={{ ...softCardStyle, padding: "14px" }}>
                                  <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap", marginBottom: "6px" }}>
                                    <div style={badge(toneFromStatus(item.status))}>{prettyKind(item.status)}</div>
                                    <div style={{ color: "#ffffff", fontWeight: 700 }}>{item.title}</div>
                                  </div>
                                  <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item.detail}</div>
                                </div>
                              ))}
                            </div>
                          </div>

                          <div style={softCardStyle}>
                            <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                              Changed fields
                            </div>
                            {draftReview.changed_fields.length === 0 ? (
                              <div style={{ color: "#c6d3f3" }}>No changed fields detected yet.</div>
                            ) : (
                              <div style={{ display: "grid", gap: "10px" }}>
                                {draftReview.changed_fields.map((item) => (
                                  <div key={item.field} style={{ ...softCardStyle, padding: "14px" }}>
                                    <div style={{ color: "#ffffff", fontWeight: 700, marginBottom: "8px" }}>{item.label}</div>
                                    <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "6px" }}>Before</div>
                                    <div style={{ color: "#dbe4ff", lineHeight: 1.6, marginBottom: "10px" }}>{item.before || "—"}</div>
                                    <div style={{ color: "#aac0ff", fontSize: "13px", marginBottom: "6px" }}>After</div>
                                    <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item.after || "—"}</div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </>
                      )}

                      {publishError && (
                        <div style={{ ...softCardStyle, border: "1px solid rgba(255, 120, 120, 0.25)", color: "#ffe1e1" }}>
                          Failed to build publish preview: {publishError}
                        </div>
                      )}

                      {!publishPreview ? (
                        <div style={softCardStyle}>Build the publish preview to inspect context impact and remaining blockers before a future real save workflow exists.</div>
                      ) : (
                        <>
                          <div style={softCardStyle}>
                            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap", marginBottom: "12px" }}>
                              <div style={{ ...badge(toneFromStatus(publishPreview.publish_status)) }}>{prettyKind(publishPreview.publish_status)}</div>
                              <div style={{ color: "#dfe7ff", fontWeight: 700 }}>{prettyKind(publishPreview.publish_mode)}</div>
                            </div>
                            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: "12px" }}>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Search terms</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{publishPreview.searchable_term_count}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Linked sections</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{publishPreview.linked_section_count}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Same-law context</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{publishPreview.same_law_context_count}</div>
                              </div>
                              <div style={softCardStyle}>
                                <div style={{ color: "#9db8ff", fontSize: "12px", marginBottom: "8px" }}>Companion hits</div>
                                <div style={{ fontSize: "28px", fontWeight: 800 }}>{publishPreview.companion_hit_count}</div>
                              </div>
                            </div>
                            <div style={{ color: "#dbe4ff", lineHeight: 1.7, marginTop: "14px" }}>
                              <strong style={{ color: "#ffffff" }}>Target record:</strong>{" "}
                              {publishPreview.target_record_id || "New draft record"}
                            </div>
                          </div>

                          <div style={softCardStyle}>
                            <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                              Publish blockers and warnings
                            </div>
                            <div style={{ display: "grid", gap: "10px" }}>
                              {publishPreview.blockers.length === 0 && publishPreview.warnings.length === 0 ? (
                                <div style={{ color: "#bdf3d8" }}>No publish blockers or warnings surfaced by the current prototype checks.</div>
                              ) : (
                                <>
                                  {publishPreview.blockers.map((item, index) => (
                                    <div key={`blocker-${index}`} style={{ ...softCardStyle, padding: "14px", border: "1px solid rgba(255, 120, 120, 0.22)" }}>
                                      <div style={{ ...badge("pink"), marginBottom: "8px" }}>BLOCKER</div>
                                      <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item}</div>
                                    </div>
                                  ))}
                                  {publishPreview.warnings.map((item, index) => (
                                    <div key={`warning-${index}`} style={{ ...softCardStyle, padding: "14px", border: "1px solid rgba(255, 196, 102, 0.20)" }}>
                                      <div style={{ ...badge("blue"), marginBottom: "8px" }}>WARNING</div>
                                      <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item}</div>
                                    </div>
                                  ))}
                                </>
                              )}
                            </div>
                          </div>

                          <div style={softCardStyle}>
                            <div style={{ fontSize: "13px", fontWeight: 700, letterSpacing: "1px", textTransform: "uppercase", color: "#a9c1ff", marginBottom: "12px" }}>
                              Recommended actions
                            </div>
                            <div style={{ display: "grid", gap: "8px" }}>
                              {publishPreview.recommended_actions.map((item, index) => (
                                <div key={`${item}-${index}`} style={{ color: "#dbe4ff", lineHeight: 1.6 }}>• {item}</div>
                              ))}
                            </div>
                          </div>

                          <div style={{ background: "linear-gradient(180deg, rgba(20, 36, 74, 0.96), rgba(12, 21, 45, 0.96))", border: "1px solid rgba(126, 162, 255, 0.18)", borderRadius: "18px", padding: "18px" }}>
                            <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>Publish preview note</div>
                            <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{publishPreview.workflow_note}</div>
                          </div>
                        </>
                      )}

                      <div style={{ background: "linear-gradient(180deg, rgba(20, 36, 74, 0.96), rgba(12, 21, 45, 0.96))", border: "1px solid rgba(126, 162, 255, 0.18)", borderRadius: "18px", padding: "18px" }}>
                        <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>Draft workflow note</div>
                        <div style={{ color: "#dbe4ff", lineHeight: 1.7 }}>{draftValidation.workflow_note}</div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </section>

            <section style={{ ...cardStyle, padding: "24px" }}>
              <div style={{ ...badge("pink"), marginBottom: "12px" }}>Still planned</div>
              <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "18px" }}>
                Next internal capabilities
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                  gap: "18px",
                }}
              >
                {summary.roadmap_items.map((item) => (
                  <div key={item.title} style={softCardStyle}>
                    <div
                      style={{
                        fontSize: "18px",
                        fontWeight: 700,
                        marginBottom: "10px",
                        color: "#ffffff",
                      }}
                    >
                      {item.title}
                    </div>
                    <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>{item.text}</div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
