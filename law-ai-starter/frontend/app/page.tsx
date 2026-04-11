import Link from "next/link";

const sectionStyle: React.CSSProperties = {
  maxWidth: "1280px",
  margin: "0 auto",
  padding: "0 28px",
};

const cardStyle: React.CSSProperties = {
  background: "rgba(18, 28, 58, 0.9)",
  border: "1px solid rgba(120, 150, 255, 0.18)",
  borderRadius: "22px",
  padding: "28px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.18)",
};

const smallCardStyle: React.CSSProperties = {
  ...cardStyle,
  padding: "22px",
  height: "100%",
};

const primaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "14px 22px",
  borderRadius: "14px",
  background: "#7ea2ff",
  color: "#081227",
  fontWeight: 700,
  textDecoration: "none",
  border: "none",
};

const secondaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "14px 22px",
  borderRadius: "14px",
  background: "transparent",
  color: "#dfe7ff",
  fontWeight: 700,
  textDecoration: "none",
  border: "1px solid rgba(150, 170, 255, 0.28)",
};

export default function HomePage() {
  return (
    <main
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at top, rgba(45,78,180,0.22), transparent 24%), linear-gradient(180deg, #071226 0%, #09152b 100%)",
        color: "#f4f7ff",
      }}
    >
      <section style={{ ...sectionStyle, paddingTop: "72px", paddingBottom: "56px" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.2fr 0.8fr",
            gap: "24px",
            alignItems: "stretch",
          }}
        >
          <div style={cardStyle}>
            <div
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: "999px",
                background: "rgba(126, 162, 255, 0.12)",
                border: "1px solid rgba(126, 162, 255, 0.22)",
                color: "#b9caff",
                fontSize: "14px",
                fontWeight: 600,
                marginBottom: "18px",
              }}
            >
              Legal information platform
            </div>

            <h1
              style={{
                fontSize: "56px",
                lineHeight: 1.05,
                margin: "0 0 18px",
                letterSpacing: "-1.2px",
              }}
            >
              Understand laws, rights, and legal provisions with clarity.
            </h1>

            <p
              style={{
                fontSize: "20px",
                lineHeight: 1.6,
                color: "#d5def7",
                maxWidth: "760px",
                marginBottom: "28px",
              }}
            >
              Law AI is designed to help people explore legal information, understand
              rights, view relevant legal provisions, and see related sections in a
              structured way. It is built for awareness and guidance, not legal advice.
            </p>

            <div
              style={{
                display: "flex",
                gap: "14px",
                flexWrap: "wrap",
                marginBottom: "30px",
              }}
            >
              <Link href="/chat" style={primaryButton}>
                Open Legal Chat
              </Link>
              <Link href="/admin" style={secondaryButton}>
                View Admin Prototype
              </Link>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                gap: "14px",
              }}
            >
              {[
                ["Source-grounded answers", "Show relevant sections and citation blocks."],
                ["Officer authority lookup", "Understand public officer scope and hierarchy."],
                ["Safe legal-information framing", "Clearly separated from legal advice."],
              ].map(([title, text]) => (
                <div
                  key={title}
                  style={{
                    background: "rgba(10, 19, 43, 0.95)",
                    border: "1px solid rgba(132, 151, 220, 0.16)",
                    borderRadius: "16px",
                    padding: "16px",
                  }}
                >
                  <div style={{ fontWeight: 700, marginBottom: "8px", color: "#ffffff" }}>
                    {title}
                  </div>
                  <div style={{ color: "#c6d3f3", lineHeight: 1.5, fontSize: "15px" }}>
                    {text}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={cardStyle}>
            <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "12px" }}>
              What this MVP focuses on
            </div>

            <div
              style={{
                display: "grid",
                gap: "14px",
              }}
            >
              {[
                [
                  "Ask legal-information questions",
                  "Users can ask plain-language questions about laws, rights, penalties, and related provisions.",
                ],
                [
                  "View structured citations",
                  "Answers should point to relevant provisions instead of giving unsupported free-text responses.",
                ],
                [
                  "Explore overlapping laws",
                  "The system can later show how multiple provisions may relate to the same issue.",
                ],
                [
                  "Understand authority levels",
                  "Users can check what rank or public officer may have authority in a given context.",
                ],
              ].map(([title, text], index) => (
                <div
                  key={title}
                  style={{
                    display: "flex",
                    gap: "14px",
                    alignItems: "flex-start",
                    padding: "14px",
                    borderRadius: "16px",
                    background: "rgba(10, 19, 43, 0.92)",
                    border: "1px solid rgba(132, 151, 220, 0.14)",
                  }}
                >
                  <div
                    style={{
                      minWidth: "34px",
                      height: "34px",
                      borderRadius: "999px",
                      background: "rgba(126, 162, 255, 0.18)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: 700,
                      color: "#dfe7ff",
                    }}
                  >
                    {index + 1}
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, marginBottom: "6px" }}>{title}</div>
                    <div style={{ color: "#c6d3f3", lineHeight: 1.55 }}>{text}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section style={{ ...sectionStyle, paddingBottom: "28px" }}>
        <h2 style={{ fontSize: "34px", marginBottom: "18px" }}>Core product capabilities</h2>
        <p
          style={{
            color: "#c6d3f3",
            maxWidth: "820px",
            lineHeight: 1.7,
            marginBottom: "24px",
          }}
        >
          The first version should focus on trust, clarity, and structure. Instead of trying
          to behave like a lawyer, the product should help users understand information in a
          clean, transparent, and explainable way.
        </p>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: "18px",
          }}
        >
          {[
            {
              title: "Rights awareness",
              text: "Help citizens understand their rights in plain language.",
            },
            {
              title: "Legal provision mapping",
              text: "Map user questions to likely legal sections and related provisions.",
            },
            {
              title: "Punishment visibility",
              text: "Show how punishments and procedural references may connect.",
            },
            {
              title: "Officer authority lookup",
              text: "Display structured authority information rather than vague answers.",
            },
            {
              title: "Citation-first output",
              text: "Every useful answer should be supported by source references.",
            },
            {
              title: "Clear safety framing",
              text: "The platform should repeatedly distinguish legal information from advice.",
            },
          ].map((item) => (
            <div key={item.title} style={smallCardStyle}>
              <div style={{ fontSize: "20px", fontWeight: 700, marginBottom: "10px" }}>
                {item.title}
              </div>
              <div style={{ color: "#c6d3f3", lineHeight: 1.6 }}>{item.text}</div>
            </div>
          ))}
        </div>
      </section>

      <section style={{ ...sectionStyle, paddingTop: "18px", paddingBottom: "28px" }}>
        <div style={cardStyle}>
          <h2 style={{ fontSize: "34px", marginTop: 0, marginBottom: "18px" }}>
            How the product should work
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
              gap: "14px",
            }}
          >
            {[
              ["1. User asks a question", "A person describes a legal situation in plain language."],
              [
                "2. System classifies intent",
                "The backend identifies whether the query is about rights, punishment, authority, or legal overlap.",
              ],
              ["3. Relevant provisions are retrieved", "The system returns structured legal records and citations."],
              ["4. Response is explained safely", "The answer is shown as legal information with clear disclaimers."],
            ].map(([title, text]) => (
              <div
                key={title}
                style={{
                  background: "rgba(10, 19, 43, 0.95)",
                  border: "1px solid rgba(132, 151, 220, 0.16)",
                  borderRadius: "16px",
                  padding: "18px",
                }}
              >
                <div style={{ fontWeight: 700, marginBottom: "10px" }}>{title}</div>
                <div style={{ color: "#c6d3f3", lineHeight: 1.55 }}>{text}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section style={{ ...sectionStyle, paddingTop: "18px", paddingBottom: "70px" }}>
        <div
          style={{
            ...cardStyle,
            background: "linear-gradient(180deg, rgba(18, 28, 58, 0.98), rgba(11, 20, 45, 0.98))",
          }}
        >
          <h2 style={{ fontSize: "32px", marginTop: 0, marginBottom: "12px" }}>
            Important legal boundary
          </h2>
          <p
            style={{
              color: "#d7e0fb",
              fontSize: "18px",
              lineHeight: 1.7,
              marginBottom: "22px",
            }}
          >
            This product is intended for legal information, public awareness, and structured
            law exploration. It should not claim to replace a licensed lawyer, court filing
            strategy, or professional legal representation.
          </p>

          <div style={{ display: "flex", gap: "14px", flexWrap: "wrap" }}>
            <Link href="/chat" style={primaryButton}>
              Continue to Chat
            </Link>
            <a href="#top" style={secondaryButton}>
              Back to top
            </a>
          </div>
        </div>
      </section>
    </main>
  );
}