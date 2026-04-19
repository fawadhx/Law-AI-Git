"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import type { FormEvent, ReactNode } from "react";
import { CopySummaryButton } from "@/components/common/copy-summary-button";
import { SaveButton } from "@/components/common/save-button";
import { API_BASE_URL } from "@/lib/runtime-config";
import { formatResearchSummary } from "@/lib/research-utils";
import { createStableHash, type SavedItem } from "@/lib/saved-items";
import styles from "./page.module.css";

type Citation = {
  title: string;
  section: string;
  note: string;
  excerpt: string;
  source_url?: string | null;
  provenance?: string | null;
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

const INITIAL_ASSISTANT_MESSAGE =
  "Ask a question to receive a structured answer with confidence cues and source references where available.";

const EXAMPLE_GROUPS = [
  {
    title: "Police & Procedure",
    examples: [
      "Can police detain a person for more than 24 hours?",
      "What happens when an FIR is registered?",
    ],
  },
  {
    title: "Tenancy & Housing",
    examples: [
      "What rights does a tenant have in a rent dispute?",
      "Can a landlord evict a tenant without notice?",
    ],
  },
  {
    title: "Employment & Wages",
    examples: [
      "What can I do if salary is not paid on time?",
      "What workplace issues may become a labor complaint?",
    ],
  },
  {
    title: "Digital Harm & Complaints",
    examples: [
      "Someone is threatening me online. What laws may be relevant?",
      "What legal issues can arise from sharing private content online?",
    ],
  },
];

function getConfidenceTone(level?: string) {
  if (level === "high") return styles.confidenceHigh;
  if (level === "medium") return styles.confidenceMedium;
  return styles.confidenceLow;
}

function getConfidenceLabel(level?: string) {
  if (level === "high") return "Strong match";
  if (level === "medium") return "Reasonable match";
  return "Tentative match";
}

function getConfidenceDescription(confidence?: ChatConfidence) {
  if (!confidence) {
    return "Ask a question to see category, confidence, and source coverage information.";
  }

  if (confidence.level === "high") {
    return "The current legal-source dataset found a comparatively strong match for this question.";
  }

  if (confidence.level === "medium") {
    return "The response appears usable, but it should still be read carefully against the cited material.";
  }

  return "Only a limited match was found. This answer should be treated with extra caution.";
}

function formatScore(score?: number): string {
  if (typeof score !== "number" || Number.isNaN(score)) return "--";
  return score.toFixed(1);
}

function getShortExcerpt(text?: string, maxLength: number = 180): string {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength).trim()}...`;
}

async function readApiError(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.clone().json();
    if (payload && typeof payload.detail === "string" && payload.detail.trim()) {
      const boundaryNote =
        typeof payload.boundary_note === "string" && payload.boundary_note.trim()
          ? ` ${payload.boundary_note.trim()}`
          : "";
      return `${payload.detail.trim()}${boundaryNote}`.trim();
    }
  } catch {
    // Ignore parse failure and fall back to text/default handling.
  }

  try {
    const text = (await response.text()).trim();
    if (text) return text;
  } catch {
    // Ignore text failure and use fallback.
  }

  return fallback;
}

function SurfacePill({
  children,
  tone = "default",
}: {
  children: ReactNode;
  tone?: "default" | "muted" | "accent";
}) {
  const className =
    tone === "accent"
      ? `${styles.pill} ${styles.pillAccent}`
      : tone === "muted"
        ? `${styles.pill} ${styles.pillMuted}`
        : styles.pill;

  return <span className={className}>{children}</span>;
}

function MessageBubble({ message }: { message: Message }) {
  const assistant = message.role === "assistant";

  return (
    <article
      className={assistant ? styles.assistantBubble : styles.userBubble}
      aria-label={assistant ? "Assistant message" : "User message"}
    >
      <div className={styles.messageMeta}>
        <span className={styles.messageRole}>{assistant ? "Law AI" : "You"}</span>
        {assistant && (message.category || message.confidence) ? (
          <div className={styles.messagePills}>
            {message.category ? <SurfacePill>{message.category.label}</SurfacePill> : null}
            {message.confidence ? (
              <span className={`${styles.confidencePill} ${getConfidenceTone(message.confidence.level)}`}>
                {getConfidenceLabel(message.confidence.level)}
              </span>
            ) : null}
          </div>
        ) : null}
      </div>

      <div className={styles.messageContent}>{message.content}</div>
    </article>
  );
}

function LoadingBubble() {
  return (
    <div className={styles.loadingBubble}>
      <div className={styles.messageRole}>Law AI</div>
      <div className={styles.loadingRow}>
        <span>Searching structured legal records</span>
        <span className={styles.typingDot} />
        <span className={styles.typingDot} />
        <span className={styles.typingDot} />
      </div>
    </div>
  );
}

function EmptyConversationState({ onApply }: { onApply: (example: string) => void }) {
  const starterExamples = EXAMPLE_GROUPS.flatMap((group) => group.examples).slice(0, 4);

  return (
    <div className={styles.emptyState}>
      <div className={styles.emptyEyebrow}>Start here</div>
      <h2>Ask a focused legal-information question</h2>
      <p>
        Clearer questions usually mention the issue, procedure, or interaction involved, such as
        FIR registration, detention time, tenancy disputes, or salary non-payment.
      </p>

      <div className={styles.exampleChipRow}>
        {starterExamples.map((example) => (
          <button key={example} type="button" className={styles.exampleChip} onClick={() => onApply(example)}>
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}

export default function ChatPage() {
  const searchParams = useSearchParams();
  const seededQuestion = searchParams.get("q") || "";

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: INITIAL_ASSISTANT_MESSAGE,
    },
  ]);
  const [latestResponse, setLatestResponse] = useState<ChatQueryResponse | null>(null);
  const [latestQuestion, setLatestQuestion] = useState("");

  const messagesPaneRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!seededQuestion.trim()) return;
    setQuestion((current) => (current.trim() ? current : seededQuestion));
  }, [seededQuestion]);

  useEffect(() => {
    const pane = messagesPaneRef.current;
    if (!pane) return;
    if (typeof pane.scrollTo !== "function") return;
    pane.scrollTo({ top: pane.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const assistantCount = useMemo(
    () => messages.filter((message) => message.role === "assistant").length,
    [messages],
  );

  const hasAskedQuestion = useMemo(
    () => messages.some((message) => message.role === "user"),
    [messages],
  );

  const latestWarnings = useMemo(() => {
    if (!latestResponse) return [];

    const warnings: string[] = [];
    if (latestResponse.confidence.level === "low") {
      warnings.push(
        "The current result is only a tentative match. Review the cited legal material before relying on it.",
      );
    }
    if (latestResponse.citations.length === 0) {
      warnings.push(
        "No source references were returned with this answer, so it should be treated as informational guidance only.",
      );
    }
    return warnings;
  }, [latestResponse]);

  const questionLength = question.trim().length;

  const savedChatItem = useMemo<SavedItem | null>(() => {
    if (!latestResponse || !latestQuestion.trim()) return null;
    const sourceId = createStableHash(`${latestQuestion}\n${latestResponse.answer}`);
    return {
      id: `chat:${sourceId}`,
      type: "chat",
      title: latestQuestion,
      subtitle: latestResponse.category.label,
      summary: getShortExcerpt(latestResponse.answer, 220),
      href: `/chat?q=${encodeURIComponent(latestQuestion)}`,
      tags: [
        latestResponse.category.label,
        latestResponse.confidence.level,
        `${latestResponse.citations.length} references`,
      ],
      metadata: {
        category: latestResponse.category.label,
        confidence: latestResponse.confidence.level,
        citationCount: latestResponse.citations.length,
        score: latestResponse.confidence.score,
      },
      sourceId,
      savedAt: new Date().toISOString(),
    };
  }, [latestQuestion, latestResponse]);

  const latestCopyText = useMemo(() => {
    if (!latestResponse || !latestQuestion.trim()) return "";
    return formatResearchSummary({
      title: latestQuestion,
      subtitle: "Law AI chat result",
      summary: getShortExcerpt(latestResponse.answer, 500),
      fields: [
        ["Category", latestResponse.category.label],
        ["Confidence", latestResponse.confidence.level],
        ["Matched records", latestResponse.confidence.matched_records],
        ["Citation titles", latestResponse.citations.map((citation) => citation.title).join(", ")],
      ],
      tags: [latestResponse.category.label, latestResponse.confidence.level],
    });
  }, [latestQuestion, latestResponse]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || loading) return;

    setLoading(true);
    setError("");
    setLatestResponse(null);

    setMessages((previous) => [...previous, { role: "user", content: trimmedQuestion }]);

    try {
      let response: Response;
      try {
        response = await fetch(`${API_BASE_URL}/api/v1/chat/query`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question: trimmedQuestion }),
        });
      } catch {
        throw new Error(
          "The legal-information service could not be reached right now. Please try again in a moment.",
        );
      }

      if (!response.ok) {
        throw new Error(
          await readApiError(
            response,
            "This legal-information request could not be completed safely right now.",
          ),
        );
      }

      const result: ChatQueryResponse = await response.json();

      setLatestResponse(result);
      setLatestQuestion(trimmedQuestion);
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          category: result.category,
          confidence: result.confidence,
        },
      ]);
      setQuestion("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch response.");
    } finally {
      setLoading(false);
    }
  }

  function clearConversation() {
    setMessages([
      {
        role: "assistant",
        content: INITIAL_ASSISTANT_MESSAGE,
      },
    ]);
    setLatestResponse(null);
    setLatestQuestion("");
    setError("");
    setQuestion(seededQuestion);
  }

  function applyExample(example: string) {
    setQuestion(example);
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.workspace}>
            <div className={styles.workspaceTopBar}>
              <div>
                <div className={styles.sectionEyebrow}>Law AI chat</div>
                <p className={styles.workspaceIntro}>
                  Ask a question, then review matched records and confidence in the same workspace.
                </p>
              </div>
            </div>

            <div className={styles.workspaceHeader}>
              <div>
                <h2>Conversation</h2>
              </div>
              <div className={styles.workspaceTools}>
                <SurfacePill tone="muted">Messages: {messages.length}</SurfacePill>
                <SurfacePill tone="muted">Assistant replies: {assistantCount}</SurfacePill>
                {latestResponse?.category ? <SurfacePill>{latestResponse.category.label}</SurfacePill> : null}
                {hasAskedQuestion ? (
                  <button type="button" className={styles.ghostButton} onClick={clearConversation}>
                    Clear chat
                  </button>
                ) : null}
              </div>
            </div>

            <form onSubmit={handleSubmit} className={styles.composer}>
              <div className={styles.composerHeader}>
                <label htmlFor="question" className={styles.composerLabel}>
                  Your question
                </label>
                <span className={styles.composerHint}>Specific questions usually match better.</span>
              </div>

              <textarea
                id="question"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Example: Can police detain a person for more than 24 hours?"
                rows={5}
                className={styles.composerInput}
              />

              <div className={styles.composerFooter}>
                <div className={styles.composerActions}>
                  <button type="submit" disabled={loading || !question.trim()} className={styles.primaryButton}>
                    {loading ? "Thinking..." : "Ask Question"}
                  </button>
                </div>
                <span className={styles.characterCount}>
                  {questionLength > 0 ? `${questionLength} characters` : "Question box ready"}
                </span>
              </div>

              {error ? <div className={styles.errorBanner}>Unable to complete request: {error}</div> : null}
            </form>

            <div ref={messagesPaneRef} className={styles.messagesPane}>
              {!hasAskedQuestion ? <EmptyConversationState onApply={applyExample} /> : null}
              {messages.map((message, index) => (
                <MessageBubble key={`${message.role}-${index}`} message={message} />
              ))}
              {loading ? <LoadingBubble /> : null}
            </div>

            <details className={styles.examplesSection}>
              <summary>
                <span>Quick prompts</span>
                <small>Use an example if you are not sure how to start.</small>
              </summary>
              <div className={styles.examplesGrid}>
                {EXAMPLE_GROUPS.map((group) => (
                  <div key={group.title} className={styles.exampleCard}>
                    <h3>{group.title}</h3>
                    <div className={styles.exampleChipRow}>
                      {group.examples.map((example) => (
                        <button
                          key={example}
                          type="button"
                          className={styles.exampleChip}
                          onClick={() => applyExample(example)}
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </details>
          </section>

          <aside className={styles.sidebar}>
            <section className={styles.sidebarCard}>
              <div className={styles.sidebarCardHeader}>
                <div className={styles.sectionEyebrow}>Current result</div>
                <div className={styles.utilityActions}>
                  {latestCopyText ? <CopySummaryButton text={latestCopyText} /> : null}
                  <SaveButton item={savedChatItem} />
                </div>
              </div>
              <h3>Category and confidence</h3>
              <div className={styles.statGrid}>
                <div className={styles.statCard}>
                  <span className={styles.statLabel}>Category</span>
                  <strong>{latestResponse?.category?.label || "No category yet"}</strong>
                  <span>{latestResponse ? latestResponse.category.key : "Waiting for a question"}</span>
                </div>
                <div className={styles.statCard}>
                  <span className={styles.statLabel}>Top score</span>
                  <strong>{formatScore(latestResponse?.confidence?.score)}</strong>
                  <span>{latestResponse?.confidence?.matched_records ?? "--"} matched records</span>
                </div>
              </div>

              {latestResponse?.confidence ? (
                <div className={`${styles.confidencePanel} ${getConfidenceTone(latestResponse.confidence.level)}`}>
                  <div className={styles.confidenceTitle}>{getConfidenceLabel(latestResponse.confidence.level)}</div>
                  <p>{getConfidenceDescription(latestResponse.confidence)}</p>
                </div>
              ) : (
                <p className={styles.panelText}>{getConfidenceDescription()}</p>
              )}

              {latestWarnings.length > 0 ? (
                <div className={styles.warningPanel}>
                  <div className={styles.warningTitle}>Caution</div>
                  <div className={styles.warningList}>
                    {latestWarnings.map((warning) => (
                      <div key={warning}>{warning}</div>
                    ))}
                  </div>
                </div>
              ) : null}
            </section>

            <section className={styles.sidebarCard}>
              <div className={styles.sectionEyebrow}>Matched legal records</div>
              <h3>References and excerpts</h3>
              {latestResponse?.citations?.length ? (
                <div className={styles.citationList}>
                  {latestResponse.citations.map((citation, index) => (
                    <article key={`${citation.title}-${index}`} className={styles.citationCard}>
                      <div className={styles.citationHeader}>
                        <SurfacePill tone="muted">Match #{index + 1}</SurfacePill>
                        {citation.provenance ? <SurfacePill>{citation.provenance}</SurfacePill> : null}
                      </div>
                      <h4>{citation.section}</h4>
                      <div className={styles.citationTitle}>{citation.title}</div>
                      <p className={styles.panelText}>{citation.note}</p>
                      {citation.excerpt ? (
                        <div className={styles.excerptBox}>&quot;{getShortExcerpt(citation.excerpt)}&quot;</div>
                      ) : null}
                      {citation.source_url ? (
                        <a href={citation.source_url} target="_blank" rel="noreferrer" className={styles.inlineLink}>
                          Open source link
                        </a>
                      ) : null}
                    </article>
                  ))}
                </div>
              ) : (
                <p className={styles.panelText}>
                  Ask a question to see matched provisions, excerpts, and source references.
                </p>
              )}
            </section>

            <section className={styles.sidebarCard}>
              <div className={styles.sectionEyebrow}>Why this matched</div>
              <h3>Backend match explanation</h3>
              {latestResponse?.why_matched?.length ? (
                <div className={styles.matchList}>
                  {latestResponse.why_matched.map((item, index) => (
                    <article key={`${item.title}-${index}`} className={styles.matchCard}>
                      <h4>{item.title}</h4>
                      <div className={styles.matchPoints}>
                        {item.points.map((point, pointIndex) => (
                          <div key={`${item.title}-${pointIndex}`}>{point}</div>
                        ))}
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <p className={styles.panelText}>
                  After you ask a question, this panel shows the signals that likely influenced the current match.
                </p>
              )}
            </section>
          </aside>
        </div>
      </div>
    </main>
  );
}
