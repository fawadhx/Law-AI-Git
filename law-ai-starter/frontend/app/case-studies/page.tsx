"use client";

import { useEffect, useMemo, useState } from "react";
import { ComparePanel, type CompareField } from "@/components/common/compare-panel";
import { CopySummaryButton } from "@/components/common/copy-summary-button";
import { RelatedItemsPanel } from "@/components/common/related-items-panel";
import { SaveButton } from "@/components/common/save-button";
import { caseStudyRecords } from "@/lib/mock/case-studies-data";
import {
  activeFilterCount,
  listOptionMatches,
  matchesSearchQuery,
  optionMatches,
  resultCountLabel,
  uniqueOptions,
  uniqueOptionsFromLists,
} from "@/lib/search-filter";
import { createTagRelatedItems, formatResearchSummary } from "@/lib/research-utils";
import type { SavedItem } from "@/lib/saved-items";
import styles from "./page.module.css";

function createSavedCase(item: (typeof caseStudyRecords)[number] | null): SavedItem | null {
  if (!item) return null;
  return {
    id: `case-study:${item.id}`,
    type: "case-study",
    title: item.title,
    subtitle: `${item.court} - ${item.orderType}`,
    summary: item.holding,
    href: "/case-studies",
    tags: [item.courtLevel, item.dataStatus, ...item.legalIssues].slice(0, 5),
    metadata: {
      court: item.court,
      bench: item.bench,
      orderDate: item.orderDate,
      outcome: item.outcome,
      dataStatus: item.dataStatus,
    },
    sourceId: item.id,
    savedAt: new Date().toISOString(),
  };
}

function getCaseTags(item: (typeof caseStudyRecords)[number]): string[] {
  return [
    item.court,
    item.courtLevel,
    item.orderType,
    item.proceduralPosture,
    item.dataStatus,
    ...item.legalIssues,
    ...item.linkedProvisions,
    ...item.tags,
  ];
}

function createCaseSummary(item: (typeof caseStudyRecords)[number] | null): string {
  if (!item) return "";
  return formatResearchSummary({
    title: item.title,
    subtitle: `${item.court} / ${item.orderType}`,
    summary: item.holding,
    fields: [
      ["Citation", item.citation],
      ["Bench", item.bench],
      ["Order date", item.orderDate],
      ["Outcome", item.outcome],
      ["Disposition", item.disposition],
      ["Data status", item.dataStatus],
      ["Linked provisions", item.linkedProvisions.join(", ")],
    ],
    tags: item.legalIssues,
  });
}

function createCaseCompareFields(
  left: (typeof caseStudyRecords)[number] | null,
  right: (typeof caseStudyRecords)[number] | null,
): CompareField[] {
  return [
    { label: "Court", left: left?.court, right: right?.court },
    { label: "Bench", left: left?.bench, right: right?.bench },
    { label: "Order type", left: left?.orderType, right: right?.orderType },
    { label: "Outcome", left: left?.outcome, right: right?.outcome },
    { label: "Legal issues", left: left?.legalIssues.join(", "), right: right?.legalIssues.join(", ") },
    { label: "Linked provisions", left: left?.linkedProvisions.join(", "), right: right?.linkedProvisions.join(", ") },
  ];
}

