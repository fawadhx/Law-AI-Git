import type { ReactNode } from "react";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import SavedPage from "@/app/saved/page";
import { SAVED_ITEMS_STORAGE_KEY, type SavedItem } from "@/lib/saved-items";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

afterEach(() => {
  window.localStorage.clear();
  cleanup();
});

describe("saved page", () => {
  it("renders an empty state when nothing is saved", () => {
    render(<SavedPage />);

    expect(screen.getByRole("heading", { name: "Saved research items" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Save useful research as you work" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Open Chat" })).toHaveAttribute("href", "/chat");
  });

  it("groups and displays locally saved items", async () => {
    const savedItem: SavedItem = {
      id: "case-study:test-case",
      type: "case-study",
      title: "Saved case order",
      subtitle: "High Court · Final order",
      summary: "A locally saved case research summary.",
      href: "/case-studies",
      tags: ["High Court", "Final order"],
      metadata: { court: "High Court" },
      sourceId: "test-case",
      savedAt: "2026-04-19T10:00:00.000Z",
    };
    window.localStorage.setItem(SAVED_ITEMS_STORAGE_KEY, JSON.stringify([savedItem]));

    render(<SavedPage />);

    await waitFor(() => {
      expect(screen.getByText("Saved case order")).toBeInTheDocument();
    });
    expect(screen.getAllByText("Case studies")[0]).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Open" })).toHaveAttribute("href", "/case-studies");
    expect(screen.getByRole("button", { name: "Copy summary" })).toBeInTheDocument();
  });
});
