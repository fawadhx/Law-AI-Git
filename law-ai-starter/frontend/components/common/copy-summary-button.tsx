"use client";

import { useState } from "react";
import { copyTextToClipboard } from "@/lib/research-utils";

type CopySummaryButtonProps = {
  text: string;
  label?: string;
};

export function CopySummaryButton({ text, label = "Copy summary" }: CopySummaryButtonProps) {
  const [status, setStatus] = useState<"idle" | "copied" | "failed">("idle");

  async function handleCopy() {
    const copied = await copyTextToClipboard(text);
    setStatus(copied ? "copied" : "failed");
    window.setTimeout(() => setStatus("idle"), 1800);
  }

  const statusLabel = status === "copied" ? "Copied" : status === "failed" ? "Copy failed" : label;

  return (
    <button type="button" className="research-button" onClick={() => void handleCopy()}>
      {statusLabel}
    </button>
  );
}
