"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

type OfficerAuthorityResponse = {
  rank: string;
  summary: string;
  powers: string[];
  limitations: string[];
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

const primaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  border: "none",
  borderRadius: "14px",
  padding: "14px 20px",
  background: "#7ea2ff",
  color: "#081227",
  fontWeight: 700,
  fontSize: "15px",
  cursor: "pointer",
  textDecoration: "none",
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

const exampleButtonStyle: React.CSSProperties = {
  background: "rgba(126, 162, 255, 0.08)",
  color: "#dfe7ff",
  border: "1px solid rgba(126, 162, 255, 0.18)",
  borderRadius: "999px",
  padding: "10px 14px",
  fontSize: "14px",
  cursor: "pointer",
};

const ranks = [
  { label: "SHO", value: "sho" },
  { label: "ASI", value: "asi" },
  { label: "Inspector", value: "inspector" },
];

export default function OfficerAuthorityPage() {
  const [rank, setRank] = useState("sho");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<OfficerAuthorityResponse | null>(null);

  const titleRank = useMemo(() => {
    const match = ranks.find((item) => item.value === rank);
    return match?.label || rank.toUpperCase();
  }, [rank]);

  async function fetchAuthority(selectedRank?: string) {
    const targetRank = (selectedRank || rank).trim().toLowerCase();
    if (!targetRank) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/officer-authority/${encodeURIComponent(targetRank)}`,
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(errorBody?.detail || "Failed to fetch officer authority.");
      }

      const data: OfficerAuthorityResponse = await response.json();
      setResult(data);
      setRank(targetRank);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Failed to fetch officer authority.");
    } finally {
      setLoading(false);
    }
  }

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
              Structured authority lookup
            </div>

            <h1
              style={{
                fontSize: "44px",
                lineHeight: 1.08,
                letterSpacing: "-1px",
                margin: "0 0 10px",
              }}
            >
              Officer Authority Lookup
            </h1>

            <p
              style={{
                margin: 0,
                maxWidth: "820px",
                color: "#c8d6f7",
                fontSize: "18px",
                lineHeight: 1.65,
              }}
            >
              This module is designed to show structured public-officer authority
              information. It should explain the officer rank, a short summary,
              likely powers, and key limitations in a clear and non-misleading way.
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

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "0.85fr 1.15fr",
            gap: "24px",
            alignItems: "start",
          }}
        >
          <section style={{ ...cardStyle, padding: "24px" }}>
            <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
              Search officer rank
            </div>
            <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "16px" }}>
              Check authority details
            </div>

            <label
              htmlFor="rank"
              style={{
                display: "block",
                fontSize: "14px",
                color: "#d7e0fb",
                marginBottom: "8px",
              }}
            >
              Officer rank
            </label>

            <input
              id="rank"
              value={rank}
              onChange={(event) => setRank(event.target.value)}
              placeholder="Enter rank, e.g. sho"
              style={{
                width: "100%",
                padding: "16px",
                borderRadius: "16px",
                background: "rgba(8, 18, 39, 0.86)",
                border: "1px solid rgba(132, 151, 220, 0.18)",
                color: "#f4f7ff",
                outline: "none",
                fontSize: "16px",
                lineHeight: 1.5,
                marginBottom: "14px",
              }}
            />

            <button
              onClick={() => void fetchAuthority()}
              disabled={loading || !rank.trim()}
              style={{
                ...primaryButton,
                width: "100%",
                opacity: loading || !rank.trim() ? 0.65 : 1,
                cursor: loading || !rank.trim() ? "not-allowed" : "pointer",
                marginBottom: "18px",
              }}
            >
              {loading ? "Loading authority..." : "Check authority"}
            </button>

            <div style={{ marginBottom: "12px", fontSize: "14px", color: "#b9caff" }}>
              Quick examples
            </div>

            <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
              {ranks.map((item) => (
                <button
                  key={item.value}
                  onClick={() => void fetchAuthority(item.value)}
                  style={exampleButtonStyle}
                >
                  {item.label}
                </button>
              ))}
            </div>

            {error && (
              <div
                style={{
                  marginTop: "18px",
                  background: "rgba(58, 18, 32, 0.75)",
                  border: "1px solid rgba(255, 118, 145, 0.24)",
                  borderRadius: "16px",
                  padding: "16px",
                }}
              >
                <div style={{ fontWeight: 700, marginBottom: "8px", color: "#ffd2db" }}>
                  Request error
                </div>
                <div style={{ color: "#ffe7ec", lineHeight: 1.6 }}>{error}</div>
              </div>
            )}
          </section>

          <section style={{ ...cardStyle, padding: "24px" }}>
            <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
              Authority response
            </div>
            <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "18px" }}>
              {result ? `${result.rank} authority details` : `${titleRank} authority details`}
            </div>

            {!result ? (
              <div
                style={{
                  background: "rgba(10, 19, 43, 0.95)",
                  border: "1px solid rgba(132, 151, 220, 0.14)",
                  borderRadius: "18px",
                  padding: "18px",
                  color: "#d7e0fb",
                  lineHeight: 1.7,
                }}
              >
                Select a rank such as <strong>SHO</strong>, <strong>ASI</strong>, or{" "}
                <strong>Inspector</strong> to load structured authority information from the
                backend.
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
                <div
                  style={{
                    background: "rgba(10, 19, 43, 0.95)",
                    border: "1px solid rgba(132, 151, 220, 0.14)",
                    borderRadius: "18px",
                    padding: "18px",
                  }}
                >
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
                    Summary
                  </div>
                  <div style={{ color: "#f4f7ff", lineHeight: 1.7, fontSize: "17px" }}>
                    {result.summary}
                  </div>
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "18px",
                  }}
                >
                  <div
                    style={{
                      background: "rgba(10, 19, 43, 0.95)",
                      border: "1px solid rgba(132, 151, 220, 0.14)",
                      borderRadius: "18px",
                      padding: "18px",
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
                      Likely powers
                    </div>

                    <ul
                      style={{
                        margin: 0,
                        paddingLeft: "20px",
                        color: "#dfe7ff",
                        lineHeight: 1.8,
                      }}
                    >
                      {result.powers.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>

                  <div
                    style={{
                      background: "rgba(10, 19, 43, 0.95)",
                      border: "1px solid rgba(132, 151, 220, 0.14)",
                      borderRadius: "18px",
                      padding: "18px",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "13px",
                        fontWeight: 700,
                        letterSpacing: "1px",
                        textTransform: "uppercase",
                        color: "#ffcfda",
                        marginBottom: "12px",
                      }}
                    >
                      Key limitations
                    </div>

                    <ul
                      style={{
                        margin: 0,
                        paddingLeft: "20px",
                        color: "#ffe7ec",
                        lineHeight: 1.8,
                      }}
                    >
                      {result.limitations.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div
                  style={{
                    background: "linear-gradient(180deg, rgba(58, 22, 32, 0.75), rgba(45, 18, 26, 0.78))",
                    border: "1px solid rgba(255, 150, 170, 0.18)",
                    borderRadius: "18px",
                    padding: "18px",
                  }}
                >
                  <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>
                    Important boundary
                  </div>
                  <div style={{ color: "#ffe7ec", lineHeight: 1.7, fontSize: "15px" }}>
                    Officer authority may depend on jurisdiction, procedure, assignment,
                    and applicable law. This module is for structured legal information,
                    not a final legal determination.
                  </div>
                </div>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}