"use client";

import { useEffect, useMemo, useState } from "react";
import { ComparePanel, type CompareField } from "@/components/common/compare-panel";
import { CopySummaryButton } from "@/components/common/copy-summary-button";
import { RelatedItemsPanel } from "@/components/common/related-items-panel";
import { SaveButton } from "@/components/common/save-button";
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
import {
  ALL_OPTION,
  activeFilterCount,
  listOptionMatches,
  matchesSearchQuery,
  optionMatches,
  resultCountLabel,
  uniqueOptions,
  uniqueOptionsFromLists,
} from "@/lib/search-filter";
import { createTagRelatedItems, formatResearchSummary } from "@/lib/research-utils";
import type { SavedItem, SavedItemType } from "@/lib/saved-items";
import styles from "./page.module.css";

type ResourceFilter = "all" | "citation" | "template" | "checklist" | "guide";

type ResourceItem =
  | {
      id: string;
      kind: "citation";
      title: string;
      summary: string;
      tags: string[];
      citationType: string;
      jurisdiction: string;
      dataStatus: string;
      record: CitationExample;
    }
  | {
      id: string;
      kind: "template";
      title: string;
      summary: string;
      tags: string[];
      templateType: string;
      dataStatus: string;
      record: DraftTemplate;
    }
  | {
      id: string;
      kind: "checklist";
      title: string;
      summary: string;
      tags: string[];
      checklistStage: string;
      appliesTo: string[];
      record: DraftChecklist;
    }
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
    citationType: item.citationType,
    jurisdiction: item.jurisdiction,
    dataStatus: item.sourceStatus,
    record: item,
  }));

  const templateItems: ResourceItem[] = draftTemplates.map((item) => ({
    id: item.id,
    kind: "template",
    title: item.title,
    summary: item.summary,
    tags: [item.templateType, item.purpose, item.sourceStatus, ...item.components.map((component) => component.label)],
    templateType: item.templateType,
    dataStatus: item.sourceStatus,
    record: item,
  }));

  const checklistItems: ResourceItem[] = draftingChecklists.map((item) => ({
    id: item.id,
    kind: "checklist",
    title: item.title,
    summary: item.scope,
    tags: [item.scope, item.stage, ...item.appliesTo],
    checklistStage: item.stage,
    appliesTo: item.appliesTo,
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

function getSavedResourceType(item: ResourceItem): SavedItemType {
  if (item.kind === "citation") return "citation";
  if (item.kind === "template") return "draft-template";
  if (item.kind === "checklist") return "draft-checklist";
  return "draft-guide";
}

function createSavedResource(item: ResourceItem | null): SavedItem | null {
  if (!item) return null;
  const type = getSavedResourceType(item);
  return {
    id: `${type}:${item.id}`,
    type,
    title: item.title,
    subtitle: item.kind,
    summary: item.summary,
    href: "/citations-drafting",
    tags: item.tags.slice(0, 5),
    metadata: {
      kind: item.kind,
      primaryTag: item.tags[0] || "",
    },
    sourceId: item.id,
    savedAt: new Date().toISOString(),
  };
}

function getResourceTags(item: ResourceItem): string[] {
  const structuralTags =
    item.kind === "citation"
      ? [item.kind, item.citationType, item.jurisdiction, item.dataStatus]
      : item.kind === "template"
        ? [item.kind, item.templateType, item.dataStatus]
        : item.kind === "checklist"
          ? [item.kind, item.checklistStage, ...item.appliesTo]
          : [item.kind];
  return [...structuralTags, ...item.tags];
}

function createResourceSummary(item: ResourceItem | null): string {
  if (!item) return "";
  const fields: Array<[string, string]> = [["Type", item.kind]];

  if (item.kind === "citation") {
    fields.push(
      ["Citation type", item.citationType],
      ["Jurisdiction", item.jurisdiction],
      ["Data status", item.dataStatus],
      ["Example", item.record.example],
    );
  }

  if (item.kind === "template") {
    fields.push(
      ["Template type", item.templateType],
      ["Purpose", item.record.purpose],
      ["Data status", item.dataStatus],
    );
  }

  if (item.kind === "checklist") {
    fields.push(
      ["Stage", item.checklistStage],
      ["Applies to", item.appliesTo.join(", ")],
    );
  }

  if (item.kind === "guide") {
    fields.push(["Section key", item.record.key], ["Plain meaning", item.record.plainMeaning]);
  }

  return formatResearchSummary({
    title: item.title,
    subtitle: "Citations & Drafting research resource",
    summary: item.summary,
    fields,
    tags: item.tags.slice(0, 6),
  });
}

function createResourceCompareFields(left: ResourceItem | null, right: ResourceItem | null): CompareField[] {
  const leftStatus = left && "dataStatus" in left ? left.dataStatus : "";
  const rightStatus = right && "dataStatus" in right ? right.dataStatus : "";
  return [
    { label: "Resource type", left: left?.kind, right: right?.kind },
    { label: "Primary tag", left: left?.tags[0], right: right?.tags[0] },
    { label: "Data status", left: leftStatus, right: rightStatus },
    { label: "Summary", left: left?.summary, right: right?.summary },
  ];
}

export default function CitationsDraftingPage() {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<ResourceFilter>("all");
  const [citationTypeFilter, setCitationTypeFilter] = useState("All citation types");
  const [jurisdictionFilter, setJurisdictionFilter] = useState("All jurisdictions");
  const [statusFilter, setStatusFilter] = useState("All statuses");
  const [templateTypeFilter, setTemplateTypeFilter] = useState("All template types");
  const [stageFilter, setStageFilter] = useState("All stages");
  const [appliesToFilter, setAppliesToFilter] = useState("All applies-to tags");
  const [selectedId, setSelectedId] = useState<string>(citationExamples[0]?.id ?? "");
  const [compareId, setCompareId] = useState("");
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  const resources = useMemo(() => buildResources(), []);

  const citationTypeOptions = useMemo(
    () => uniqueOptions(citationExamples.map((item) => item.citationType), "All citation types"),
    [],
  );
  const jurisdictionOptions = useMemo(
    () => uniqueOptions(citationExamples.map((item) => item.jurisdiction), "All jurisdictions"),
    [],
  );
  const statusOptions = useMemo(
    () => uniqueOptions(
      [
        ...citationExamples.map((item) => item.sourceStatus),
        ...draftTemplates.map((item) => item.sourceStatus),
      ],
      "All statuses",
    ),
    [],
  );
  const templateTypeOptions = useMemo(
    () => uniqueOptions(draftTemplates.map((item) => item.templateType), "All template types"),
    [],
  );
  const stageOptions = useMemo(
    () => uniqueOptions(draftingChecklists.map((item) => item.stage), "All stages"),
    [],
  );
  const appliesToOptions = useMemo(
    () => uniqueOptionsFromLists(draftingChecklists.map((item) => item.appliesTo), "All applies-to tags"),
    [],
  );

  const activeFilters = activeFilterCount(
    {
      citationTypeFilter,
      jurisdictionFilter,
      statusFilter,
      templateTypeFilter,
      stageFilter,
      appliesToFilter,
      resourceType: filter === "all" ? ALL_OPTION : filter,
    },
    [
      ALL_OPTION,
      "all",
      "All citation types",
      "All jurisdictions",
      "All statuses",
      "All template types",
      "All stages",
      "All applies-to tags",
    ],
  );

  function resetFilters() {
    setQuery("");
    setFilter("all");
    setCitationTypeFilter("All citation types");
    setJurisdictionFilter("All jurisdictions");
    setStatusFilter("All statuses");
    setTemplateTypeFilter("All template types");
    setStageFilter("All stages");
    setAppliesToFilter("All applies-to tags");
  }

  const filteredResources = useMemo(() => {
    return resources.filter((item) => {
      const filterMatch = filter === "all" ? true : item.kind === filter;
      if (!filterMatch) return false;
      if (item.kind !== "citation" && citationTypeFilter !== "All citation types") return false;
      if (item.kind === "citation" && !optionMatches(citationTypeFilter, item.citationType, "All citation types")) {
        return false;
      }
      if (item.kind !== "citation" && jurisdictionFilter !== "All jurisdictions") return false;
      if (item.kind === "citation" && !optionMatches(jurisdictionFilter, item.jurisdiction, "All jurisdictions")) {
        return false;
      }
      if (!["citation", "template"].includes(item.kind) && statusFilter !== "All statuses") return false;
      if ("dataStatus" in item && !optionMatches(statusFilter, item.dataStatus, "All statuses")) return false;
      if (item.kind !== "template" && templateTypeFilter !== "All template types") return false;
      if (item.kind === "template" && !optionMatches(templateTypeFilter, item.templateType, "All template types")) {
        return false;
      }
      if (item.kind !== "checklist" && stageFilter !== "All stages") return false;
      if (item.kind === "checklist" && !optionMatches(stageFilter, item.checklistStage, "All stages")) return false;
      if (item.kind !== "checklist" && appliesToFilter !== "All applies-to tags") return false;
      if (item.kind === "checklist" && !listOptionMatches(appliesToFilter, item.appliesTo, "All applies-to tags")) {
        return false;
      }

      return matchesSearchQuery(query, [item.title, item.summary, ...item.tags]);
    });
  }, [
    appliesToFilter,
    citationTypeFilter,
    filter,
    jurisdictionFilter,
    query,
    resources,
    stageFilter,
    statusFilter,
    templateTypeFilter,
  ]);

  const selectedResource = useMemo(() => {
    return filteredResources.find((item) => item.id === selectedId) ?? filteredResources[0] ?? null;
  }, [filteredResources, selectedId]);

  useEffect(() => {
    if (filteredResources.length === 0) return;
    if (filteredResources.some((item) => item.id === selectedId)) return;
    setSelectedId(filteredResources[0].id);
  }, [filteredResources, selectedId]);

  const savedResource = useMemo(() => createSavedResource(selectedResource), [selectedResource]);
  const compareResource = useMemo(() => resources.find((item) => item.id === compareId) ?? null, [compareId, resources]);
  const relatedResources = useMemo(
    () => createTagRelatedItems(resources, selectedResource, getResourceTags, 3),
    [resources, selectedResource],
  );
  const selectedSummary = useMemo(() => createResourceSummary(selectedResource), [selectedResource]);

  return (
    <main className={styles.page}>
      <div className={styles.shell}>
        <div className={styles.layoutGrid}>
          <section className={styles.workspace}>
            <div className={styles.topBar}>
              <div>
                <div className={styles.sectionEyebrow}>Citations & Drafting</div>
                <p className={`${styles.sectionText} ${styles.topBarText}`}>
                  Search citation examples, templates, checklists, and drafting structure guides.
                </p>
              </div>
            </div>

            <section className={styles.controlCard}>
              <div className={styles.controlHead}>
                <div>
                  <div className={styles.sectionEyebrow}>Search and browse</div>
                  <h1>Citation and drafting resources</h1>
                  <p className={styles.sectionText}>
                    Start with search, then narrow with resource type or advanced filters.
                  </p>
                </div>
                <span className={styles.resultCount}>{resultCountLabel(filteredResources.length, "resource")}</span>
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
                <div className={styles.advancedFilters}>
                  <label className={styles.selectField}>
                    <span>Citation type</span>
                    <select value={citationTypeFilter} onChange={(event) => setCitationTypeFilter(event.target.value)}>
                      {citationTypeOptions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Jurisdiction</span>
                    <select value={jurisdictionFilter} onChange={(event) => setJurisdictionFilter(event.target.value)}>
                      {jurisdictionOptions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Data status</span>
                    <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
                      {statusOptions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Template type</span>
                    <select value={templateTypeFilter} onChange={(event) => setTemplateTypeFilter(event.target.value)}>
                      {templateTypeOptions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Checklist stage</span>
                    <select value={stageFilter} onChange={(event) => setStageFilter(event.target.value)}>
                      {stageOptions.map((item) => (
                        <option key={item} value={item}>
                          {item}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className={styles.selectField}>
                    <span>Applies to</span>
                    <select value={appliesToFilter} onChange={(event) => setAppliesToFilter(event.target.value)}>
                      {appliesToOptions.map((item) => (
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
                  <strong>No resources match your filters.</strong> Try <span>notice</span>,{" "}
                  <span>section</span>, or <span>petition</span>, or{" "}
                  <button type="button" onClick={resetFilters}>
                    reset filters
                  </button>
                  .
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
              <div>
                <div className={styles.sectionEyebrow}>Selected detail</div>
                <h2>{selectedResource?.title ?? "Choose a resource"}</h2>
              </div>
              <SaveButton item={savedResource} />
            </div>

            {!selectedResource ? (
              <div className={styles.emptyState}>
                Choose a citation example, template, checklist, or section guide to review it here.
              </div>
            ) : (
              <>
                <article className={styles.detailCard}>
                  <div className={styles.detailLead}>
                    <div className={styles.kindBadge}>{selectedResource.kind}</div>
                    <p className={styles.detailText}>{selectedResource.summary}</p>
                  </div>
                  <div className={styles.tagRow}>
                    {selectedResource.tags.slice(0, 5).map((tag, index) => (
                      <span key={`${selectedResource.id}-summary-${tag}-${index}`} className={styles.tagChip}>
                        {tag}
                      </span>
                    ))}
                  </div>
                </article>

                <section className={styles.utilityPanel}>
                  <div className={styles.detailHeader}>
                    <div>
                      <div className={styles.sectionEyebrow}>Research utilities</div>
                      <p className={styles.detailText}>Copy this summary, or compare only when needed.</p>
                    </div>
                    <CopySummaryButton text={selectedSummary} />
                  </div>
                  <details className={styles.utilityDetails}>
                    <summary>Compare and related resources</summary>
                    <label className={styles.selectField}>
                      <span>Compare with</span>
                      <select value={compareId} onChange={(event) => setCompareId(event.target.value)}>
                        <option value="">Choose another resource</option>
                        {resources
                          .filter((item) => item.id !== selectedResource.id)
                          .map((item) => (
                            <option key={item.id} value={item.id}>
                              {item.title}
                            </option>
                          ))}
                      </select>
                    </label>
                    <ComparePanel
                      leftTitle={selectedResource.title}
                      rightTitle={compareResource?.title}
                      fields={createResourceCompareFields(selectedResource, compareResource)}
                    />
                    <RelatedItemsPanel
                      items={relatedResources.map((item) => ({
                        id: item.id,
                        title: item.title,
                        subtitle: item.kind,
                        tags: item.tags,
                        onSelect: () => setSelectedId(item.id),
                      }))}
                    />
                  </details>
                </section>

                {selectedResource.kind === "citation" ? (
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
              </>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}
