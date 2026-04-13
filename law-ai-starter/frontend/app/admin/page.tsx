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

type AdminSummaryResponse = {
  stats: AdminStat[];
  control_areas: AdminRoadmapItem[];
  status_cards: AdminStatusCard[];
  workflow_steps: string[];
  roadmap_items: AdminRoadmapItem[];
  admin_boundary: string;
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

  useEffect(() => {
    const controller = new AbortController();

    async function loadAdminWorkspace() {
      try {
        setLoading(true);
        setError("");

        const [summaryResponse, sourcesResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/api/v1/admin/summary`, {
            method: "GET",
            signal: controller.signal,
            cache: "no-store",
          }),
          fetch(`${API_BASE_URL}/api/v1/admin/sources`, {
            method: "GET",
            signal: controller.signal,
            cache: "no-store",
          }),
        ]);

        if (!summaryResponse.ok) {
          throw new Error(`Summary request failed with status ${summaryResponse.status}`);
        }

        if (!sourcesResponse.ok) {
          throw new Error(`Source catalog request failed with status ${sourcesResponse.status}`);
        }

        const [summaryResult, catalogResult]: [
          AdminSummaryResponse,
          AdminSourceCatalogResponse,
        ] = await Promise.all([summaryResponse.json(), sourcesResponse.json()]);

        setSummary(summaryResult);
        setCatalog(catalogResult);
        if (catalogResult.items.length > 0) {
          setSelectedSourceId((current) => current || catalogResult.items[0].id);
        }
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err.message || "Failed to load admin workspace.");
        }
      } finally {
        setLoading(false);
      }
    }

    loadAdminWorkspace();

    return () => controller.abort();
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

  useEffect(() => {
    if (!selectedSourceId) {
      return;
    }

    const controller = new AbortController();

    async function loadDetail() {
      try {
        setDetailLoading(true);
        setDetailError("");

        const response = await fetch(`${API_BASE_URL}/api/v1/admin/sources/${selectedSourceId}`, {
          method: "GET",
          signal: controller.signal,
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`Detail request failed with status ${response.status}`);
        }

        const result: AdminSourceDetailResponse = await response.json();
        setDetail(result);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setDetailError(err.message || "Failed to load source detail.");
        }
      } finally {
        setDetailLoading(false);
      }
    }

    loadDetail();

    return () => controller.abort();
  }, [selectedSourceId]);

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
              The admin workspace now supports a real source-detail flow. You can filter the live
              prototype catalog, select one record, and inspect excerpt quality, searchable terms,
              and linked sections before later add, edit, and review workflows are introduced.
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
