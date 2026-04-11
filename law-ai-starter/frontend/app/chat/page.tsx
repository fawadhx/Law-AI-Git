"use client";

import { useState } from "react";
import Link from "next/link";
import { askLawQuestion } from "@/lib/api";
import type { ChatMessage, Citation } from "@/types/chat";

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

const suggestionButton: React.CSSProperties = {
  background: "rgba(126, 162, 255, 0.08)",
  color: "#dfe7ff",
  border: "1px solid rgba(126, 162, 255, 0.18)",
  borderRadius: "999px",
  padding: "10px 14px",
  fontSize: "14px",
  cursor: "pointer",
};

const examples = [
  "What are my rights if a police officer stops me for questioning?",
  "If someone threatens me online, what laws may apply?",
  "What punishment may apply for theft under basic criminal law?",
  "Which legal provisions can overlap in a harassment case?",
];

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [disclaimer, setDisclaimer] = useState(
    "This system is intended for legal information and public awareness only. It should not be treated as a substitute for professional legal advice or representation.",
  );
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-assistant",
      role: "assistant",
      content:
        "Welcome to Law AI. Ask a legal-information question and the system will return a structured response with citation blocks.",
    },
  ]);

  async function handleSubmit() {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmed,
    };

    setMessages((current) => [...current, userMessage]);
    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const response = await askLawQuestion(trimmed);

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: response.answer,
      };

      setMessages((current) => [...current, assistantMessage]);
      setCitations(response.citations || []);
      setDisclaimer(
        response.disclaimer ||
          "This system is intended for legal information and public awareness only.",
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch legal response.");
    } finally {
      setLoading(false);
    }
  }

  function handleExampleClick(example: string) {
    setQuestion(example);
    setError("");
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSubmit();
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
              Public legal-information chat
            </div>

            <h1
              style={{
                fontSize: "44px",
                lineHeight: 1.08,
                letterSpacing: "-1px",
                margin: "0 0 10px",
              }}
            >
              Legal Information Chat
            </h1>

            <p
              style={{
                margin: 0,
                maxWidth: "780px",
                color: "#c8d6f7",
                fontSize: "18px",
                lineHeight: 1.65,
              }}
            >
              Ask a question about rights, punishments, public-officer authority,
              or overlapping legal provisions. The product should explain clearly,
              cite relevant sections, and avoid presenting itself as a lawyer.
            </p>
          </div>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <Link href="/" style={secondaryButton}>
              Back to Homepage
            </Link>
            <Link href="/admin" style={secondaryButton}>
              Admin
            </Link>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.15fr 0.85fr",
            gap: "24px",
            alignItems: "start",
          }}
        >
          <section style={{ ...cardStyle, padding: "24px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "12px",
                marginBottom: "18px",
                flexWrap: "wrap",
              }}
            >
              <div>
                <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "6px" }}>
                  Conversation
                </div>
                <div style={{ fontSize: "22px", fontWeight: 700 }}>Chat history</div>
              </div>

              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "8px",
                  borderRadius: "999px",
                  padding: "8px 12px",
                  background: loading
                    ? "rgba(255, 196, 90, 0.12)"
                    : "rgba(126, 162, 255, 0.12)",
                  border: loading
                    ? "1px solid rgba(255, 196, 90, 0.22)"
                    : "1px solid rgba(126, 162, 255, 0.22)",
                  color: loading ? "#ffd37c" : "#b9caff",
                  fontSize: "13px",
                  fontWeight: 600,
                }}
              >
                <span
                  style={{
                    width: "8px",
                    height: "8px",
                    borderRadius: "999px",
                    background: loading ? "#ffd37c" : "#7ea2ff",
                    display: "inline-block",
                  }}
                />
                {loading ? "Generating response..." : "Ready"}
              </div>
            </div>

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "16px",
                maxHeight: "760px",
                overflowY: "auto",
                paddingRight: "4px",
              }}
            >
              {messages.map((message) => {
                const isUser = message.role === "user";

                return (
                  <div
                    key={message.id}
                    style={{
                      alignSelf: isUser ? "flex-end" : "flex-start",
                      width: isUser ? "78%" : "100%",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "12px",
                        fontWeight: 700,
                        letterSpacing: "1px",
                        textTransform: "uppercase",
                        color: isUser ? "#a9c1ff" : "#d5def7",
                        marginBottom: "8px",
                      }}
                    >
                      {isUser ? "User" : "Assistant"}
                    </div>

                    <div
                      style={{
                        background: isUser
                          ? "linear-gradient(180deg, rgba(43, 70, 150, 0.72), rgba(28, 46, 102, 0.82))"
                          : "rgba(11, 20, 45, 0.95)",
                        border: isUser
                          ? "1px solid rgba(126, 162, 255, 0.22)"
                          : "1px solid rgba(132, 151, 220, 0.16)",
                        borderRadius: "18px",
                        padding: "18px 18px",
                        color: "#f3f6ff",
                        lineHeight: 1.65,
                        fontSize: "17px",
                        whiteSpace: "pre-wrap",
                      }}
                    >
                      {message.content}
                    </div>
                  </div>
                );
              })}

              {loading && (
                <div style={{ width: "100%" }}>
                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: 700,
                      letterSpacing: "1px",
                      textTransform: "uppercase",
                      color: "#d5def7",
                      marginBottom: "8px",
                    }}
                  >
                    Assistant
                  </div>

                  <div
                    style={{
                      background: "rgba(11, 20, 45, 0.95)",
                      border: "1px solid rgba(132, 151, 220, 0.16)",
                      borderRadius: "18px",
                      padding: "18px",
                      color: "#d2dcfb",
                    }}
                  >
                    Thinking about the most relevant legal-information response...
                  </div>
                </div>
              )}
            </div>
          </section>

          <aside style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
            <section style={{ ...cardStyle, padding: "22px" }}>
              <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
                Ask a question
              </div>
              <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "16px" }}>
                Describe the legal issue clearly
              </div>

              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Example: What are my rights if a police officer stops me for questioning, and what should I understand about their authority?"
                style={{
                  width: "100%",
                  minHeight: "180px",
                  resize: "vertical",
                  padding: "16px",
                  borderRadius: "16px",
                  background: "rgba(8, 18, 39, 0.86)",
                  border: "1px solid rgba(132, 151, 220, 0.18)",
                  color: "#f4f7ff",
                  outline: "none",
                  fontSize: "16px",
                  lineHeight: 1.6,
                  marginBottom: "14px",
                }}
              />

              <button
                onClick={() => void handleSubmit()}
                disabled={loading || !question.trim()}
                style={{
                  ...primaryButton,
                  width: "100%",
                  opacity: loading || !question.trim() ? 0.65 : 1,
                  cursor: loading || !question.trim() ? "not-allowed" : "pointer",
                }}
              >
                {loading ? "Generating response..." : "Ask question"}
              </button>

              <p
                style={{
                  color: "#c6d3f3",
                  lineHeight: 1.6,
                  fontSize: "14px",
                  marginTop: "14px",
                  marginBottom: 0,
                }}
              >
                Press <strong>Enter</strong> to submit, or use <strong>Shift + Enter</strong> for a new line.
              </p>
            </section>

            <section style={{ ...cardStyle, padding: "22px" }}>
              <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "12px" }}>
                Quick examples
              </div>

              <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                {examples.map((example) => (
                  <button
                    key={example}
                    onClick={() => handleExampleClick(example)}
                    style={suggestionButton}
                  >
                    {example}
                  </button>
                ))}
              </div>
            </section>

            {error && (
              <section
                style={{
                  ...cardStyle,
                  padding: "18px",
                  background: "rgba(58, 18, 32, 0.75)",
                  border: "1px solid rgba(255, 118, 145, 0.24)",
                }}
              >
                <div style={{ fontWeight: 700, marginBottom: "8px", color: "#ffd2db" }}>
                  Request error
                </div>
                <div style={{ color: "#ffe7ec", lineHeight: 1.6 }}>{error}</div>
              </section>
            )}

            <section style={{ ...cardStyle, padding: "22px" }}>
              <div style={{ fontSize: "14px", color: "#b9caff", marginBottom: "8px" }}>
                Answer support
              </div>
              <div style={{ fontSize: "24px", fontWeight: 700, marginBottom: "16px" }}>
                Citation panel
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                {citations.length === 0 ? (
                  <div
                    style={{
                      background: "rgba(10, 19, 43, 0.95)",
                      border: "1px solid rgba(132, 151, 220, 0.14)",
                      borderRadius: "16px",
                      padding: "16px",
                      color: "#c6d3f3",
                      lineHeight: 1.6,
                    }}
                  >
                    Citation records will appear here after the assistant returns a response.
                  </div>
                ) : (
                  citations.map((citation, index) => (
                    <div
                      key={`${citation.title}-${index}`}
                      style={{
                        background: "rgba(10, 19, 43, 0.95)",
                        border: "1px solid rgba(132, 151, 220, 0.14)",
                        borderRadius: "16px",
                        padding: "16px",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "20px",
                          fontWeight: 700,
                          marginBottom: "8px",
                          color: "#ffffff",
                        }}
                      >
                        {citation.title}
                      </div>
                      <div
                        style={{
                          color: "#b9caff",
                          fontSize: "14px",
                          marginBottom: "8px",
                        }}
                      >
                        Section: {citation.section}
                      </div>
                      <div style={{ color: "#dbe4ff", lineHeight: 1.6 }}>{citation.note}</div>
                    </div>
                  ))
                )}
              </div>
            </section>

            <section
              style={{
                ...cardStyle,
                padding: "20px",
                background: "linear-gradient(180deg, rgba(58, 22, 32, 0.75), rgba(45, 18, 26, 0.78))",
                border: "1px solid rgba(255, 150, 170, 0.18)",
              }}
            >
              <div style={{ fontSize: "15px", fontWeight: 700, marginBottom: "10px" }}>
                Important legal boundary
              </div>
              <div style={{ color: "#ffe7ec", lineHeight: 1.7, fontSize: "15px" }}>
                {disclaimer}
              </div>
            </section>
          </aside>
        </div>
      </div>
    </main>
  );
}