"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

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
  maxWidth: "1280px",
  margin: "0 auto",
  padding: "0 24px",
};

const cardStyle: React.CSSProperties = {
  background: "rgba(18, 28, 58, 0.92)",
  border: "1px solid rgba(120, 150, 255, 0.16)",
  borderRadius: "22px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.22)",
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

const statCardStyle: React.CSSProperties = {
  background: "rgba(10, 19, 43, 0.95)",
  border: "1px solid rgba(132, 151, 220, 0.14)",
  borderRadius: "18px",
  padding: "18px",
};

export default function AdminPage() {
  const [data, setData] = useState<AdminSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function fetchAdminSummary() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_BASE_URL}/api/v1/admin/summary`, {
          method: "GET",
          signal: controller.signal,
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const result: AdminSummaryResponse = await response.json();
        setData(result);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err.message || "Failed to load admin summary.");
        }
      } finally {
        setLoading(false);
      }
    }

    fetchAdminSummary();

    return () => controller.abort();
  }, []);

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
            <div
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: "999px",
                background: "rgba(126, 162, 255, 0.12)",
                border: "1px solid rgba(126, 162, 255, 0.22)",
                color: "#b9caff",
                fontSize: "13px",
                fontWeight: 600,
                marginBottom: "12px",
              }}
            >
              Internal control panel
            </div>

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
                maxWidth: "840px",
                color: "#c8d6f7",
                fontSize: "18px",
                lineHeight: 1.65,
              }}
            >
              This area is intended for internal management of legal source records,
              prompt policies, authority mappings, and future system controls. In the
              current prototype, it is a structured admin dashboard mockup.
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
            Loading admin summary...
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
            Failed to load admin summary: {error}
          </div>
        )}

        {data && (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                gap: "18px",
                marginBottom: "24px",
              }}
            >
              {data.stats.map((item) => (
                <div key={item.title} style={statCardStyle}>
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
                gridTemplateColumns: "0.9fr 1.1fr",
                gap: "24px",
                alignItems: "start",
                marginBottom: "24px",
              }}
            >
              <section style={{ ...cardStyle, padding: "24px" }}>
                <div
                  style={{
                    fontSize: "14px",
                    color: "#b9caff",
                    marginBottom: "8px",
                  }}
                >
                  Admin modules
                </div>
                <div
                  style={{
                    fontSize: "24px",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Control areas
                </div>

                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "14px",
                  }}
                >
                  {data.control_areas.map((item) => (
                    <div
                      key={item.title}
                      style={{
                        background: "rgba(10, 19, 43, 0.95)",
                        border: "1px solid rgba(132, 151, 220, 0.14)",
                        borderRadius: "18px",
                        padding: "16px",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "17px",
                          fontWeight: 700,
                          marginBottom: "8px",
                          color: "#ffffff",
                        }}
                      >
                        {item.title}
                      </div>
                      <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>
                        {item.text}
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section style={{ ...cardStyle, padding: "24px" }}>
                <div
                  style={{
                    fontSize: "14px",
                    color: "#b9caff",
                    marginBottom: "8px",
                  }}
                >
                  Current admin overview
                </div>
                <div
                  style={{
                    fontSize: "24px",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Prototype management dashboard
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "16px",
                    marginBottom: "18px",
                  }}
                >
                  {data.status_cards.map((item) => (
                    <div key={item.title} style={statCardStyle}>
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
                      <div style={{ color: "#f4f7ff", lineHeight: 1.7 }}>
                        {item.content}
                      </div>
                    </div>
                  ))}
                </div>

                <div
                  style={{
                    background: "rgba(10, 19, 43, 0.95)",
                    border: "1px solid rgba(132, 151, 220, 0.14)",
                    borderRadius: "18px",
                    padding: "18px",
                    marginBottom: "18px",
                  }}
                >
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

                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "12px",
                    }}
                  >
                    {data.workflow_steps.map((item, index) => (
                      <div
                        key={item}
                        style={{
                          display: "flex",
                          gap: "12px",
                          alignItems: "flex-start",
                        }}
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
                        <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>
                          {item}
                        </div>
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
                  <div
                    style={{
                      fontSize: "15px",
                      fontWeight: 700,
                      marginBottom: "10px",
                    }}
                  >
                    Important admin boundary
                  </div>
                  <div
                    style={{
                      color: "#ffe7ec",
                      lineHeight: 1.7,
                      fontSize: "15px",
                    }}
                  >
                    {data.admin_boundary}
                  </div>
                </div>
              </section>
            </div>

            <section style={{ ...cardStyle, padding: "24px" }}>
              <div
                style={{
                  fontSize: "14px",
                  color: "#b9caff",
                  marginBottom: "8px",
                }}
              >
                Future admin roadmap
              </div>
              <div
                style={{
                  fontSize: "24px",
                  fontWeight: 700,
                  marginBottom: "18px",
                }}
              >
                Planned next internal capabilities
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                  gap: "18px",
                }}
              >
                {data.roadmap_items.map((item) => (
                  <div key={item.title} style={statCardStyle}>
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
                    <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>
                      {item.text}
                    </div>
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