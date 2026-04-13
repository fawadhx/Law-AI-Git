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
  maxWidth: "1320px",
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

function prettyKind(value: string) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function AdminPage() {
  const [summary, setSummary] = useState<AdminSummaryResponse | null>(null);
  const [catalog, setCatalog] = useState<AdminSourceCatalogResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [selectedLaw, setSelectedLaw] = useState("all");
  const [selectedKind, setSelectedKind] = useState("all");
  const [selectedGroup, setSelectedGroup] = useState("all");

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

  const filteredPunishmentCount = filteredItems.filter(
    (item) => item.provision_kind === "punishment",
  ).length;

  const filteredProcedureCount = filteredItems.filter(
    (item) => item.provision_kind === "procedure",
  ).length;

  const filteredLawCount = new Set(filteredItems.map((item) => item.law_name)).size;

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
                maxWidth: "880px",
                color: "#c8d6f7",
                fontSize: "18px",
                lineHeight: 1.65,
              }}
            >
              This workspace now reads the live prototype legal source catalog. It is still
              read-only, but it gives you a real source-management foundation before adding
              create, edit, review, and publish workflows.
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
                      <div
                        key={item}
                        style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}
                      >
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
              <div style={{ ...badge(), marginBottom: "12px" }}>Phase 4 foundation</div>
              <div
                style={{
                  fontSize: "26px",
                  fontWeight: 700,
                  marginBottom: "16px",
                }}
              >
                Source catalog workspace
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
              </div>

              {filteredItems.length === 0 ? (
                <div style={softCardStyle}>
                  No source records matched the current filters. Try clearing one or more filters.
                </div>
              ) : (
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: "16px",
                  }}
                >
                  {filteredItems.map((item) => (
                    <article key={item.id} style={softCardStyle}>
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

                      <div style={{ fontSize: "20px", fontWeight: 700, marginBottom: "8px" }}>
                        {item.section_title}
                      </div>

                      <div
                        style={{
                          color: "#aac0ff",
                          fontSize: "13px",
                          marginBottom: "10px",
                        }}
                      >
                        {item.law_name} • Section {item.section_number}
                      </div>

                      <div style={{ color: "#dbe4ff", lineHeight: 1.65, marginBottom: "14px" }}>
                        {item.summary}
                      </div>

                      <div
                        style={{
                          display: "grid",
                          gap: "10px",
                          marginBottom: "12px",
                        }}
                      >
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

                      <div
                        style={{
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "8px",
                        }}
                      >
                        {item.tags.slice(0, 5).map((tag) => (
                          <span
                            key={`${item.id}-${tag}`}
                            style={{
                              padding: "6px 10px",
                              borderRadius: "999px",
                              background: "rgba(126, 162, 255, 0.10)",
                              border: "1px solid rgba(126, 162, 255, 0.16)",
                              color: "#dce6ff",
                              fontSize: "12px",
                              fontWeight: 600,
                            }}
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </article>
                  ))}
                </div>
              )}
            </section>

            <section style={{ ...cardStyle, padding: "24px" }}>
              <div style={{ ...badge("pink"), marginBottom: "12px" }}>Still planned</div>
              <div
                style={{
                  fontSize: "24px",
                  fontWeight: 700,
                  marginBottom: "18px",
                }}
              >
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
