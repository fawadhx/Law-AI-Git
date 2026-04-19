import type { ReactNode } from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import CitationsDraftingPage from "@/app/citations-drafting/page";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

describe("citations and drafting page", () => {
  it("renders the core educational citation and drafting workspace", () => {
    render(<CitationsDraftingPage />);

    expect(
      screen.getByRole("heading", { name: "Citation lookup and drafting guidance" }),
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search statutes, sections, templates, petitions, affidavits..."),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Statute title format")[0]).toBeInTheDocument();
    expect(screen.getByText("Before submission checklist")).toBeInTheDocument();
  });
});
