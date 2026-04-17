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
                  <div className="brand-title">Law AI</div>
                  <div className="brand-subtitle">Legal information platform</div>
                </div>
              </Link>

              <nav className="top-nav">
                <Link href="/" className="nav-link">
                  Home
                </Link>
                <Link href="/chat" className="nav-link">
                  Chat
                </Link>
                <Link href="/officer-authority" className="nav-link">
                  Officer Authority
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
              <div>Law AI prototype for legal information and awareness.</div>
              <div>This product should not be treated as legal advice.</div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
