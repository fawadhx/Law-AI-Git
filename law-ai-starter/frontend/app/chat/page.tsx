"use client";

import Link from "next/link";
import { useState } from "react";
import type { CSSProperties, FormEvent } from "react";

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
  padding: "28px 0 52px",
};

const containerStyle: CSSProperties = {
  maxWidth: "1320px",
  margin: "0 auto",
  padding: "0 20px",
};

const cardStyle: CSSProperties = {
  background: "rgba(18, 28, 58, 0.92)",
  border: "1px solid rgba(120, 150, 255, 0.16)",
  borderRadius: "22px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.22)",
};

const sectionLabelStyle: CSSProperties = {
  fontSize: "12px",
  color: "#b9caff",
  marginBottom: "8px",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.65px",
};

const sectionTitleStyle: CSSProperties = {
  fontSize: "20px",
  fontWeight: 700,
  marginBottom: "14px",
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
  padding: "14px",
};

const secondaryButton: CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "14px",
  padding: "12px 16px",
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
  fontWeight: 700,
  fontSize: "14px",
  cursor: "pointer",
};

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

function getAnswerStatusConfig(confidence?: ChatConfidence): {
  label: string;
  description: string;
  style: CSSProperties;
} | null {
  if (!confidence) return null;

  if (confidence.level === "high") {
    return {
      label: "Strong match",
      description:
        "The current prototype found a comparatively strong legal-source match.",
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
      description:
        "The current prototype found a reasonable match, but the result should still be read cautiously.",
      style: {
        background: "rgba(250, 204, 21, 0.12)",
        border: "1px solid rgba(250, 204, 21, 0.22)",
        color: "#fef3c7",
      },
    };
  }

  return {
    label: "Tentative match",
    description:
      "The current prototype found only a limited or tentative match, so this result should be treated with extra caution.",
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
    return "The current prototype found a reasonable match, but the result should still be read cautiously.";
  }

  return "The current prototype found only a limited or tentative match, so this result should be treated with extra caution.";
}

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
  const [latestResponse, setLatestResponse] =
    useState<ChatQueryResponse | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || loading) return;

    setLoading(true);
    setError("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: trimmedQuestion },
    ]);

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
      const message =
        err instanceof Error ? err.message : "Failed to fetch response.";
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
                  fontSize: "clamp(30px, 5vw, 42px)",
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
                  maxWidth: "780px",
                  color: "#c8d6f7",
                  fontSize: "16px",
                  lineHeight: 1.7,
                }}
              >
                Ask a legal-information question and the system will try to match
                it against the current structured prototype dataset, return
                supporting citations, classify the issue type, and show match
                confidence.
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
            <section style={{ ...cardStyle, padding: "20px" }}>
              <div className="conversation-header">
                <div>
                  <div style={sectionLabelStyle}>Conversation</div>
                  <div style={{ ...sectionTitleStyle, marginBottom: "6px" }}>
                    Ask a legal-information question
                  </div>
                  <div style={mutedBodyStyle}>
                    The left panel stays focused on the conversation, while the
                    right side shows the current matched result snapshot.
                  </div>
                </div>
              </div>

              <div className="messages-pane">
                {messages.map((message, index) => {
                  const statusConfig =
                    message.role === "assistant"
                      ? getAnswerStatusConfig(message.confidence)
                      : null;

                  return (
                    <div
                      key={`${message.role}-${index}`}
                      style={{
                        alignSelf: message.role === "user" ? "flex-end" : "stretch",
                        maxWidth: message.role === "user" ? "76%" : "100%",
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
                        padding: "14px",
                        overflowWrap: "anywhere",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "12px",
                          fontWeight: 800,
                          letterSpacing: "0.5px",
                          textTransform: "uppercase",
                          color:
                            message.role === "user" ? "#cfe0ff" : "#a9c1ff",
                          marginBottom: "8px",
                        }}
                      >
                        {message.role === "user" ? "You" : "Law AI"}
                      </div>

                      {statusConfig && (
                        <div
                          style={{
                            borderRadius: "14px",
                            padding: "11px 13px",
                            marginBottom: "12px",
                            ...statusConfig.style,
                          }}
                        >
                          <div
                            style={{
                              fontSize: "12px",
                              fontWeight: 800,
                              textTransform: "uppercase",
                              letterSpacing: "0.6px",
                              marginBottom: "6px",
                            }}
                          >
                            {statusConfig.label}
                          </div>
                          <div
                            style={{
                              fontSize: "13px",
                              lineHeight: 1.6,
                            }}
                          >
                            {statusConfig.description}
                          </div>
                        </div>
                      )}

                      {message.role === "assistant" &&
                        (message.category || message.confidence) && (
                          <div
                            style={{
                              display: "flex",
                              gap: "8px",
                              flexWrap: "wrap",
                              marginBottom: "12px",
                            }}
                          >
                            {message.category && (
                              <div
                                style={{
                                  display: "inline-flex",
                                  alignItems: "center",
                                  gap: "8px",
                                  padding: "6px 10px",
                                  borderRadius: "999px",
                                  background: "rgba(126, 162, 255, 0.12)",
                                  border:
                                    "1px solid rgba(126, 162, 255, 0.22)",
                                  color: "#dfe7ff",
                                  fontSize: "12px",
                                  fontWeight: 700,
                                }}
                              >
                                Detected category: {message.category.label}
                              </div>
                            )}

                            {message.confidence && (
                              <div
                                style={{
                                  display: "inline-flex",
                                  alignItems: "center",
                                  gap: "8px",
                                  padding: "6px 10px",
                                  borderRadius: "999px",
                                  fontSize: "12px",
                                  fontWeight: 700,
                                  ...getConfidenceBadgeStyle(
                                    message.confidence.level
                                  ),
                                }}
                              >
                                Confidence: {message.confidence.level.toUpperCase()}
                              </div>
                            )}
                          </div>
                        )}

                      <div
                        style={{
                          whiteSpace: "pre-wrap",
                          color: "#edf2ff",
                          lineHeight: 1.75,
                          fontSize: "14px",
                        }}
                      >
                        {message.content}
                      </div>
                    </div>
                  );
                })}
              </div>

              <form onSubmit={handleSubmit} className="composer-card">
                <label
                  htmlFor="question"
                  style={{
                    display: "block",
                    fontSize: "13px",
                    color: "#b9caff",
                    marginBottom: "10px",
                    fontWeight: 700,
                  }}
                >
                  Your question
                </label>

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
                    minHeight: "122px",
                    marginBottom: "12px",
                  }}
                />

                <div
                  style={{
                    display: "flex",
                    gap: "12px",
                    alignItems: "center",
                    flexWrap: "wrap",
                    marginBottom: error ? "12px" : 0,
                  }}
                >
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

              <div style={{ marginTop: "18px" }}>
                <div style={{ ...sectionLabelStyle, marginBottom: "10px" }}>
                  Quick examples by issue type
                </div>

                <div className="examples-grid">
                  {EXAMPLE_GROUPS.map((group) => (
                    <div key={group.title} style={panelInnerCardStyle}>
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
                        {group.title}
                      </div>

                      <div
                        style={{
                          display: "flex",
                          gap: "8px",
                          flexWrap: "wrap",
                        }}
                      >
                        {group.examples.map((example) => (
                          <button
                            key={example}
                            type="button"
                            onClick={() => applyExample(example)}
                            style={{
                              borderRadius: "999px",
                              padding: "9px 12px",
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
                  ))}
                </div>
              </div>
            </section>

            <aside className="sidebar-stack">
              <section style={{ ...cardStyle, padding: "20px" }}>
                <div style={sectionLabelStyle}>Current result snapshot</div>
                <div style={sectionTitleStyle}>Detected category and confidence</div>

                <div className="snapshot-head">
                  <div>
                    <div
                      style={{
                        fontSize: "22px",
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
                    <div
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        justifyContent: "center",
                        padding: "7px 11px",
                        borderRadius: "999px",
                        fontSize: "12px",
                        fontWeight: 800,
                        whiteSpace: "nowrap",
                        ...getConfidenceBadgeStyle(latestResponse.confidence.level),
                      }}
                    >
                      {latestResponse.confidence.level.toUpperCase()} confidence
                    </div>
                  )}
                </div>

                <div className="stats-grid">
                  <div style={panelInnerCardStyle}>
                    <div style={sectionLabelStyle}>Top match score</div>
                    <div style={{ fontSize: "22px", fontWeight: 800 }}>
                      {latestResponse?.confidence?.score ?? "--"}
                    </div>
                  </div>

                  <div style={panelInnerCardStyle}>
                    <div style={sectionLabelStyle}>Matched records</div>
                    <div style={{ fontSize: "22px", fontWeight: 800 }}>
                      {latestResponse?.confidence?.matched_records ?? "--"}
                    </div>
                  </div>
                </div>

                <div style={{ ...mutedBodyStyle, marginTop: "14px" }}>
                  {getConfidenceDescription(latestResponse?.confidence)}
                </div>

                <div style={{ ...panelInnerCardStyle, marginTop: "14px" }}>
                  <div style={sectionLabelStyle}>Legal boundary</div>
                  <div style={mutedBodyStyle}>
                    {latestResponse?.disclaimer ||
                      "This system is for legal information and public awareness only. It must not be treated as a lawyer or a substitute for legal advice."}
                  </div>
                </div>
              </section>

              <section style={{ ...cardStyle, padding: "20px" }}>
                <div style={sectionLabelStyle}>Why this matched</div>
                <div style={sectionTitleStyle}>Match explanation</div>

                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {latestResponse?.why_matched?.length ? (
                    latestResponse.why_matched.map((item, index) => (
                      <div
                        key={`${item.title}-${index}`}
                        style={panelInnerCardStyle}
                      >
                        <div
                          style={{
                            fontSize: "15px",
                            fontWeight: 700,
                            color: "#ffffff",
                            lineHeight: 1.5,
                            marginBottom: "10px",
                          }}
                        >
                          {item.title}
                        </div>

                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "7px",
                          }}
                        >
                          {item.points.map((point, pointIndex) => (
                            <div
                              key={`${item.title}-${pointIndex}`}
                              style={{
                                color: "#dbe4ff",
                                lineHeight: 1.65,
                                fontSize: "14px",
                              }}
                            >
                              • {point}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div style={{ ...panelInnerCardStyle, color: "#c6d3f3", lineHeight: 1.7 }}>
                      Ask a question to see which keywords, tags, or legal signals
                      likely caused the current match.
                    </div>
                  )}
                </div>
              </section>

              <section style={{ ...cardStyle, padding: "20px" }}>
                <div style={sectionLabelStyle}>Matched legal records</div>
                <div style={sectionTitleStyle}>Top matched provisions</div>

                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  {latestResponse?.citations?.length ? (
                    latestResponse.citations.map((citation, index) => (
                      <div
                        key={`matched-record-${citation.title}-${index}`}
                        style={panelInnerCardStyle}
                      >
                        <div
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            padding: "5px 9px",
                            borderRadius: "999px",
                            background: "rgba(126, 162, 255, 0.10)",
                            border: "1px solid rgba(126, 162, 255, 0.18)",
                            color: "#cfe0ff",
                            fontSize: "11px",
                            fontWeight: 700,
                            marginBottom: "10px",
                          }}
                        >
                          Match #{index + 1}
                        </div>

                        <div
                          style={{
                            fontSize: "15px",
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
                            marginBottom: "10px",
                            lineHeight: 1.55,
                          }}
                        >
                          {citation.title}
                        </div>

                        <div
                          style={{
                            color: "#dbe4ff",
                            lineHeight: 1.65,
                            fontSize: "14px",
                            marginBottom: citation.excerpt ? "10px" : 0,
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
                              padding: "11px 12px",
                            }}
                          >
                            <div
                              style={{
                                fontSize: "11px",
                                fontWeight: 700,
                                textTransform: "uppercase",
                                letterSpacing: "0.6px",
                                color: "#b9caff",
                                marginBottom: "8px",
                              }}
                            >
                              Source excerpt
                            </div>
                            <div
                              style={{
                                color: "#edf2ff",
                                lineHeight: 1.65,
                                fontSize: "13px",
                                fontStyle: "italic",
                              }}
                            >
                              “{getShortExcerpt(citation.excerpt, 180)}”
                            </div>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div style={{ ...panelInnerCardStyle, color: "#c6d3f3", lineHeight: 1.7 }}>
                      Ask a question to see the top matched legal provisions and
                      their source excerpts.
                    </div>
                  )}
                </div>
              </section>
            </aside>
          </div>
        </div>
      </div>

      <style jsx>{`
        .chat-page-shell {
          display: flex;
          flex-direction: column;
          gap: 22px;
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
          grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.85fr);
          gap: 20px;
          align-items: start;
        }

        .conversation-header {
          margin-bottom: 16px;
        }

        .messages-pane {
          display: flex;
          flex-direction: column;
          gap: 12px;
          margin-bottom: 16px;
          max-height: 700px;
          overflow-y: auto;
          padding-right: 4px;
        }

        .composer-card {
          background: rgba(10, 19, 43, 0.78);
          border: 1px solid rgba(132, 151, 220, 0.14);
          border-radius: 18px;
          padding: 14px;
        }

        .examples-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 12px;
        }

        .sidebar-stack {
          display: flex;
          flex-direction: column;
          gap: 20px;
          position: sticky;
          top: 18px;
        }

        .snapshot-head {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 12px;
          flex-wrap: wrap;
          margin-bottom: 14px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 12px;
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

        @media (max-width: 720px) {
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
      `}</style>
    </main>
  );
}
