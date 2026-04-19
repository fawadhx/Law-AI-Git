import type { ReactNode } from "react";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import ChatPage from "@/app/chat/page";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(),
}));

afterEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
  cleanup();
});

describe("chat save action", () => {
  it("allows saving the latest successful chat result", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({
        answer: "Police detention questions usually require checking the procedural record and cited provisions.",
        citations: [
          {
            title: "Code of Criminal Procedure, 1898",
            section: "Section 61",
            note: "Demo citation note",
            excerpt: "A short excerpt",
            source_url: null,
            provenance: "catalog",
          },
        ],
        disclaimer: "",
        category: { key: "criminal_procedure", label: "Criminal procedure" },
        confidence: { level: "medium", score: 4.2, matched_records: 1 },
        why_matched: [{ title: "Procedure match", points: ["Matched detention terms"] }],
      }),
    } as Response);

    render(<ChatPage />);

    fireEvent.change(screen.getByLabelText("Your question"), {
      target: { value: "Can police detain a person for more than 24 hours?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Ask Question" }));

    const saveButton = await screen.findByRole("button", {
      name: "Save Can police detain a person for more than 24 hours?",
    });
    expect(screen.getByRole("button", { name: "Copy summary" })).toBeInTheDocument();
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(window.localStorage.getItem("law-ai-saved-items-v1")).toContain("Criminal procedure");
    });
  });
});
