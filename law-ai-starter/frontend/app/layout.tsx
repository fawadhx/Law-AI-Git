import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Law AI",
  description: "Legal information platform prototype",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-scroll-behavior="smooth" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <div className="app-shell">
          <header className="site-header">
            <div className="shell-container header-inner">
              <Link href="/" className="brand-link">
                <div className="brand-badge">LA</div>

                <div className="brand-copy">
                  <div className="brand-title">
                    LawBridge <span className="brand-accent">AI</span>
                  </div>
                </div>
              </Link>

              <nav className="top-nav">
                <Link href="/#rights" className="nav-link">
                  Know Your Rights
                </Link>
                <Link href="/officer-authority" className="nav-link">
                  Officer Authority
                </Link>
                <Link href="/admin" className="nav-link">
                  Source Library
                </Link>
                <Link href="/admin" className="nav-link">
                  Pricing
                </Link>
              </nav>

              <div className="header-actions">
                <Link href="/chat" className="header-login">
                  Log In
                </Link>
                <Link href="/chat" className="header-cta">
                  Get Started
                </Link>
              </div>
            </div>
          </header>

          <main className="site-main">{children}</main>

          <footer className="site-footer">
            <div className="shell-container footer-inner">
              <div className="footer-brand-block">
                <div className="footer-brand-row">
                  <div className="footer-badge">LA</div>
                  <div className="footer-brand-title">LawBridge AI</div>
                </div>
                <p className="footer-brand-copy">
                  The world&apos;s first authoritative legal-information platform for public
                  transparency and literacy.
                </p>
                <div className="footer-icon-row">
                  <span className="footer-icon">G</span>
                  <span className="footer-icon">C</span>
                </div>
              </div>

              <div className="footer-column">
                <div className="footer-heading">Product</div>
                <Link href="/#rights" className="footer-link">
                  Know Your Rights
                </Link>
                <Link href="/officer-authority" className="footer-link">
                  Officer Authority
                </Link>
                <Link href="/admin" className="footer-link">
                  Statute Library
                </Link>
                <Link href="/chat" className="footer-link">
                  AI Research Assistant
                </Link>
              </div>

              <div className="footer-column">
                <div className="footer-heading">Resources</div>
                <Link href="/admin" className="footer-link">
                  Documentation
                </Link>
                <Link href="/chat" className="footer-link">
                  Legal Glossary
                </Link>
                <Link href="/chat" className="footer-link">
                  Community Forum
                </Link>
                <Link href="/admin" className="footer-link">
                  Public API
                </Link>
              </div>

              <div className="footer-column">
                <div className="footer-heading">Legal</div>
                <Link href="/chat" className="footer-link">
                  Privacy Policy
                </Link>
                <Link href="/chat" className="footer-link">
                  Terms of Service
                </Link>
                <Link href="/chat" className="footer-link">
                  Information Disclaimer
                </Link>
                <Link href="/chat" className="footer-link">
                  Cookie Policy
                </Link>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}

