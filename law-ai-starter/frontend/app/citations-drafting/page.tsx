"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import {
  citationExamples,
  draftSectionGuides,
  draftingChecklists,
  draftTemplates,
  type CitationExample,
  type DraftChecklist,
  type DraftSectionGuide,
  type DraftTemplate,
} from "@/lib/mock/citations-drafting-data";
import styles from "./page.module.css";

type ResourceFilter = "all" | "citation" | "template" | "checklist" | "guide";

type ResourceItem =
  | { id: string; kind: "citation"; title: string; summary: string; tags: string[]; record: CitationExample }
  | { id: string; kind: "template"; title: string; summary: string; tags: string[]; record: DraftTemplate }
  | { id: string; kind: "checklist"; title: string; summary: string; tags: string[]; record: DraftChecklist }
  | { id: string; kind: "guide"; title: string; summary: string; tags: string[]; record: DraftSectionGuide };

const FILTERS: Array<{ key: ResourceFilter; label: string }> = [
  { key: "all", label: "All resources" },
  { key: "citation", label: "Citation examples" },
  { key: "template", label: "Templates" },
  { key: "checklist", label: "Checklists" },
  { key: "guide", label: "Section guides" },
];

function buildResources(): ResourceItem[] {
  const citationItems: ResourceItem[] = citationExamples.map((item) => ({
    id: item.id,
    kind: "citation",
    title: item.title,
    summary: item.note,
    tags: [item.citationType, item.jurisdiction, item.sourceStatus, item.useWhen, ...item.tags],
    record: item,
  }));

  const templateItems: ResourceItem[] = draftTemplates.map((item) => ({
    id: item.id,
    kind: "template",
    title: item.title,
    summary: item.summary,
    tags: [item.templateType, item.purpose, item.sourceStatus, ...item.components.map((component) => component.label)],
    record: item,
  }));

  const checklistItems: ResourceItem[] = draftingChecklists.map((item) => ({
    id: item.id,
    kind: "checklist",
    title: item.title,
    summary: item.scope,
    tags: [item.scope, item.stage, ...item.appliesTo],
    record: item,
  }));

  const guideItems: ResourceItem[] = draftSectionGuides.map((item) => ({
    id: item.id,
    kind: "guide",
    title: item.label,
    summary: item.description,
    tags: [item.key, item.plainMeaning, item.avoid],
    record: item,
  }));

  return [...citationItems, ...templateItems, ...checklistItems, ...guideItems];
}