export default function CaseStudiesPage() {
  const [query, setQuery] = useState("");
  const [courtFilter, setCourtFilter] = useState("All courts");
  const [orderTypeFilter, setOrderTypeFilter] = useState("All order types");
  const [jurisdictionFilter, setJurisdictionFilter] = useState("All jurisdictions");
  const [courtLevelFilter, setCourtLevelFilter] = useState("All court levels");
  const [benchFilter, setBenchFilter] = useState("All benches");
  const [postureFilter, setPostureFilter] = useState("All postures");
  const [statusFilter, setStatusFilter] = useState("All statuses");
  const [issueFilter, setIssueFilter] = useState("All issues");
  const [linkedTypeFilter, setLinkedTypeFilter] = useState("All linked-law types");
  const [selectedId, setSelectedId] = useState(caseStudyRecords[0]?.id ?? "");
  const [compareId, setCompareId] = useState("");
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  const courts = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.court), "All courts"),
    [],
  );
  const orderTypes = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.orderType), "All order types"),
    [],
  );
  const jurisdictions = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.jurisdiction), "All jurisdictions"),
    [],
  );
  const courtLevels = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.courtLevel), "All court levels"),
    [],
  );
  const benches = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.bench), "All benches"),
    [],
  );
  const postures = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.proceduralPosture), "All postures"),
    [],
  );
  const statuses = useMemo(
    () => uniqueOptions(caseStudyRecords.map((item) => item.dataStatus), "All statuses"),
    [],
  );
  const legalIssues = useMemo(
    () => uniqueOptionsFromLists(caseStudyRecords.map((item) => item.legalIssues), "All issues"),
    [],
  );
  const linkedLawTypes = useMemo(
    () => uniqueOptionsFromLists(
      caseStudyRecords.map((item) => item.linkedLawReferences.map((reference) => reference.referenceType)),
      "All linked-law types",
    ),
    [],
  );

  const activeFilters = activeFilterCount(
    {
      courtFilter,
      orderTypeFilter,
      jurisdictionFilter,
      courtLevelFilter,
      benchFilter,
      postureFilter,
      statusFilter,
      issueFilter,
      linkedTypeFilter,
    },
    [
      "All courts",
      "All order types",
      "All jurisdictions",
      "All court levels",
      "All benches",
      "All postures",
      "All statuses",
      "All issues",
      "All linked-law types",
    ],
  );

  function resetFilters() {
    setQuery("");
    setCourtFilter("All courts");
    setOrderTypeFilter("All order types");
    setJurisdictionFilter("All jurisdictions");
    setCourtLevelFilter("All court levels");
    setBenchFilter("All benches");
    setPostureFilter("All postures");
    setStatusFilter("All statuses");
    setIssueFilter("All issues");
    setLinkedTypeFilter("All linked-law types");
  }

  const filteredCases = useMemo(() => {
    return caseStudyRecords.filter((item) => {
      if (!optionMatches(courtFilter, item.court, "All courts")) return false;
      if (!optionMatches(orderTypeFilter, item.orderType, "All order types")) return false;
      if (!optionMatches(jurisdictionFilter, item.jurisdiction, "All jurisdictions")) return false;
      if (!optionMatches(courtLevelFilter, item.courtLevel, "All court levels")) return false;
      if (!optionMatches(benchFilter, item.bench, "All benches")) return false;
      if (!optionMatches(postureFilter, item.proceduralPosture, "All postures")) return false;
      if (!optionMatches(statusFilter, item.dataStatus, "All statuses")) return false;
      if (!listOptionMatches(issueFilter, item.legalIssues, "All issues")) return false;
      if (
        !listOptionMatches(
          linkedTypeFilter,
          item.linkedLawReferences.map((reference) => reference.referenceType),
          "All linked-law types",
        )
      ) {
        return false;
      }

      const haystack = [
        item.title,
        item.citation,
        item.dataStatus,
        item.jurisdiction,
        item.courtLevel,
        item.court,
        item.bench,
        item.proceduralPosture,
        item.summary,
        item.holding,
        item.outcome,
        item.disposition,
        item.researchUse,
        ...item.linkedProvisions,
        ...item.legalIssues,
        ...item.keyFacts,
        ...item.tags,
      ];

      return matchesSearchQuery(query, haystack);
    });
  }, [
    benchFilter,
    courtFilter,
    courtLevelFilter,
    issueFilter,
    jurisdictionFilter,
    linkedTypeFilter,
    orderTypeFilter,
    postureFilter,
    query,
    statusFilter,
  ]);

  const selectedCase = useMemo(() => {
    return filteredCases.find((item) => item.id === selectedId) ?? filteredCases[0] ?? null;
  }, [filteredCases, selectedId]);

  useEffect(() => {
    if (filteredCases.length === 0) return;
    if (filteredCases.some((item) => item.id === selectedId)) return;
    setSelectedId(filteredCases[0].id);
  }, [filteredCases, selectedId]);

  const savedCase = useMemo(() => createSavedCase(selectedCase), [selectedCase]);
  const compareCase = useMemo(() => caseStudyRecords.find((item) => item.id === compareId) ?? null, [compareId]);
  const relatedCases = useMemo(
    () => createTagRelatedItems(caseStudyRecords, selectedCase, getCaseTags, 3),
    [selectedCase],
  );
  const selectedCaseSummary = useMemo(() => createCaseSummary(selectedCase), [selectedCase]);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.workspace}>
            <div className={styles.topBar}>
              <div>
                <div className={styles.sectionEyebrow}>Case Studies / Orders</div>
                <p className={`${styles.sectionText} ${styles.topBarText}`}>
                  Search structured case and order summaries by court, bench, issue, or linked law.
                </p>
              </div>
            </div>

            <section className={styles.controlCard}>
              <div className={styles.controlHead}>
                <div>
                  <div className={styles.sectionEyebrow}>Research workspace</div>
                  <h1>Case and order research</h1>
                  <p className={styles.sectionText}>
                    Search first, then narrow by court, order type, or advanced metadata.
                  </p>
                </div>
                <span className={styles.resultCount}>{resultCountLabel(filteredCases.length, "case record")}</span>
              </div>

              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search case title, court, citation, bench, or linked law..."
                className={styles.searchInput}
              />

              <div className={styles.primaryFilterGrid}>
                <label className={styles.selectField}>
                  <span>Court</span>
                  <select value={courtFilter} onChange={(event) => setCourtFilter(event.target.value)}>
                    {courts.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label className={styles.selectField}>
                  <span>Order type</span>
                  <select value={orderTypeFilter} onChange={(event) => setOrderTypeFilter(event.target.value)}>
                    {orderTypes.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
                <label className={styles.selectField}>
                  <span>Legal issue</span>
                  <select value={issueFilter} onChange={(event) => setIssueFilter(event.target.value)}>
                    {legalIssues.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className={styles.filterSummary}>
                <span>{activeFilters ? `${activeFilters} filters active` : "No advanced filters active"}</span>
                <button type="button" onClick={() => setShowAdvancedFilters((value) => !value)}>
                  {showAdvancedFilters ? "Hide filters" : "More filters"}
                </button>
                <button type="button" onClick={resetFilters}>
                  Reset filters
                </button>
              </div>

              {showAdvancedFilters ? (
                <div className={styles.filterGrid}>
                  <label className={styles.selectField}>
                    <span>Jurisdiction</span>
                    <select value={jurisdictionFilter} onChange={(event) => setJurisdictionFilter(event.target.value)}>
                      {jurisdictions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Court level</span>
                    <select value={courtLevelFilter} onChange={(event) => setCourtLevelFilter(event.target.value)}>
                      {courtLevels.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Bench / judge</span>
                    <select value={benchFilter} onChange={(event) => setBenchFilter(event.target.value)}>
                      {benches.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Posture</span>
                    <select value={postureFilter} onChange={(event) => setPostureFilter(event.target.value)}>
                      {postures.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Data status</span>
                    <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
                      {statuses.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Linked-law type</span>
                    <select value={linkedTypeFilter} onChange={(event) => setLinkedTypeFilter(event.target.value)}>
                      {linkedLawTypes.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              ) : null}

              <div className={styles.quickStats}>
                <div className={styles.statCard}>
                  <strong>{caseStudyRecords.length}</strong>
                  <span>Case records</span>
                </div>
                <div className={styles.statCard}>
                  <strong>{courts.length - 1}</strong>
                  <span>Courts</span>
                </div>
                <div className={styles.statCard}>
                  <strong>{orderTypes.length - 1}</strong>
                  <span>Order types</span>
                </div>
              </div>

              <div className={styles.primerGrid}>
                <div className={styles.primerCard}>
                  <strong>Record status</strong>
                  <span>Current case entries are demo structures for future verified order integration.</span>
                </div>
                <div className={styles.primerCard}>
                  <strong>Research focus</strong>
                  <span>Each record separates court, bench, order type, issue, outcome, and timeline.</span>
                </div>
                <div className={styles.primerCard}>
                  <strong>Source-ready shape</strong>
                  <span>Fields are prepared for official source URLs, citations, and linked provisions.</span>
                </div>
              </div>
            </section>

            <section className={styles.listPanel}>
              <div className={styles.listHeader}>
                <div className={styles.sectionEyebrow}>Cases</div>
                <p className={styles.sectionText}>
                  Select a case to inspect the court, bench, outcome, and order timeline in more detail.
                </p>
              </div>

              {filteredCases.length === 0 ? (
                <div className={styles.emptyState}>
                  <strong>No case records match your filters.</strong> Try <span>bail</span>,{" "}
                  <span>constitutional</span>, or a broader court name, or{" "}
                  <button type="button" onClick={resetFilters}>
                    reset filters
                  </button>
                  .
                </div>
              ) : (
                <div className={styles.caseList}>
                  {filteredCases.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      className={
                        item.id === selectedCase?.id ? `${styles.caseCard} ${styles.caseCardActive}` : styles.caseCard
                      }
                      onClick={() => setSelectedId(item.id)}
                    >
                      <div className={styles.caseMeta}>
                        <span className={styles.kindBadge}>{item.orderType}</span>
                        <span className={styles.tagLine}>{item.orderDate}</span>
                      </div>
                      <h2>{item.title}</h2>
                      <div className={styles.caseReference}>{item.citation}</div>
                      <div className={styles.caseSubMeta}>
                        <span>{item.court}</span>
                        <span>{item.bench}</span>
                        <span>{item.proceduralPosture}</span>
                      </div>
                      <p>{item.summary}</p>
                      <div className={styles.issueLine}>
                        {item.legalIssues.slice(0, 2).map((issue) => (
                          <span key={`${item.id}-${issue}`}>{issue}</span>
                        ))}
                      </div>
                      <div className={styles.tagRow}>
                        {item.linkedProvisions.slice(0, 3).map((tag, index) => (
                          <span key={`${item.id}-${tag}-${index}`} className={styles.tagChip}>
                            {tag}
                          </span>
                        ))}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </section>
          </section>

          <aside className={styles.detailPanel}>
            <div className={styles.detailHeader}>
              <div>
                <div className={styles.sectionEyebrow}>Selected case</div>
                <h2>{selectedCase?.title ?? "Choose a case"}</h2>
              </div>
              <SaveButton item={savedCase} />
            </div>

            {!selectedCase ? (
              <div className={styles.emptyState}>
                Choose a case record to review the order summary and linked provisions here.
              </div>
            ) : (
              <div className={styles.detailStack}>
                <article className={styles.detailCard}>
                  <div className={styles.caseLead}>
                    <div>
                      <div className={styles.caseLeadTitle}>{selectedCase.title}</div>
                      <div className={styles.caseReference}>{selectedCase.citation}</div>
                    </div>
                    <div className={styles.caseLeadBadges}>
                      <span className={styles.kindBadge}>{selectedCase.orderType}</span>
                      <span className={styles.outcomeBadge}>{selectedCase.outcome}</span>
                    </div>
                  </div>
                  <div className={styles.metaGrid}>
                    <div className={styles.metaItem}>
                      <strong>Citation</strong>
                      <span>{selectedCase.citation}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Court</strong>
                      <span>{selectedCase.court}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Jurisdiction</strong>
                      <span>{selectedCase.jurisdiction}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Court level</strong>
                      <span>{selectedCase.courtLevel}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Bench</strong>
                      <span>{selectedCase.bench}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Order date</strong>
                      <span>{selectedCase.orderDate}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Order type</strong>
                      <span>{selectedCase.orderType}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Outcome</strong>
                      <span>{selectedCase.outcome}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Data status</strong>
                      <span>{selectedCase.dataStatus}</span>
                    </div>
                    <div className={styles.metaItem}>
                      <strong>Procedural posture</strong>
                      <span>{selectedCase.proceduralPosture}</span>
                    </div>
                  </div>
                </article>

                <section className={styles.utilityPanel}>
                  <div className={styles.detailHeader}>
                    <div>
                      <div className={styles.sectionEyebrow}>Research utilities</div>
                      <p className={styles.sectionText}>Copy this case summary, or compare only when needed.</p>
                    </div>
                    <CopySummaryButton text={selectedCaseSummary} />
                  </div>
                  <details className={styles.utilityDetails}>
                    <summary>Compare and related records</summary>
                    <label className={styles.selectField}>
                      <span>Compare with</span>
                      <select value={compareId} onChange={(event) => setCompareId(event.target.value)}>
                        <option value="">Choose another case</option>
                        {caseStudyRecords
                          .filter((item) => item.id !== selectedCase.id)
                          .map((item) => (
                            <option key={item.id} value={item.id}>
                              {item.title}
                            </option>
                          ))}
                      </select>
                    </label>
                    <ComparePanel
                      leftTitle={selectedCase.title}
                      rightTitle={compareCase?.title}
                      fields={createCaseCompareFields(selectedCase, compareCase)}
                    />
                    <RelatedItemsPanel
                      items={relatedCases.map((item) => ({
                        id: item.id,
                        title: item.title,
                        subtitle: `${item.court} / ${item.orderType}`,
                        tags: item.legalIssues,
                        onSelect: () => setSelectedId(item.id),
                      }))}
                    />
                  </details>
                </section>

                <article className={styles.detailCard}>
                  <div className={styles.detailSection}>
                    <h3>Short holding / summary</h3>
                    <p>{selectedCase.holding}</p>
                  </div>
                  <div className={styles.detailSection}>
                    <h3>Disposition</h3>
                    <p>{selectedCase.disposition}</p>
                  </div>
                  <div className={styles.detailSection}>
                    <h3>Order overview</h3>
                    <p>{selectedCase.summary}</p>
                  </div>
                  <div className={styles.detailSection}>
                    <h3>Research use</h3>
                    <p>{selectedCase.researchUse}</p>
                  </div>
                </article>

                <article className={styles.detailCard}>
                  <div className={styles.detailSection}>
                    <h3>Legal issues</h3>
                    <div className={styles.issueGrid}>
                      {selectedCase.legalIssues.map((item) => (
                        <div key={`${selectedCase.id}-${item}`} className={styles.issueCard}>
                          {item}
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className={styles.detailSection}>
                    <h3>Key facts tracked</h3>
                    <div className={styles.bulletList}>
                      {selectedCase.keyFacts.map((item) => (
                        <div key={`${selectedCase.id}-${item}`}>{item}</div>
                      ))}
                    </div>
                  </div>
                </article>

                <article className={styles.detailCard}>
                  <div className={styles.detailSection}>
                    <h3>Linked laws / provisions</h3>
                    <div className={styles.linkedLawList}>
                      {selectedCase.linkedLawReferences.map((item) => (
                        <div key={`${selectedCase.id}-${item.label}`} className={styles.linkedLawItem}>
                          <strong>{item.label}</strong>
                          <span>{item.referenceType}</span>
                          <p>{item.note}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </article>

                <article className={styles.detailCard}>
                  <div className={styles.detailSection}>
                    <h3>Case timeline / order history</h3>
                    <div className={styles.timeline}>
                      {selectedCase.timeline.map((event) => (
                        <div key={event.id} className={styles.timelineItem}>
                          <div className={styles.timelineDate}>{event.date}</div>
                          <div>
                            <div className={styles.timelineTitle}>
                              {event.title} <span>{event.eventType}</span>
                            </div>
                            <div className={styles.timelineSummary}>{event.summary}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </article>

                <article className={styles.detailCard}>
                  <div className={styles.detailSection}>
                    <h3>Source status</h3>
                    <p>{selectedCase.sourceNote}</p>
                    {selectedCase.sourceUrl ? (
                      <a href={selectedCase.sourceUrl} className={styles.sourceLink}>
                        Open source
                      </a>
                    ) : null}
                  </div>
                </article>
              </div>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}
