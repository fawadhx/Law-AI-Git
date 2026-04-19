"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { API_BASE_URL } from "@/lib/runtime-config";
import styles from "./page.module.css";

type OfficerAuthorityResponse = {
  rank: string;
  summary: string;
  powers: string[];
  limitations: string[];
};

const ranks = [
  { label: "SHO", value: "sho" },
  { label: "ASI", value: "asi" },
  { label: "Inspector", value: "inspector" },
];

export default function OfficerAuthorityPage() {
  const [rank, setRank] = useState("sho");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<OfficerAuthorityResponse | null>(null);

  const titleRank = useMemo(() => {
    const match = ranks.find((item) => item.value === rank);
    return match?.label || rank.toUpperCase();
  }, [rank]);

  async function fetchAuthority(selectedRank?: string) {
    const targetRank = (selectedRank || rank).trim().toLowerCase();
    if (!targetRank) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/officer-authority/${encodeURIComponent(targetRank)}`,
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(errorBody?.detail || "Failed to fetch officer authority.");
      }

      const data: OfficerAuthorityResponse = await response.json();
      setResult(data);
      setRank(targetRank);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Failed to fetch officer authority.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.searchCard}>
            <div className={styles.topBar}>
              <div>
                <div className={styles.sectionEyebrow}>Officer authority lookup</div>
                <p className={styles.sectionText}>
                  Search a rank and review the structured authority summary inside the working tool.
                </p>
              </div>
              <div className={styles.heroActions}>
                <Link href="/" className={styles.secondaryLink}>
                  Home
                </Link>
                <Link href="/chat" className={styles.secondaryLink}>
                  Chat
                </Link>
              </div>
            </div>

            <h2>Check authority details</h2>

            <label htmlFor="rank" className={styles.fieldLabel}>
              Officer rank
            </label>
            <input
              id="rank"
              value={rank}
              onChange={(event) => setRank(event.target.value)}
              placeholder="Enter rank, for example sho"
              className={styles.field}
            />

            <button
              onClick={() => void fetchAuthority()}
              disabled={loading || !rank.trim()}
              className={styles.primaryButton}
            >
              {loading ? "Loading authority..." : "Check authority"}
            </button>

            <div className={styles.quickSection}>
              <div className={styles.sectionEyebrow}>Quick examples</div>
              <div className={styles.rankChips}>
                {ranks.map((item) => (
                  <button
                    key={item.value}
                    onClick={() => void fetchAuthority(item.value)}
                    className={styles.rankChip}
                    type="button"
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {error ? <div className={styles.errorBanner}>Request error: {error}</div> : null}
          </section>

          <section className={styles.resultCard}>
            <div className={styles.sectionEyebrow}>Authority response</div>
            <h2>{result ? `${result.rank} authority details` : `${titleRank} authority details`}</h2>

            {!result ? (
              <div className={styles.emptyState}>
                Select a rank such as <strong>SHO</strong>, <strong>ASI</strong>, or{" "}
                <strong>Inspector</strong> to load structured authority information from the
                backend.
              </div>
            ) : (
              <div className={styles.resultStack}>
                <article className={styles.summaryPanel}>
                  <div className={styles.panelLabel}>Summary</div>
                  <div className={styles.summaryText}>{result.summary}</div>
                </article>

                <div className={styles.dualGrid}>
                  <article className={styles.powersPanel}>
                    <div className={styles.panelLabel}>Can do / likely powers</div>
                    <ul className={styles.list}>
                      {result.powers.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </article>

                  <article className={styles.limitationsPanel}>
                    <div className={styles.panelLabel}>Cannot do / key limits</div>
                    <ul className={styles.list}>
                      {result.limitations.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </article>
                </div>

                <article className={styles.referencePanel}>
                  <div className={styles.panelLabel}>Reference details</div>
                  <div className={styles.referenceGrid}>
                    <div className={styles.referenceItem}>
                      <strong>Rank searched</strong>
                      <span>{result.rank}</span>
                    </div>
                    <div className={styles.referenceItem}>
                      <strong>Output type</strong>
                      <span>Structured legal-information summary</span>
                    </div>
                    <div className={styles.referenceItem}>
                      <strong>Use carefully</strong>
                      <span>Authority can vary by procedure, jurisdiction, and context.</span>
                    </div>
                    <div className={styles.referenceItem}>
                      <strong>Reading note</strong>
                      <span>Review the result alongside the relevant law, procedure, and factual setting.</span>
                    </div>
                  </div>
                </article>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
