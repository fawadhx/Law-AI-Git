import type { ReactNode } from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import HomePage from "@/app/page";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

describe("homepage", () => {
  it("renders the core public legal-information content", () => {
    render(<HomePage />);

    expect(
      screen.getByRole("heading", { name: "Legal Transparency for Every Citizen." }),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Open Legal Chat" })).toHaveAttribute("href", "/chat");
    expect(screen.getByRole("link", { name: "View Admin Prototype" })).toHaveAttribute("href", "/admin");
    expect(screen.getByText(/LEGAL INFORMATION ONLY:/i)).toBeInTheDocument();
  });
});
