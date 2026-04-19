"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { caseStudyRecords } from "@/lib/mock/case-studies-data";
import styles from "./page.module.css";

export default function CaseStudiesPage() {
  const [query, setQuery] = useState("");
  const [courtFilter, setCourtFilter] = useState("All courts");
  const [orderTypeFilter, setOrderTypeFilter] = useState("All order types");
  const [selectedId, setSelectedId] = useState(caseStudyRecords[0]?.id ?? "");

  const courts = useMemo(
    () => ["All courts", ...new Set(caseStudyRecords.map((item) => item.court))],
    [],
  );
  const orderTypes = useMemo(
    () => ["All order types", ...new Set(caseStudyRecords.map((item) => item.orderType))],
    [],
  );

  const filteredCases = useMemo(() => {
    const needle = query.trim().toLowerCase();

    return caseStudyRecords.filter((item) => {
      const courtMatch = courtFilter === "All courts" || item.court === courtFilter;
      const orderMatch = orderTypeFilter === "All order types" || item.orderType === orderTypeFilter;
      if (!courtMatch || !orderMatch) return false;
      if (!needle) return true;

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
      ]
        .join(" ")
        .toLowerCase();

      return haystack.includes(needle);
    });
  }, [courtFilter, orderTypeFilter, query]);

  const selectedCase = useMemo(() => {
    return filteredCases.find((item) => item.id === selectedId) ?? filteredCases[0] ?? null;
  }, [filteredCases, selectedId]);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.workspace}>
            <div className={styles.topBar}>
              <div>
                <div className={styles.sectionEyebrow}>Case Studies / Orders</div>
                <p className={`${styles.sectionText} ${styles.topBarText}`}>
                  Browse educational case summaries to see which court issued what order and how
                  the result was framed.
                </p>
              </div>
              <div className={styles.topLinks}>
                <Link href="/" className={styles.secondaryLink}>
                  Home
                </Link>
                <Link href="/chat" className={styles.secondaryLink}>
                  Chat
                </Link>
              </div>
            </div>

            <section className={styles.controlCard}>
              <div className={styles.controlHead}>
                <div>
                  <div className={styles.sectionEyebrow}>Research workspace</div>
                  <h1>Case research and order summaries</h1>
                  <p className={styles.sectionText}>
                    Search across court, citation, order type, and linked provisions without leaving the workspace.
                  </p>
                </div>
                <span className={styles.resultCount}>{filteredCases.length} case records</span>
              </div>

              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search case title, court, citation, bench, or linked law..."
                className={styles.searchInput}
              />

              <div className={styles.filterGrid}>
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
              </div>

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
                  No cases match this search. Try a broader court name or a general term like{" "}
                  <strong>bail</strong> or <strong>constitutional</strong>.
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
              <div className={styles.sectionEyebrow}>Selected case</div>
              <h2>{selectedCase?.title ?? "Choose a case"}</h2>
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
