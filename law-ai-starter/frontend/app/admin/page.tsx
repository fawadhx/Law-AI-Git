"use client";

import Link from "next/link";

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

const statCardStyle: React.CSSProperties = {
  background: "rgba(10, 19, 43, 0.95)",
  border: "1px solid rgba(132, 151, 220, 0.14)",
  borderRadius: "18px",
  padding: "18px",
};

export default function AdminPage() {
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

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: "18px",
            marginBottom: "24px",
          }}
        >
          {[
            ["128", "Source records", "Total legal source records tracked in the admin layer."],
            ["18", "Authority mappings", "Structured rank and authority mappings configured."],
            ["06", "Prompt rules", "Prompt policy groups for safe legal-information responses."],
            ["03", "Draft modules", "Upcoming modules prepared for future implementation."],
          ].map(([value, title, text]) => (
            <div key={title} style={statCardStyle}>
              <div
                style={{
                  fontSize: "34px",
                  fontWeight: 800,
                  marginBottom: "8px",
                  color: "#ffffff",
                }}
              >
                {value}
              </div>
              <div
                style={{
                  fontSize: "16px",
                  fontWeight: 700,
                  marginBottom: "8px",
                  color: "#dfe7ff",
                }}
              >
                {title}
              </div>
              <div style={{ color: "#c6d3f3", lineHeight: 1.6, fontSize: "14px" }}>
                {text}
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
            <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
              Admin modules
            </div>
            <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "16px" }}>
              Control areas
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              {[
                [
                  "Legal source records",
                  "Upload, store, edit, review, and version structured legal source records.",
                ],
                [
                  "Prompt and policy controls",
                  "Manage system instructions, disclaimers, and response safety behavior.",
                ],
                [
                  "Authority mappings",
                  "Maintain officer-rank mappings, summaries, powers, and limitations.",
                ],
                [
                  "Future retrieval controls",
                  "Prepare retrieval configuration, source quality checks, and review workflows.",
                ],
              ].map(([title, text]) => (
                <div
                  key={title}
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
                    {title}
                  </div>
                  <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>{text}</div>
                </div>
              ))}
            </div>
          </section>

          <section style={{ ...cardStyle, padding: "24px" }}>
            <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
              Current admin overview
            </div>
            <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "16px" }}>
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
              <div style={statCardStyle}>
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
                  Source status
                </div>
                <div style={{ color: "#f4f7ff", lineHeight: 1.7 }}>
                  Core law source management is planned but not yet connected to real
                  database records.
                </div>
              </div>

              <div style={statCardStyle}>
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
                  Prompt status
                </div>
                <div style={{ color: "#f4f7ff", lineHeight: 1.7 }}>
                  Prompt control is currently conceptual and will later move into
                  backend-managed policy records.
                </div>
              </div>
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

              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                {[
                  "Review legal source entries before publishing them to production.",
                  "Maintain disclaimers and legal-information boundaries centrally.",
                  "Version prompt policies and authority records for traceability.",
                  "Prepare future review states such as draft, reviewed, approved, and archived.",
                ].map((item, index) => (
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
                    <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{item}</div>
                  </div>
                ))}
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
                Important admin boundary
              </div>
              <div style={{ color: "#ffe7ec", lineHeight: 1.7, fontSize: "15px" }}>
                This admin screen is a prototype control panel. Authentication, access
                control, upload workflows, audit logging, and source approval logic
                should be added before treating it as a real production admin system.
              </div>
            </div>
          </section>
        </div>

        <section style={{ ...cardStyle, padding: "24px" }}>
          <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
            Future admin roadmap
          </div>
          <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "18px" }}>
            Planned next internal capabilities
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
              gap: "18px",
            }}
          >
            {[
              {
                title: "Source upload manager",
                text: "Upload and normalize legal documents into structured internal records.",
              },
              {
                title: "Prompt policy editor",
                text: "Manage system disclaimers, classifications, and response control logic.",
              },
              {
                title: "Authority records panel",
                text: "Edit officer-rank summaries, powers, and limitations from admin UI.",
              },
              {
                title: "Review workflow",
                text: "Move source records through draft, review, approval, and archive stages.",
              },
              {
                title: "Audit trail",
                text: "Track source changes, policy edits, and future admin activity logs.",
              },
              {
                title: "Role-based access",
                text: "Limit admin features by role before any production deployment.",
              },
            ].map((item) => (
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
                <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>{item.text}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}