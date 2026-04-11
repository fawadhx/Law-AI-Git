import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Law AI",
  description: "Legal information platform prototype",
};

const navContainerStyle: React.CSSProperties = {
  maxWidth: "1280px",
  margin: "0 auto",
  padding: "0 28px",
};

const navLinkStyle: React.CSSProperties = {
  color: "#dfe7ff",
  textDecoration: "none",
  fontSize: "15px",
  fontWeight: 600,
  padding: "10px 14px",
  borderRadius: "12px",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div
          style={{
            minHeight: "100vh",
            background:
              "radial-gradient(circle at top, rgba(45,78,180,0.12), transparent 22%), linear-gradient(180deg, #061120 0%, #09152b 100%)",
            color: "#f4f7ff",
          }}
        >
          <header
            style={{
              position: "sticky",
              top: 0,
              zIndex: 50,
              backdropFilter: "blur(16px)",
              background: "rgba(5, 10, 24, 0.78)",
              borderBottom: "1px solid rgba(120, 150, 255, 0.10)",
            }}
          >
            <div
              style={{
                ...navContainerStyle,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "20px",
                minHeight: "78px",
                flexWrap: "wrap",
              }}
            >
              <Link
                href="/"
                style={{
                  textDecoration: "none",
                  color: "#ffffff",
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                }}
              >
                <div
                  style={{
                    width: "40px",
                    height: "40px",
                    borderRadius: "14px",
                    background:
                      "linear-gradient(180deg, rgba(126,162,255,0.95), rgba(77,118,255,0.88))",
                    color: "#081227",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 800,
                    fontSize: "16px",
                    boxShadow: "0 10px 24px rgba(53, 94, 217, 0.28)",
                  }}
                >
                  LA
                </div>

                <div>
                  <div
                    style={{
                      fontSize: "20px",
                      fontWeight: 800,
                      lineHeight: 1.1,
                      letterSpacing: "-0.4px",
                    }}
                  >
                    Law AI
                  </div>
                  <div
                    style={{
                      fontSize: "12px",
                      color: "#aebee9",
                      marginTop: "2px",
                    }}
                  >
                    Legal information platform
                  </div>
                </div>
              </Link>

              <nav
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  flexWrap: "wrap",
                }}
              >
                <Link href="/" style={navLinkStyle}>
                  Home
                </Link>
                <Link href="/chat" style={navLinkStyle}>
                  Chat
                </Link>
                <Link href="/officer-authority" style={navLinkStyle}>
                  Officer Authority
                </Link>
                <Link href="/admin" style={navLinkStyle}>
                  Admin
                </Link>
              </nav>
            </div>
          </header>

          <div>{children}</div>

          <footer
            style={{
              borderTop: "1px solid rgba(120, 150, 255, 0.10)",
              marginTop: "20px",
            }}
          >
            <div
              style={{
                ...navContainerStyle,
                paddingTop: "20px",
                paddingBottom: "24px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "14px",
                flexWrap: "wrap",
                color: "#aebee9",
                fontSize: "14px",
              }}
            >
              <div>Law AI prototype for legal information and awareness.</div>
              <div>This product should not be treated as legal advice.</div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}