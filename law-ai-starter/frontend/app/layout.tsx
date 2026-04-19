import type { Metadata } from "next";
import Link from "next/link";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import "./globals.css";

export const metadata: Metadata = {
  title: "Law AI",
  description: "Pakistan-focused legal information platform for public awareness and source-backed guidance",
};

const themeBootstrapScript = `
  (function() {
    try {
      var storedTheme = window.localStorage.getItem("law-ai-theme");
      var resolvedTheme = storedTheme === "dark" ? "dark" : "light";
      document.documentElement.dataset.theme = resolvedTheme;
    } catch (error) {
      document.documentElement.dataset.theme = "light";
    }
  })();
`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-scroll-behavior="smooth" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeBootstrapScript }} />
      </head>
      <body suppressHydrationWarning>
        <div className="app-shell">
          <header className="site-header">
            <div className="shell-container header-inner">
              <Link href="/" className="brand-link">
                <div className="brand-logo" aria-hidden="true">
                  <span className="brand-logo-image brand-logo-light" />
                  <span className="brand-logo-image brand-logo-dark" />
                </div>

                <div className="brand-copy">
                  <div className="brand-title">Law AI</div>
                  <div className="brand-subtitle">Pakistan legal information platform</div>
                </div>
              </Link>

              <nav className="top-nav">
                <ThemeToggle />
                <Link href="/" className="nav-link">
                  Home
                </Link>
                <Link href="/chat" className="nav-link">
                  Chat
                </Link>
                <Link href="/officer-authority" className="nav-link">
                  Officer Authority
                </Link>
                <Link href="/citations-drafting" className="nav-link">
                  Citations &amp; Drafting
                </Link>
                <Link href="/case-studies" className="nav-link">
                  Case Studies
                </Link>
                <Link href="/admin" className="nav-link">
                  Admin
                </Link>
              </nav>
            </div>
          </header>

          <main className="site-main">{children}</main>

          <footer className="site-footer">
            <div className="shell-container footer-inner">
              <div className="footer-brand">
                <div className="footer-logo" aria-hidden="true">
                  <span className="brand-logo-image brand-logo-light" />
                  <span className="brand-logo-image brand-logo-dark" />
                </div>
                <div className="footer-title">Law AI</div>
                <div className="footer-copy">
                  Public-facing legal information for awareness, transparency, and structured
                  source exploration.
                </div>
              </div>
              <div className="footer-links">
                <Link href="/chat" className="footer-link">
                  Chat
                </Link>
                <Link href="/officer-authority" className="footer-link">
                  Officer Authority
                </Link>
                <Link href="/citations-drafting" className="footer-link">
                  Citations &amp; Drafting
                </Link>
                <Link href="/case-studies" className="footer-link">
                  Case Studies
                </Link>
                <Link href="/admin" className="footer-link">
                  Admin
                </Link>
              </div>
              <div className="footer-note">For general informational use only.</div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
