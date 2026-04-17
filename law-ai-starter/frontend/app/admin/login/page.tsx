"use client";

import Link from "next/link";
import { useEffect, useState, type FormEvent } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  clearAdminToken,
  fetchAdminMe,
  getStoredAdminToken,
  loginAdmin,
  storeAdminToken,
} from "@/lib/admin-auth";

const pageWrap: React.CSSProperties = {
  minHeight: "100vh",
  background:
    "radial-gradient(circle at top, rgba(45,78,180,0.20), transparent 24%), linear-gradient(180deg, #071226 0%, #09152b 100%)",
  color: "#f4f7ff",
  padding: "32px 0 72px",
};

const containerStyle: React.CSSProperties = {
  maxWidth: "1360px",
  margin: "0 auto",
  padding: "0 24px",
};

const cardStyle: React.CSSProperties = {
  background: "rgba(18, 28, 58, 0.92)",
  border: "1px solid rgba(120, 150, 255, 0.16)",
  borderRadius: "22px",
  boxShadow: "0 12px 34px rgba(0, 0, 0, 0.22)",
};

const secondaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  borderRadius: "14px",
  padding: "14px 20px",
  background: "transparent",
  color: "#dfe7ff",
  fontWeight: 700,
  fontSize: "15px",
  cursor: "pointer",
  textDecoration: "none",
  border: "1px solid rgba(150, 170, 255, 0.26)",
};

const fieldStyle: React.CSSProperties = {
  width: "100%",
  borderRadius: "14px",
  border: "1px solid rgba(136, 159, 232, 0.18)",
  background: "rgba(8, 15, 35, 0.96)",
  color: "#eef3ff",
  padding: "14px 15px",
  fontSize: "14px",
  outline: "none",
};

const badge: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  gap: "6px",
  padding: "7px 11px",
  borderRadius: "999px",
  fontSize: "12px",
  fontWeight: 700,
  border: "1px solid rgba(126, 162, 255, 0.22)",
  background: "rgba(126, 162, 255, 0.12)",
  color: "#b9caff",
};

export default function AdminLoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const nextPath = searchParams.get("next") || "/admin";

  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [checking, setChecking] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function restoreSession() {
      const storedToken = getStoredAdminToken();
      if (!storedToken) {
        if (!cancelled) {
          setChecking(false);
        }
        return;
      }

      try {
        await fetchAdminMe(storedToken);
        if (!cancelled) {
          router.replace(nextPath);
        }
      } catch {
        clearAdminToken();
        if (!cancelled) {
          setChecking(false);
        }
      }
    }

    restoreSession();

    return () => {
      cancelled = true;
    };
  }, [nextPath, router]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setLoading(true);
      setError("");
      const result = await loginAdmin(username, password);
      storeAdminToken(result.access_token);
      setPassword("");
      router.replace(nextPath);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || "Failed to sign in.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={pageWrap}>
      <div style={containerStyle}>
        <div style={{ ...cardStyle, padding: "32px", maxWidth: "560px", margin: "80px auto 0" }}>
          <div style={{ ...badge, marginBottom: "12px" }}>Protected admin route</div>
          <h1 style={{ fontSize: "38px", lineHeight: 1.1, margin: "0 0 12px" }}>Admin Login</h1>
          <p style={{ margin: "0 0 24px", color: "#c8d6f7", lineHeight: 1.7 }}>
            Sign in to access protected admin routes. Public legal-information pages and chat remain available without authentication.
          </p>

          {checking ? (
            <div style={{ color: "#dbe4ff" }}>Checking existing admin session...</div>
          ) : (
            <form onSubmit={handleSubmit} style={{ display: "grid", gap: "16px" }}>
              <div>
                <div style={{ color: "#dfe7ff", fontSize: "14px", fontWeight: 700, marginBottom: "8px" }}>Username</div>
                <input
                  type="text"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  style={fieldStyle}
                  autoComplete="username"
                />
              </div>

              <div>
                <div style={{ color: "#dfe7ff", fontSize: "14px", fontWeight: 700, marginBottom: "8px" }}>Password</div>
                <input
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  style={fieldStyle}
                  autoComplete="current-password"
                />
              </div>

              {error && (
                <div
                  style={{
                    background: "rgba(120, 22, 44, 0.2)",
                    border: "1px solid rgba(255, 120, 120, 0.25)",
                    borderRadius: "16px",
                    padding: "14px 16px",
                    color: "#ffe1e1",
                  }}
                >
                  {error}
                </div>
              )}

              <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", marginTop: "4px" }}>
                <button
                  type="submit"
                  style={{ ...secondaryButton, background: "#dfe7ff", color: "#071226", border: "none" }}
                  disabled={loading}
                >
                  {loading ? "Signing in..." : "Sign In"}
                </button>
                <Link href="/" style={secondaryButton}>
                  Back to Homepage
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </main>
  );
}
