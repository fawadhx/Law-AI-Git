import type { ReactNode } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import RootLayout from "@/app/layout";

vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: ReactNode; href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("@/components/layout/theme-toggle", () => ({
  ThemeToggle: () => <button type="button">Toggle theme</button>,
}));

describe("public shell", () => {
  it("renders the shared navigation links for the new public pages", () => {
    const markup = renderToStaticMarkup(
      <RootLayout>
        <div>Shell child</div>
      </RootLayout>,
    );

    expect(markup).toContain('href="/citations-drafting"');
    expect(markup).toContain("Citations &amp; Drafting");
    expect(markup).toContain('href="/case-studies"');
    expect(markup).toContain("Case Studies");
  });
});
