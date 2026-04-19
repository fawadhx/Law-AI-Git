import type { ReactNode } from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import CaseStudiesPage from "@/app/case-studies/page";

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

describe("case studies page", () => {
  it("renders the case research workspace and sample record metadata", () => {
    render(<CaseStudiesPage />);

    expect(screen.getByRole("heading", { name: "Case and order research" })).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search case title, court, citation, bench, or linked law..."),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Illustrative bail order study")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Lahore High Court")[0]).toBeInTheDocument();
  });

  it("filters case records by court, issue, and linked-law type", () => {
    render(<CaseStudiesPage />);

    fireEvent.change(screen.getAllByLabelText("Court")[0], {
      target: { value: "Islamabad High Court" },
    });

    expect(screen.getAllByText("Illustrative constitutional petition order")[0]).toBeInTheDocument();
    expect(screen.getByText("1 case record")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Reset filters" }));
    fireEvent.change(screen.getAllByLabelText("Legal issue")[0], {
      target: { value: "Departmental record" },
    });

    expect(screen.getAllByText("Illustrative service matter order")[0]).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "More filters" }));
    fireEvent.change(screen.getAllByLabelText("Linked-law type")[0], {
      target: { value: "rules" },
    });

    expect(screen.getAllByText("Illustrative service matter order")[0]).toBeInTheDocument();
    expect(screen.getByText("1 case record")).toBeInTheDocument();
  });

  it("saves the selected case record", () => {
    render(<CaseStudiesPage />);

    fireEvent.click(screen.getByRole("button", { name: "Save Illustrative bail order study" }));

    expect(window.localStorage.getItem("law-ai-saved-items-v1")).toContain("Illustrative bail order study");
    expect(screen.getByRole("button", { name: "Remove saved Illustrative bail order study" })).toBeInTheDocument();
  });

  it("renders comparison and related case utilities", () => {
    render(<CaseStudiesPage />);

    expect(screen.getByText("Research utilities")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Compare and related records"));
    expect(screen.getByText("Related records")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Compare with"), {
      target: { value: "islamabad-constitutional-order" },
    });

    expect(screen.getByText("Side-by-side comparison")).toBeInTheDocument();
    expect(screen.getAllByText("Illustrative constitutional petition order")[0]).toBeInTheDocument();
  });
});
