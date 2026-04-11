"use client";

type ChatInputProps = {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
};

export function ChatInput({ value, onChange, onSubmit, loading }: ChatInputProps) {
  return (
    <div className="card chat-input-wrap">
      <div>
        <div className="label">Ask a legal information question</div>
        <textarea
          className="chat-textarea"
          placeholder="Example: What laws may apply if someone threatens me online, and what punishments can overlap?"
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
      </div>

      <button className="button-primary" onClick={onSubmit} disabled={loading || !value.trim()}>
        {loading ? "Thinking..." : "Ask question"}
      </button>

      <p className="footer-note">
        The assistant should provide legal information with citations. It should not present itself as a lawyer.
      </p>
    </div>
  );
}
