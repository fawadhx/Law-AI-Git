"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { CSSProperties, FormEvent, ReactNode } from "react";

type Citation = {
  title: string;
  section: string;
  note: string;
  excerpt: string;
};

type ChatCategory = {
  key: string;
  label: string;
};

type ChatConfidence = {
  level: string;
  score: number;
  matched_records: number;
};

type MatchExplanation = {
  title: string;
  points: string[];
};

type ChatQueryResponse = {
  answer: string;
  citations: Citation[];
  disclaimer: string;
  category: ChatCategory;
  confidence: ChatConfidence;
  why_matched: MatchExplanation[];
};

type Message = {
  role: "user" | "assistant";
  content: string;
  category?: ChatCategory;
  confidence?: ChatConfidence;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

const pageWrap: CSSProperties = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top, rgba(45,78,180,0.18), transparent 24%), linear-gradient(180deg, #071226 0%, #09152b 100%)",
  color: "#f4f7ff",
  padding: "24px 0 44px",
};

const containerStyle: CSSProperties = {
  maxWidth: "1320px",
  margin: "0 auto",
  padding: "0 18px",
};

const cardStyle: CSSProperties = {
  background: "rgba(18, 28, 58, 0.92)",
  border: "1px solid rgba(120, 150, 255, 0.16)",
  borderRadius: "22px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.22)",
};

const sectionLabelStyle: CSSProperties = {
  fontSize: "11px",
  color: "#b9caff",
  marginBottom: "8px",
  fontWeight: 800,
  textTransform: "uppercase",
  letterSpacing: "0.7px",
};

const sectionTitleStyle: CSSProperties = {
  fontSize: "19px",
  fontWeight: 700,
  marginBottom: "12px",
  lineHeight: 1.3,
};

const mutedBodyStyle: CSSProperties = {
  color: "#dbe4ff",
  lineHeight: 1.65,
  fontSize: "14px",
};

const panelInnerCardStyle: CSSProperties = {
  background: "rgba(10, 19, 43, 0.95)",
  border: "1px solid rgba(132, 151, 220, 0.14)",
  borderRadius: "16px",
  padding: "13px",
};

const secondaryButton: CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "14px",
  padding: "11px 15px",
  background: "transparent",
  color: "#dfe7ff",
  fontWeight: 700,
  fontSize: "14px",
  cursor: "pointer",
  textDecoration: "none",
  border: "1px solid rgba(150, 170, 255, 0.26)",
};

const primaryButton: CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  border: "none",
  borderRadius: "14px",
  padding: "12px 18px",
  background: "#7ea2ff",
  color: "#081227",
  fontWeight: 800,
  fontSize: "14px",
  cursor: "pointer",
};

const EXAMPLE_GROUPS = [
  {
    title: "Theft / Property",
    examples: [
      "What punishment can happen if someone steals property?",
      "Does theft require dishonest taking of movable property?",
    ],
  },
  {
    title: "Threats / Intimidation",
    examples: [
      "Someone is threatening me online",
      "What law may apply if someone threatens my reputation or property?",
    ],
  },
  {
    title: "Police / Detention",
    examples: [
      "Can police keep a person more than 24 hours?",
      "When may police arrest without a warrant?",
    ],
  },
  {
    title: "Reputation / Online Harm",
    examples: [
      "Someone harmed my reputation on social media",
      "What PECA section may apply to online dignity or privacy harm?",
    ],
  },
  {
    title: "General / Weak Match",
    examples: ["I have some legal issue", "Somebody did something bad"],
  },
];

function getConfidenceBadgeStyle(level?: string): CSSProperties {
  if (level === "high") {
    return {
      background: "rgba(34, 197, 94, 0.16)",
      border: "1px solid rgba(34, 197, 94, 0.28)",
      color: "#bbf7d0",
    };
  }

  if (level === "medium") {
    return {
      background: "rgba(250, 204, 21, 0.14)",
      border: "1px solid rgba(250, 204, 21, 0.26)",
      color: "#fde68a",
    };
  }

  return {
    background: "rgba(248, 113, 113, 0.14)",
    border: "1px solid rgba(248, 113, 113, 0.24)",
    color: "#fecaca",
  };
}

