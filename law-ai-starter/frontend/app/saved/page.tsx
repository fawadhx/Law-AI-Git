"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { CopySummaryButton } from "@/components/common/copy-summary-button";
import {
  savedItemTypeLabels,
  type SavedItem,
  type SavedItemType,
} from "@/lib/saved-items";
import { useSavedItems } from "@/lib/use-saved-items";
import { matchesSearchQuery, optionMatches, resultCountLabel } from "@/lib/search-filter";
import { formatResearchSummary } from "@/lib/research-utils";
import styles from "./page.module.css";

const TYPE_FILTERS: Array<{ value: "All saved types" | SavedItemType; label: string }> = [
  { value: "All saved types", label: "All saved types" },
  { value: "chat", label: savedItemTypeLabels.chat },
  { value: "officer-authority", label: savedItemTypeLabels["officer-authority"] },
  { value: "citation", label: savedItemTypeLabels.citation },
  { value: "draft-template", label: savedItemTypeLabels["draft-template"] },
  { value: "draft-checklist", label: savedItemTypeLabels["draft-checklist"] },
  { value: "draft-guide", label: savedItemTypeLabels["draft-guide"] },
  { value: "case-study", label: savedItemTypeLabels["case-study"] },
];

function groupItems(items: SavedItem[]) {
  return TYPE_FILTERS.filter((filter) => filter.value !== "All saved types")
    .map((filter) => ({
      type: filter.value as SavedItemType,
      label: filter.label,
      items: items.filter((item) => item.type === filter.value),
    }))
    .filter((group) => group.items.length > 0);
}

function formatSavedDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Saved recently";
  return `Saved ${date.toLocaleDateString("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  })}`;
}

function createSavedSummary(item: SavedItem): string {
  return formatResearchSummary({
    title: item.title,
    subtitle: item.subtitle,
    summary: item.summary,
    fields: [
      ["Type", savedItemTypeLabels[item.type]],
      ["Saved", formatSavedDate(item.savedAt)],
      ["Source", item.href],
    ],
    tags: item.tags,
  });
}

export default function SavedPage() {
  const { items, remove } = useSavedItems();
  const [query, setQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState<"All saved types" | SavedItemType>("All saved types");

  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      if (!optionMatches(typeFilter, item.type, "All saved types")) return false;
      return matchesSearchQuery(query, [
        item.title,
        item.subtitle,
        item.summary,
        item.type,
        item.sourceId,
        ...item.tags,
        ...Object.values(item.metadata).map(String),
      ]);
    });
  }, [items, query, typeFilter]);

  const groupedItems = useMemo(() => groupItems(filteredItems), [filteredItems]);

  function resetFilters() {
    setQuery("");
    setTypeFilter("All saved types");
  }

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <section className={styles.workspace}>
          <div className={styles.topBar}>
            <div>
              <div className={styles.sectionEyebrow}>Saved workspace</div>
              <h1>Saved research items</h1>
              <p className={styles.sectionText}>
                Revisit useful chat answers, authority lookups, drafting resources, and case records saved on this device.
              </p>
            </div>
          </div>

          <section className={styles.controlCard}>
            <div className={styles.controlHead}>
              <div>
                <div className={styles.sectionEyebrow}>Search saved items</div>
                <p className={styles.sectionText}>
                  Saved items are stored locally in your browser and can be removed anytime.
                </p>
              </div>
              <span className={styles.resultCount}>{resultCountLabel(filteredItems.length, "saved item")}</span>
            </div>

            <div className={styles.filterGrid}>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search saved titles, tags, courts, categories..."
                className={styles.searchInput}
              />
              <label className={styles.selectField}>
                <span>Saved type</span>
                <select
                  value={typeFilter}
                  onChange={(event) => setTypeFilter(event.target.value as "All saved types" | SavedItemType)}
                >
                  {TYPE_FILTERS.map((item) => (
                    <option key={item.value} value={item.value}>
                      {item.label}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            {items.length > 0 ? (
              <div className={styles.typeSummary}>
                {groupItems(items).map((group) => (
                  <button
                    key={group.type}
                    type="button"
                    className={typeFilter === group.type ? `${styles.typeChip} ${styles.typeChipActive}` : styles.typeChip}
                    onClick={() => setTypeFilter(group.type)}
                  >
                    {group.label}: {group.items.length}
                  </button>
                ))}
              </div>
            ) : null}
          </section>

          {items.length === 0 ? (
            <section className={styles.emptyState}>
              <div className={styles.sectionEyebrow}>Nothing saved yet</div>
              <h2>Save useful research as you work</h2>
              <p>
                Use the save button on chat results, selected citation/drafting resources, case
                details, and officer authority results. Saved items will appear here on this device.
              </p>
              <div className={styles.emptyLinks}>
                <Link href="/chat">Open Chat</Link>
                <Link href="/officer-authority">Officer Authority</Link>
                <Link href="/citations-drafting">Citations &amp; Drafting</Link>
                <Link href="/case-studies">Case Studies</Link>
              </div>
            </section>
          ) : filteredItems.length === 0 ? (
            <section className={styles.emptyState}>
              <div className={styles.sectionEyebrow}>No matching saved items</div>
              <h2>Try a broader search</h2>
              <p>Clear the search text or switch back to all saved types to see everything saved.</p>
              <div className={styles.emptyLinks}>
                <button type="button" onClick={resetFilters}>
                  Reset saved filters
                </button>
              </div>
            </section>
          ) : (
            <div className={styles.groupStack}>
              {groupedItems.map((group) => (
                <section key={group.type} className={styles.groupSection}>
                  <div className={styles.groupHeader}>
                    <div>
                      <div className={styles.sectionEyebrow}>{group.label}</div>
                      <h2>{resultCountLabel(group.items.length, "item")}</h2>
                    </div>
                  </div>
                  <div className={styles.cardGrid}>
                    {group.items.map((item) => (
                      <article key={item.id} className={styles.savedCard}>
                        <div className={styles.cardMeta}>
                          <span className={styles.kindBadge}>{savedItemTypeLabels[item.type]}</span>
                          <span>{formatSavedDate(item.savedAt)}</span>
                        </div>
                        <h3>{item.title}</h3>
                        <div className={styles.subtitle}>{item.subtitle}</div>
                        <p>{item.summary}</p>
                        {item.tags.length ? (
                          <div className={styles.tagRow}>
                            {item.tags.slice(0, 4).map((tag) => (
                              <span key={`${item.id}-${tag}`} className={styles.tagChip}>
                                {tag}
                              </span>
                            ))}
                          </div>
                        ) : null}
                        <div className={styles.cardActions}>
                          <Link href={item.href}>Open</Link>
                          <CopySummaryButton text={createSavedSummary(item)} />
                          <button type="button" onClick={() => remove(item.id)}>
                            Remove
                          </button>
                        </div>
                      </article>
                    ))}
                  </div>
                </section>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