function FilterChip({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      className={active ? `${styles.filterChip} ${styles.filterChipActive}` : styles.filterChip}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

export default function CitationsDraftingPage() {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<ResourceFilter>("all");
  const [selectedId, setSelectedId] = useState<string>(citationExamples[0]?.id ?? "");

  const resources = useMemo(() => buildResources(), []);

  const filteredResources = useMemo(() => {
    const needle = query.trim().toLowerCase();

    return resources.filter((item) => {
      const filterMatch = filter === "all" ? true : item.kind === filter;
      if (!filterMatch) return false;
      if (!needle) return true;

      const haystack = [item.title, item.summary, ...item.tags].join(" ").toLowerCase();
      return haystack.includes(needle);
    });
  }, [filter, query, resources]);

  const selectedResource = useMemo(() => {
    return filteredResources.find((item) => item.id === selectedId) ?? filteredResources[0] ?? null;
  }, [filteredResources, selectedId]);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.workspace}>
            <div className={styles.topBar}>
              <div>
                <div className={styles.sectionEyebrow}>Citations & Drafting</div>
                <p className={`${styles.sectionText} ${styles.topBarText}`}>
                  Explore citation formats, educational drafting templates, and structure guides in
                  one compact legal-information workspace.
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
                  <div className={styles.sectionEyebrow}>Search and browse</div>
                  <h1>Citation lookup and drafting guidance</h1>
                  <p className={styles.sectionText}>
                    Browse citation formats, drafting templates, checklists, and section guides in one place.
                  </p>
                </div>
                <span className={styles.resultCount}>{filteredResources.length} resources</span>
              </div>

              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search statutes, sections, templates, petitions, affidavits..."
                className={styles.searchInput}
              />

              <div className={styles.filterRow}>
                {FILTERS.map((item) => (
                  <FilterChip
                    key={item.key}
                    active={filter === item.key}
                    label={item.label}
                    onClick={() => setFilter(item.key)}
                  />
                ))}
              </div>

              <div className={styles.quickStats}>
                <div className={styles.statCard}>
                  <strong>{citationExamples.length}</strong>
                  <span>Citation examples</span>
                </div>
                <div className={styles.statCard}>
                  <strong>{draftTemplates.length}</strong>
                  <span>Draft templates</span>
                </div>
                <div className={styles.statCard}>
                  <strong>{draftingChecklists.length}</strong>
                  <span>Checklists</span>
                </div>
                <div className={styles.statCard}>
                  <strong>{draftSectionGuides.length}</strong>
                  <span>Section guides</span>
                </div>
              </div>

              <div className={styles.primerGrid}>
                <div className={styles.primerCard}>
                  <strong>What a citation does</strong>
                  <span>Identifies the legal source, pinpoint reference, and publication context.</span>
                </div>
                <div className={styles.primerCard}>
                  <strong>How drafts are organized</strong>
                  <span>Separates parties, facts, grounds, requested relief, and supporting record.</span>
                </div>
                <div className={styles.primerCard}>
                  <strong>Data status</strong>
                  <span>Examples here are educational structures prepared for later verified-source hookup.</span>
                </div>
              </div>
            </section>

            <section className={styles.listPanel}>
              <div className={styles.listHeader}>
                <div className={styles.sectionEyebrow}>Resources</div>
                <p className={styles.sectionText}>
                  Select a card to inspect the format, template structure, or checklist in more detail.
                </p>
              </div>

              {filteredResources.length === 0 ? (
                <div className={styles.emptyState}>
                  No results match this search. Try a broader keyword like <strong>notice</strong>,{" "}
                  <strong>section</strong>, or <strong>petition</strong>.
                </div>
              ) : (
                <div className={styles.resourceList}>
                  {filteredResources.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      className={
                        item.id === selectedResource?.id
                          ? `${styles.resourceCard} ${styles.resourceCardActive}`
                          : styles.resourceCard
                      }
                      onClick={() => setSelectedId(item.id)}
                    >
                      <div className={styles.resourceMeta}>
                        <span className={styles.kindBadge}>{item.kind}</span>
                        <span className={styles.tagLine}>{item.tags[0]}</span>
                      </div>
                      <h2>{item.title}</h2>
                      <p>{item.summary}</p>
                      <div className={styles.tagRow}>
                        {item.tags.slice(0, 3).map((tag, index) => (
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
              <div className={styles.sectionEyebrow}>Selected detail</div>
              <h2>{selectedResource?.title ?? "Choose a resource"}</h2>
            </div>

            {!selectedResource ? (
              <div className={styles.emptyState}>
                Choose a citation example, template, checklist, or section guide to review it here.
              </div>
            ) : selectedResource.kind === "citation" ? (
              <article className={styles.detailCard}>
                <div className={styles.detailLead}>
                  <span className={styles.kindBadge}>citation</span>
                  <p className={styles.detailText}>
                    Educational format example for referencing legal materials more consistently.
                  </p>
                </div>
                <div className={styles.detailMetaGrid}>
                  <div className={styles.metaItem}>
                    <strong>Type</strong>
                    <span>{selectedResource.record.citationType}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Jurisdiction</strong>
                    <span>{selectedResource.record.jurisdiction}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Data status</strong>
                    <span>{selectedResource.record.sourceStatus}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Use when</strong>
                    <span>{selectedResource.record.useWhen}</span>
                  </div>
                </div>
                <div className={styles.exampleBlock}>
                  <div className={styles.sectionEyebrow}>Format example</div>
                  <code>{selectedResource.record.example}</code>
                </div>
                <div className={styles.detailSection}>
                  <h3>Citation parts</h3>
                  <div className={styles.componentGrid}>
                    {selectedResource.record.citationParts.map((part) => (
                      <div key={`${selectedResource.record.id}-${part.label}`} className={styles.componentItem}>
                        <strong>{part.label}</strong>
                        <span>{part.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className={styles.detailSection}>
                  <h3>Common mistakes</h3>
                  <div className={styles.bulletList}>
                    {selectedResource.record.commonMistakes.map((item) => (
                      <div key={item}>{item}</div>
                    ))}
                  </div>
                </div>
                <div className={styles.detailText}>{selectedResource.record.note}</div>
                <div className={styles.sourceNote}>{selectedResource.record.sourceNote}</div>
              </article>
            ) : selectedResource.kind === "template" ? (
              <article className={styles.detailCard}>
                <div className={styles.detailLead}>
                  <span className={styles.kindBadge}>template</span>
                  <p className={styles.detailText}>
                    Use this as a structure guide, not a personalized legal draft.
                  </p>
                </div>
                <div className={styles.detailMetaGrid}>
                  <div className={styles.metaItem}>
                    <strong>Template type</strong>
                    <span>{selectedResource.record.templateType}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Purpose</strong>
                    <span>{selectedResource.record.purpose}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Data status</strong>
                    <span>{selectedResource.record.sourceStatus}</span>
                  </div>
                </div>
                <div className={styles.exampleBlock}>
                  <div className={styles.sectionEyebrow}>Sample opening</div>
                  <code>{selectedResource.record.sampleOpening}</code>
                </div>
                <div className={styles.detailSection}>
                  <h3>Core components</h3>
                  <div className={styles.componentGrid}>
                    {selectedResource.record.components.map((component) => (
                      <div key={`${selectedResource.record.id}-${component.label}`} className={styles.componentItem}>
                        <strong>{component.label}</strong>
                        <span>{component.purpose}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className={styles.detailSection}>
                  <h3>Suggested structure</h3>
                  <div className={styles.stackList}>
                    {selectedResource.record.sections.map((item) => (
                      <div key={item} className={styles.stackItem}>
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
                <div className={styles.detailSection}>
                  <h3>Checklist</h3>
                  <div className={styles.bulletList}>
                    {selectedResource.record.checklist.map((item) => (
                      <div key={item}>{item}</div>
                    ))}
                  </div>
                </div>
                <div className={styles.sourceNote}>{selectedResource.record.educationalBoundary}</div>
              </article>
            ) : selectedResource.kind === "checklist" ? (
              <article className={styles.detailCard}>
                <div className={styles.detailLead}>
                  <span className={styles.kindBadge}>checklist</span>
                  <p className={styles.detailText}>
                    Quick drafting review points for educational document preparation.
                  </p>
                </div>
                <div className={styles.metaItem}>
                  <strong>Scope</strong>
                  <span>{selectedResource.record.scope}</span>
                </div>
                <div className={styles.detailMetaGrid}>
                  <div className={styles.metaItem}>
                    <strong>Stage</strong>
                    <span>{selectedResource.record.stage}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <strong>Applies to</strong>
                    <span>{selectedResource.record.appliesTo.join(", ")}</span>
                  </div>
                </div>
                <div className={styles.detailSection}>
                  <h3>Checklist items</h3>
                  <div className={styles.bulletList}>
                    {selectedResource.record.items.map((item) => (
                      <div key={item}>{item}</div>
                    ))}
                  </div>
                </div>
              </article>
            ) : (
              <article className={styles.detailCard}>
                <div className={styles.detailLead}>
                  <span className={styles.kindBadge}>section guide</span>
                  <p className={styles.detailText}>
                    Breakdown of a common draft component and what it is meant to do.
                  </p>
                </div>
                <div className={styles.metaItem}>
                  <strong>Section key</strong>
                  <span>{selectedResource.record.key}</span>
                </div>
                <div className={styles.metaItem}>
                  <strong>Plain meaning</strong>
                  <span>{selectedResource.record.plainMeaning}</span>
                </div>
                <div className={styles.detailText}>{selectedResource.record.description}</div>
                <div className={styles.exampleBlock}>
                  <div className={styles.sectionEyebrow}>Drafting hint</div>
                  <p>{selectedResource.record.draftingHint}</p>
                </div>
                <div className={styles.sourceNote}>Avoid: {selectedResource.record.avoid}</div>
              </article>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}
