import type { ReactNode } from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import CitationsDraftingPage from "@/app/citations-drafting/page";

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

describe("citations and drafting page", () => {
  it("renders the core educational citation and drafting workspace", () => {
    render(<CitationsDraftingPage />);

    expect(
      screen.getByRole("heading", { name: "Citation and drafting resources" }),
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search statutes, sections, templates, petitions, affidavits..."),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Statute title format")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Before submission checklist")[0]).toBeInTheDocument();
    expect(screen.getByText("Research utilities")).toBeInTheDocument();
    expect(screen.getByText("Related records")).toBeInTheDocument();
  });

  it("filters citation and drafting resources with structured controls", () => {
    render(<CitationsDraftingPage />);

    fireEvent.click(screen.getByRole("button", { name: "More filters" }));
    fireEvent.change(screen.getAllByLabelText("Citation type")[0], {
      target: { value: "case-citation" },
    });

    expect(screen.getAllByText("Case citation format")[0]).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Notice structure/ })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Reset filters" }));
    fireEvent.change(screen.getAllByLabelText("Checklist stage")[0], {
      target: { value: "review" },
    });

    expect(screen.getAllByText("Citation cleanup checklist")[0]).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Affidavit basic format guidance/ })).not.toBeInTheDocument();
  });

  it("saves and removes the selected drafting resource", () => {
    render(<CitationsDraftingPage />);

    fireEvent.click(screen.getByRole("button", { name: "Save Statute title format" }));

    expect(window.localStorage.getItem("law-ai-saved-items-v1")).toContain("Statute title format");
    expect(screen.getByRole("button", { name: "Remove saved Statute title format" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Remove saved Statute title format" }));

    expect(window.localStorage.getItem("law-ai-saved-items-v1")).toBe("[]");
  });

  it("compares the selected resource with another resource", () => {
    render(<CitationsDraftingPage />);

    fireEvent.click(screen.getByText("Compare and related resources"));
    fireEvent.change(screen.getByLabelText("Compare with"), {
      target: { value: "crpc-154-section" },
    });

    expect(screen.getByText("Side-by-side comparison")).toBeInTheDocument();
    expect(screen.getAllByText("Section reference format")[0]).toBeInTheDocument();
  });
});