function getShortExcerpt(text?: string, maxLength: number = 140): string {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength).trim()}...`;
}

function formatScore(score?: number): string {
  if (typeof score !== "number" || Number.isNaN(score)) return "--";
  return score.toFixed(1);
}

function getAnswerStatusConfig(confidence?: ChatConfidence): {
  label: string;
  description: string;
  style: CSSProperties;
} | null {
  if (!confidence) return null;

  if (confidence.level === "high") {
    return {
      label: "Strong match",
      description: "The prototype found a comparatively strong legal-source match.",
      style: {
        background: "rgba(34, 197, 94, 0.14)",
        border: "1px solid rgba(34, 197, 94, 0.24)",
        color: "#dcfce7",
      },
    };
  }

  if (confidence.level === "medium") {
    return {
      label: "Reasonable match",
      description: "The result looks usable, but it should still be read cautiously.",
      style: {
        background: "rgba(250, 204, 21, 0.12)",
        border: "1px solid rgba(250, 204, 21, 0.22)",
        color: "#fef3c7",
      },
    };
  }

  return {
    label: "Tentative match",
    description: "Only a limited match was found, so this answer needs extra caution.",
    style: {
      background: "rgba(248, 113, 113, 0.12)",
      border: "1px solid rgba(248, 113, 113, 0.22)",
      color: "#fee2e2",
    },
  };
}

function getConfidenceDescription(confidence?: ChatConfidence): string {
  if (!confidence) {
    return "Submit a question to see backend confidence scoring for the current prototype match.";
  }

  if (confidence.level === "high") {
    return "The current prototype found a comparatively strong internal legal-source match.";
  }

  if (confidence.level === "medium") {
    return "The prototype found a reasonable match, but the answer should still be read cautiously.";
  }

  return "The prototype found only a limited match, so the answer should be treated with extra caution.";
}

function SmallPill({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "8px",
        padding: "6px 10px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 800,
        lineHeight: 1.2,
        ...style,
      }}
    >
      {children}
    </div>
  );
}

function SectionCard({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <section style={{ ...cardStyle, padding: "18px" }}>
      <div style={sectionLabelStyle}>{eyebrow}</div>
      <div style={sectionTitleStyle}>{title}</div>
      {children}
    </section>
  );
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={panelInnerCardStyle}>
      <div style={sectionLabelStyle}>{label}</div>
      <div style={{ fontSize: "21px", fontWeight: 800 }}>{value}</div>
    </div>
  );
}

function EmptyPanel({ text }: { text: string }) {
  return (
    <div style={{ ...panelInnerCardStyle, color: "#c6d3f3", lineHeight: 1.7 }}>
      {text}
    </div>
  );
}

function ExampleGroupCard({
  title,
  examples,
  onApply,
}: {
  title: string;
  examples: string[];
  onApply: (example: string) => void;
}) {
  return (
    <div style={panelInnerCardStyle}>
      <div
        style={{
          fontSize: "12px",
          fontWeight: 800,
          textTransform: "uppercase",
          letterSpacing: "0.6px",
          color: "#a9c1ff",
          marginBottom: "10px",
        }}
      >
        {title}
      </div>

      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {examples.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => onApply(example)}
            style={{
              borderRadius: "999px",
              padding: "8px 11px",
              background: "rgba(126, 162, 255, 0.10)",
              border: "1px solid rgba(126, 162, 255, 0.20)",
              color: "#dfe7ff",
              fontSize: "12px",
              cursor: "pointer",
              textAlign: "left",
            }}
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const statusConfig =
    message.role === "assistant" ? getAnswerStatusConfig(message.confidence) : null;

  return (
    <div
      style={{
        alignSelf: message.role === "user" ? "flex-end" : "stretch",
        maxWidth: message.role === "user" ? "74%" : "100%",
        marginLeft: message.role === "user" ? "auto" : 0,
        background:
          message.role === "user"
            ? "rgba(126, 162, 255, 0.16)"
            : "rgba(10, 19, 43, 0.95)",
        border:
          message.role === "user"
            ? "1px solid rgba(126, 162, 255, 0.22)"
            : "1px solid rgba(132, 151, 220, 0.14)",
        borderRadius: "18px",
        padding: message.role === "user" ? "12px 13px" : "13px 14px",
        overflowWrap: "anywhere",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "10px",
          flexWrap: "wrap",
          marginBottom: "9px",
        }}
      >
        <div
          style={{
            fontSize: "11px",
            fontWeight: 800,
            letterSpacing: "0.6px",
            textTransform: "uppercase",
            color: message.role === "user" ? "#cfe0ff" : "#a9c1ff",
          }}
        >
          {message.role === "user" ? "You" : "Law AI"}
        </div>

        {message.role === "assistant" && (message.category || message.confidence) && (
          <div style={{ display: "flex", gap: "7px", flexWrap: "wrap" }}>
            {message.category && (
              <SmallPill
                style={{
                  background: "rgba(126, 162, 255, 0.12)",
                  border: "1px solid rgba(126, 162, 255, 0.22)",
                  color: "#dfe7ff",
                }}
              >
                {message.category.label}
              </SmallPill>
            )}

            {message.confidence && (
              <SmallPill style={getConfidenceBadgeStyle(message.confidence.level)}>
                {message.confidence.level.toUpperCase()}
              </SmallPill>
            )}
          </div>
        )}
      </div>

      {statusConfig && (
        <div
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "flex-start",
            flexWrap: "wrap",
            borderRadius: "14px",
            padding: "10px 11px",
            marginBottom: "11px",
            ...statusConfig.style,
          }}
        >
          <div
            style={{
              fontSize: "11px",
              fontWeight: 800,
              textTransform: "uppercase",
              letterSpacing: "0.6px",
              whiteSpace: "nowrap",
            }}
          >
            {statusConfig.label}
          </div>
          <div style={{ fontSize: "12px", lineHeight: 1.6, flex: 1 }}>{statusConfig.description}</div>
        </div>
      )}

      <div
        style={{
          whiteSpace: "pre-wrap",
          color: "#edf2ff",
          lineHeight: 1.72,
          fontSize: "14px",
        }}
      >
        {message.content}
      </div>
    </div>
  );
}

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Ask a legal-information question to receive a prototype response based on the current structured legal-source records.",
    },
  ]);
  const [latestResponse, setLatestResponse] = useState<ChatQueryResponse | null>(null);

  const messageCount = messages.length;
  const assistantCount = useMemo(
    () => messages.filter((message) => message.role === "assistant").length,
    [messages]
  );

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || loading) return;

    setLoading(true);
    setError("");

    setMessages((prev) => [...prev, { role: "user", content: trimmedQuestion }]);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: trimmedQuestion }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const result: ChatQueryResponse = await response.json();

      setLatestResponse(result);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          category: result.category,
          confidence: result.confidence,
        },
      ]);
      setQuestion("");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to fetch response.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function applyExample(example: string) {
    setQuestion(example);
  }

  return (
    <main style={pageWrap}>
      <div style={containerStyle}>
        <div className="chat-page-shell">
          <div className="hero-row">
            <div>
              <div
                style={{
                  display: "inline-block",
                  padding: "7px 11px",
                  borderRadius: "999px",
                  background: "rgba(126, 162, 255, 0.12)",
                  border: "1px solid rgba(126, 162, 255, 0.22)",
                  color: "#b9caff",
                  fontSize: "12px",
                  fontWeight: 700,
                  marginBottom: "12px",
                  letterSpacing: "0.4px",
                }}
              >
                Legal information assistant
              </div>

              <h1
                style={{
                  fontSize: "clamp(28px, 5vw, 40px)",
                  lineHeight: 1.05,
                  letterSpacing: "-1px",
                  margin: "0 0 10px",
                }}
              >
                Legal Chat
              </h1>

              <p
                style={{
                  margin: 0,
                  maxWidth: "760px",
                  color: "#c8d6f7",
                  fontSize: "15px",
                  lineHeight: 1.7,
                }}
              >
                Ask a legal-information question and the system will try to match it
                against the current structured prototype dataset, return supporting
                citations, classify the issue type, and show match confidence.
              </p>
            </div>

            <div className="hero-actions">
              <Link href="/" style={secondaryButton}>
                Back to Homepage
              </Link>
              <Link href="/officer-authority" style={secondaryButton}>
                Officer Authority
              </Link>
            </div>
          </div>

          <div className="content-grid">
            <section style={{ ...cardStyle, padding: "18px" }}>
              <div className="conversation-header">
                <div>
                  <div style={sectionLabelStyle}>Conversation</div>
                  <div style={{ ...sectionTitleStyle, marginBottom: "6px" }}>
                    Ask a legal-information question
                  </div>
                  <div style={{ ...mutedBodyStyle, marginBottom: "14px" }}>
                    The left panel stays focused on the conversation, while the right
                    side shows the current matched result snapshot.
                  </div>
                </div>

                <div className="conversation-stats">
                  <SmallPill
                    style={{
                      background: "rgba(126, 162, 255, 0.10)",
                      border: "1px solid rgba(126, 162, 255, 0.20)",
                      color: "#dfe7ff",
                    }}
                  >
                    Messages: {messageCount}
                  </SmallPill>
                  <SmallPill
                    style={{
                      background: "rgba(126, 162, 255, 0.08)",
                      border: "1px solid rgba(126, 162, 255, 0.16)",
                      color: "#cfe0ff",
                    }}
                  >
                    Assistant replies: {assistantCount}
                  </SmallPill>
                  {latestResponse?.category && (
                    <SmallPill
                      style={{
                        background: "rgba(126, 162, 255, 0.08)",
                        border: "1px solid rgba(126, 162, 255, 0.16)",
                        color: "#cfe0ff",
                      }}
                    >
                      Current issue: {latestResponse.category.label}
                    </SmallPill>
                  )}
                </div>
              </div>

              <div className="messages-pane">
                {messages.map((message, index) => (
                  <MessageBubble key={`${message.role}-${index}`} message={message} />
                ))}
              </div>

              <form onSubmit={handleSubmit} className="composer-card">
                <div className="composer-head">
                  <label
                    htmlFor="question"
                    style={{
                      display: "block",
                      fontSize: "13px",
                      color: "#b9caff",
                      fontWeight: 700,
                    }}
                  >
                    Your question
                  </label>

                  <div style={{ fontSize: "12px", color: "#9fb4e8" }}>
                    Keep it specific for better matching.
                  </div>
                </div>

                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Example: Can police detain a person for more than 24 hours?"
                  rows={4}
                  style={{
                    width: "100%",
                    resize: "vertical",
                    borderRadius: "16px",
                    border: "1px solid rgba(126, 162, 255, 0.22)",
                    background: "rgba(8, 17, 38, 0.95)",
                    color: "#f4f7ff",
                    padding: "14px",
                    fontSize: "14px",
                    lineHeight: 1.7,
                    outline: "none",
                    minHeight: "116px",
                    marginBottom: "12px",
                  }}
                />

                <div className="composer-footer">
                  <button
                    type="submit"
                    disabled={loading}
                    style={{
                      ...primaryButton,
                      opacity: loading ? 0.7 : 1,
                    }}
                  >
                    {loading ? "Thinking..." : "Ask Question"}
                  </button>

                  <div style={{ fontSize: "12px", color: "#9fb4e8" }}>
                    Legal information only — not legal advice.
                  </div>
                </div>

                {error && (
                  <div
                    style={{
                      marginTop: "12px",
                      borderRadius: "14px",
                      padding: "13px 15px",
                      background: "rgba(65, 18, 28, 0.8)",
                      border: "1px solid rgba(255, 120, 120, 0.22)",
                      color: "#ffd7df",
                      lineHeight: 1.7,
                      fontSize: "14px",
                    }}
                  >
                    Failed to fetch response: {error}
                  </div>
                )}
              </form>

              <div style={{ marginTop: "16px" }}>
                <div style={{ ...sectionLabelStyle, marginBottom: "10px" }}>
                  Quick examples by issue type
                </div>

                <div className="examples-grid">
                  {EXAMPLE_GROUPS.map((group) => (
                    <ExampleGroupCard
                      key={group.title}
                      title={group.title}
                      examples={group.examples}
                      onApply={applyExample}
                    />
                  ))}
                </div>
              </div>
            </section>

            <aside className="sidebar-stack">
              <SectionCard
                eyebrow="Current result snapshot"
                title="Detected category and confidence"
              >
                <div className="snapshot-head">
                  <div>
                    <div
                      style={{
                        fontSize: "21px",
                        fontWeight: 800,
                        lineHeight: 1.25,
                        marginBottom: "6px",
                      }}
                    >
                      {latestResponse?.category?.label || "No category yet"}
                    </div>
                    <div style={mutedBodyStyle}>
                      {latestResponse
                        ? `Structured category key: ${latestResponse.category.key}`
                        : "Submit a question to see the detected category returned by the backend."}
                    </div>
                  </div>

                  {latestResponse?.confidence && (
                    <SmallPill style={getConfidenceBadgeStyle(latestResponse.confidence.level)}>
                      {latestResponse.confidence.level.toUpperCase()} confidence
                    </SmallPill>
                  )}
                </div>

                <div className="stats-grid compact-grid">
                  <StatCard
                    label="Top match score"
                    value={formatScore(latestResponse?.confidence?.score)}
                  />
                  <StatCard
                    label="Matched records"
                    value={latestResponse?.confidence?.matched_records ?? "--"}
                  />
                </div>

                <div style={{ ...mutedBodyStyle, marginTop: "13px" }}>
                  {getConfidenceDescription(latestResponse?.confidence)}
                </div>

                <div style={{ ...panelInnerCardStyle, marginTop: "13px" }}>
                  <div style={sectionLabelStyle}>Legal boundary</div>
                  <div style={mutedBodyStyle}>
                    {latestResponse?.disclaimer ||
                      "This system is for legal information and public awareness only. It must not be treated as a lawyer or a substitute for legal advice."}
                  </div>
                </div>
              </SectionCard>

              <SectionCard eyebrow="Why this matched" title="Match explanation">
                <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  {latestResponse?.why_matched?.length ? (
                    latestResponse.why_matched.map((item, index) => (
                      <div key={`${item.title}-${index}`} style={panelInnerCardStyle}>
                        <div
                          style={{
                            fontSize: "14px",
                            fontWeight: 700,
                            color: "#ffffff",
                            lineHeight: 1.5,
                            marginBottom: "9px",
                          }}
                        >
                          {item.title}
                        </div>

                        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                          {item.points.map((point, pointIndex) => (
                            <div
                              key={`${item.title}-${pointIndex}`}
                              style={{
                                color: "#dbe4ff",
                                lineHeight: 1.6,
                                fontSize: "13px",
                              }}
                            >
                              • {point}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <EmptyPanel text="Ask a question to see which keywords, tags, or legal signals likely caused the current match." />
                  )}
                </div>
              </SectionCard>

              <SectionCard eyebrow="Matched legal records" title="Top matched provisions">
                <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  {latestResponse?.citations?.length ? (
                    latestResponse.citations.map((citation, index) => (
                      <div key={`matched-record-${citation.title}-${index}`} style={panelInnerCardStyle}>
                        <div className="record-header">
                          <SmallPill
                            style={{
                              background: "rgba(126, 162, 255, 0.10)",
                              border: "1px solid rgba(126, 162, 255, 0.18)",
                              color: "#cfe0ff",
                            }}
                          >
                            Match #{index + 1}
                          </SmallPill>
                        </div>

                        <div
                          style={{
                            fontSize: "14px",
                            fontWeight: 700,
                            color: "#ffffff",
                            lineHeight: 1.5,
                            marginBottom: "6px",
                          }}
                        >
                          {citation.section}
                        </div>

                        <div
                          style={{
                            fontSize: "12px",
                            color: "#a9c1ff",
                            marginBottom: "8px",
                            lineHeight: 1.55,
                          }}
                        >
                          {citation.title}
                        </div>

                        <div
                          style={{
                            color: "#dbe4ff",
                            lineHeight: 1.6,
                            fontSize: "13px",
                            marginBottom: citation.excerpt ? "9px" : 0,
                          }}
                        >
                          {citation.note}
                        </div>

                        {citation.excerpt && (
                          <div
                            style={{
                              background: "rgba(126, 162, 255, 0.08)",
                              border: "1px solid rgba(126, 162, 255, 0.14)",
                              borderRadius: "14px",
                              padding: "10px 11px",
                            }}
                          >
                            <div
                              style={{
                                fontSize: "11px",
                                fontWeight: 700,
                                textTransform: "uppercase",
                                letterSpacing: "0.6px",
                                color: "#b9caff",
                                marginBottom: "7px",
                              }}
                            >
                              Source excerpt
                            </div>
                            <div
                              style={{
                                color: "#edf2ff",
                                lineHeight: 1.6,
                                fontSize: "12px",
                                fontStyle: "italic",
                              }}
                            >
                              “{getShortExcerpt(citation.excerpt, 160)}”
                            </div>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <EmptyPanel text="Ask a question to see the top matched legal provisions and their source excerpts." />
                  )}
                </div>
              </SectionCard>
            </aside>
          </div>
        </div>
      </div>

      <style jsx>{`
        .chat-page-shell {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .hero-row {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 18px;
          flex-wrap: wrap;
        }

        .hero-actions {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .content-grid {
          display: grid;
          grid-template-columns: minmax(0, 1.5fr) minmax(310px, 0.82fr);
          gap: 18px;
          align-items: start;
        }

        .conversation-header {
          margin-bottom: 14px;
        }

        .conversation-stats {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .messages-pane {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 14px;
          max-height: 660px;
          overflow-y: auto;
          padding-right: 4px;
        }

        .composer-card {
          background: rgba(10, 19, 43, 0.78);
          border: 1px solid rgba(132, 151, 220, 0.14);
          border-radius: 18px;
          padding: 14px;
        }

        .composer-head,
        .composer-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          flex-wrap: wrap;
        }

        .composer-head {
          margin-bottom: 10px;
        }

        .composer-footer {
          margin-bottom: 0;
        }

        .examples-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 10px;
        }

        .sidebar-stack {
          display: flex;
          flex-direction: column;
          gap: 18px;
          position: sticky;
          top: 18px;
        }

        .snapshot-head {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 12px;
          flex-wrap: wrap;
          margin-bottom: 12px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 10px;
        }

        .record-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          margin-bottom: 8px;
          flex-wrap: wrap;
        }

        .messages-pane::-webkit-scrollbar {
          width: 8px;
        }

        .messages-pane::-webkit-scrollbar-thumb {
          background: rgba(126, 162, 255, 0.22);
          border-radius: 999px;
        }

        @media (max-width: 1100px) {
          .content-grid {
            grid-template-columns: 1fr;
          }

          .sidebar-stack {
            position: static;
          }
        }

        @media (max-width: 760px) {
          .examples-grid,
          .stats-grid {
            grid-template-columns: 1fr;
          }

          .messages-pane {
            max-height: none;
            overflow: visible;
          }
        }

        @media (max-width: 640px) {
          .hero-actions {
            width: 100%;
          }

          .hero-actions :global(a) {
            flex: 1 1 100%;
          }
        }

        @media (max-width: 560px) {
          .composer-footer :global(button) {
            width: 100%;
          }
        }
      `}</style>
    </main>
  );
}
