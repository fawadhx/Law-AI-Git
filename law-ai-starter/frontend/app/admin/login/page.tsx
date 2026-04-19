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
import styles from "./page.module.css";

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
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.loginCard}>
          <div className={styles.badge}>Protected admin route</div>
          <h1>Admin Login</h1>
          <p>
            Sign in to access protected admin workflows. Public legal-information pages and chat
            remain available without authentication.
          </p>

          {checking ? (
            <div className={styles.statusText}>Checking existing admin session...</div>
          ) : (
            <form onSubmit={handleSubmit} className={styles.form}>
              <div>
                <label htmlFor="username" className={styles.label}>
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  className={styles.field}
                  autoComplete="username"
                />
              </div>

              <div>
                <label htmlFor="password" className={styles.label}>
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  className={styles.field}
                  autoComplete="current-password"
                />
              </div>

              {error ? <div className={styles.errorBanner}>{error}</div> : null}

              <div className={styles.actions}>
                <button type="submit" className={styles.primaryButton} disabled={loading}>
                  {loading ? "Signing in..." : "Sign In"}
                </button>
                <Link href="/" className={styles.secondaryLink}>
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
