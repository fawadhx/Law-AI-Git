import type { ReactNode } from "react";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import OfficerAuthorityPage from "@/app/officer-authority/page";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

afterEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
  cleanup();
});

describe("officer authority page", () => {
  it("keeps rank lookup visible and filters rank discovery helpers", () => {
    render(<OfficerAuthorityPage />);

    expect(screen.getByRole("heading", { name: "Rank authority lookup" })).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter rank, for example sho")).toBeInTheDocument();

    fireEvent.change(screen.getByPlaceholderText("Search rank, FIR, arrest, investigation..."), {
      target: { value: "arrest" },
    });

    expect(screen.getByRole("button", { name: /ASI/i })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Reset" }));
    fireEvent.change(screen.getByLabelText("Authority theme"), {
      target: { value: "supervision" },
    });

    expect(screen.getByRole("button", { name: /Inspector/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /SHO/i })).not.toBeInTheDocument();
  });

  it("allows saving a loaded authority result", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({
        rank: "SHO",
        summary: "Station-level authority summary.",
        powers: ["Register and process complaints"],
        limitations: ["Must follow procedure"],
      }),
    } as Response);

    render(<OfficerAuthorityPage />);

    fireEvent.click(screen.getByRole("button", { name: "Check authority" }));

    const saveButton = await screen.findByRole("button", { name: "Save SHO authority details" });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(window.localStorage.getItem("law-ai-saved-items-v1")).toContain("SHO authority details");
    });
  });
});
