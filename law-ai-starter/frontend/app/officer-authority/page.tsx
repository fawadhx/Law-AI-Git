"use client";

import { useMemo, useState } from "react";
import { SaveButton } from "@/components/common/save-button";
import { API_BASE_URL } from "@/lib/runtime-config";
import {
  activeFilterCount,
  listOptionMatches,
  matchesSearchQuery,
  resultCountLabel,
  uniqueOptionsFromLists,
} from "@/lib/search-filter";
import type { SavedItem } from "@/lib/saved-items";
import styles from "./page.module.css";

type OfficerAuthorityResponse = {
  rank: string;
  summary: string;
  powers: string[];
  limitations: string[];
};

const ranks = [
  {
    label: "SHO",
    value: "sho",
    themes: ["FIR", "complaint", "station process", "investigation"],
    description: "Station-level authority and public complaint handling context.",
  },
  {
    label: "ASI",
    value: "asi",
    themes: ["arrest", "investigation", "field process", "detention"],
    description: "Field investigation and procedure-related authority context.",
  },
  {
    label: "Inspector",
    value: "inspector",
    themes: ["supervision", "investigation", "public order", "case review"],
    description: "Supervisory police authority and investigation oversight context.",
  },
];

export default function OfficerAuthorityPage() {
  const [rank, setRank] = useState("sho");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<OfficerAuthorityResponse | null>(null);
  const [discoveryQuery, setDiscoveryQuery] = useState("");
  const [themeFilter, setThemeFilter] = useState("All authority themes");

  const titleRank = useMemo(() => {
    const match = ranks.find((item) => item.value === rank);
    return match?.label || rank.toUpperCase();
  }, [rank]);

  const authorityThemes = useMemo(
    () => uniqueOptionsFromLists(ranks.map((item) => item.themes), "All authority themes"),
    [],
  );

  const filteredRanks = useMemo(() => {
    return ranks.filter((item) => {
      if (!listOptionMatches(themeFilter, item.themes, "All authority themes")) return false;
      return matchesSearchQuery(discoveryQuery, [
        item.label,
        item.value,
        item.description,
        ...item.themes,
      ]);
    });
  }, [discoveryQuery, themeFilter]);

  const activeDiscoveryFilters = activeFilterCount(
    { themeFilter },
    ["All authority themes"],
  ) + (discoveryQuery.trim() ? 1 : 0);

  const savedAuthorityItem = useMemo<SavedItem | null>(() => {
    if (!result) return null;
    const sourceId = result.rank.toLowerCase();
    return {
      id: `officer-authority:${sourceId}`,
      type: "officer-authority",
      title: `${result.rank} authority details`,
      subtitle: "Officer authority lookup",
      summary: result.summary,
      href: "/officer-authority",
      tags: [result.rank, "authority", "powers", "limitations"],
      metadata: {
        rank: result.rank,
        powers: result.powers.length,
        limitations: result.limitations.length,
      },
      sourceId,
      savedAt: new Date().toISOString(),
    };
  }, [result]);

  function resetDiscoveryFilters() {
    setDiscoveryQuery("");
    setThemeFilter("All authority themes");
  }

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
                  Enter a rank to load the backend authority summary, powers, and limits.
                </p>
              </div>
            </div>

            <h2>Rank authority lookup</h2>

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
              <div className={styles.sectionEyebrow}>Rank discovery</div>
              <div className={styles.discoveryGrid}>
                <input
                  value={discoveryQuery}
                  onChange={(event) => setDiscoveryQuery(event.target.value)}
                  placeholder="Search rank, FIR, arrest, investigation..."
                  className={styles.discoveryField}
                />
                <label className={styles.selectField}>
                  <span>Authority theme</span>
                  <select value={themeFilter} onChange={(event) => setThemeFilter(event.target.value)}>
                    {authorityThemes.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <div className={styles.filterSummary}>
                <span>
                  {resultCountLabel(filteredRanks.length, "rank")} shown
                  {activeDiscoveryFilters ? `, ${activeDiscoveryFilters} filters active` : ""}
                </span>
                <button type="button" onClick={resetDiscoveryFilters}>
                  Reset
                </button>
              </div>
              {filteredRanks.length === 0 ? (
                <div className={styles.emptyState}>
                  No rank matches this search. Try <strong>FIR</strong>, <strong>arrest</strong>, or{" "}
                  <strong>investigation</strong>.
                </div>
              ) : (
                <div className={styles.rankChips}>
                  {filteredRanks.map((item) => (
                    <button
                      key={item.value}
                      onClick={() => void fetchAuthority(item.value)}
                      className={styles.rankChip}
                      type="button"
                    >
                      <span>{item.label}</span>
                      <small>{item.themes.slice(0, 2).join(" / ")}</small>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {error ? <div className={styles.errorBanner}>Request error: {error}</div> : null}
          </section>

          <section className={styles.resultCard}>
            <div className={styles.resultHeader}>
              <div>
                <div className={styles.sectionEyebrow}>Authority response</div>
                <h2>{result ? `${result.rank} authority details` : `${titleRank} authority details`}</h2>
              </div>
              <SaveButton item={savedAuthorityItem} />
            </div>

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
