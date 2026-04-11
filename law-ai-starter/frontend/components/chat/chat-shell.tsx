"use client";

import { useMemo, useState } from "react";
import { askLawQuestion } from "@/lib/api";
import { ChatInput } from "@/components/chat/chat-input";
import { MessageList } from "@/components/chat/message-list";
import type { ChatMessage, Citation } from "@/types/chat";

export function ChatShell() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [disclaimer, setDisclaimer] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "seed-assistant",
      role: "assistant",
      content:
        "Welcome. Ask a legal information question and this starter will return a mock answer with sample citations.",
    },
  ]);

  const hasMessages = useMemo(() => messages.length > 0, [messages]);

  async function handleSubmit() {
    const trimmed = question.trim();
    if (!trimmed) return;

    setLoading(true);
    setError(null);

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmed,
    };

    setMessages((current) => [...current, userMessage]);
    setQuestion("");

    try {
      const response = await askLawQuestion(trimmed);

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: response.answer,
      };

      setMessages((current) => [...current, assistantMessage]);
      setCitations(response.citations);
      setDisclaimer(response.disclaimer);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="section">
      <div className="container chat-layout">
        <div className="card">
          <p className="muted">Public chat prototype</p>
          <h1>Legal Information Chat</h1>
          <p className="muted">
            This scaffold currently uses a mocked backend response so the UI and API structure can be tested first.
          </p>

          {hasMessages && <MessageList messages={messages} />}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <ChatInput value={question} onChange={setQuestion} onSubmit={handleSubmit} loading={loading} />

          {error && <div className="warning-box">{error}</div>}

          <div className="card">
            <h3>Answer citations</h3>
            <div className="citation-list">
              {citations.length === 0 ? (
                <p className="muted">Citations will appear here after a response.</p>
              ) : (
                citations.map((citation, index) => (
                  <div key={`${citation.title}-${index}`} className="citation-item">
                    <strong>{citation.title}</strong>
                    <div className="muted">Section: {citation.section}</div>
                    <div>{citation.note}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="warning-box">
            <strong>Important:</strong> {disclaimer || "This product should provide legal information, not legal advice."}
          </div>
        </div>
      </div>
    </main>
  );
}
