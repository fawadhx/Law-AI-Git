import type { ReactNode } from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import CaseStudiesPage from "@/app/case-studies/page";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

describe("case studies page", () => {
  it("renders the case research workspace and sample record metadata", () => {
    render(<CaseStudiesPage />);

    expect(screen.getByRole("heading", { name: "Case research and order summaries" })).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search case title, court, citation, bench, or linked law..."),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Illustrative bail order study")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Lahore High Court")[0]).toBeInTheDocument();
  });
});
