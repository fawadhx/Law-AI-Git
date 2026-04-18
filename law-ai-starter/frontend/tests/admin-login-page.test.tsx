import type { ReactNode } from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import AdminLoginPage from "@/app/admin/login/page";

const replace = vi.fn();

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace }),
  useSearchParams: () => new URLSearchParams("next=%2Fadmin"),
}));

vi.mock("@/lib/admin-auth", () => ({
  clearAdminToken: vi.fn(),
  fetchAdminMe: vi.fn(),
  getStoredAdminToken: vi.fn(() => null),
  loginAdmin: vi.fn(),
  storeAdminToken: vi.fn(),
}));

describe("admin login page", () => {
  it("renders the protected admin login gate", async () => {
    render(<AdminLoginPage />);

    await waitFor(() =>
      expect(screen.getByRole("heading", { name: "Admin Login" })).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: "Sign In" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Back to Homepage" })).toHaveAttribute("href", "/");
  });
});
