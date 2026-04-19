export const ALL_OPTION = "All";

export function normalizeSearchText(value: string | number | null | undefined): string {
  return String(value ?? "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\s\-\/&]/g, " ")
    .replace(/\s+/g, " ");
}

export function matchesSearchQuery(query: string, values: Array<string | number | null | undefined>): boolean {
  const needle = normalizeSearchText(query);
  if (!needle) return true;

  const haystack = normalizeSearchText(values.filter(Boolean).join(" "));
  return needle
    .split(" ")
    .filter(Boolean)
    .every((term) => haystack.includes(term));
}

export function uniqueOptions(values: Array<string | null | undefined>, allLabel = ALL_OPTION): string[] {
  const unique = Array.from(
    new Set(values.map((value) => String(value ?? "").trim()).filter(Boolean)),
  ).sort((left, right) => left.localeCompare(right));

  return [allLabel, ...unique];
}

export function uniqueOptionsFromLists(values: string[][], allLabel = ALL_OPTION): string[] {
  return uniqueOptions(values.flat(), allLabel);
}

export function optionMatches(selected: string, value: string | null | undefined, allLabel = ALL_OPTION): boolean {
  return selected === allLabel || String(value ?? "") === selected;
}

export function listOptionMatches(selected: string, values: string[], allLabel = ALL_OPTION): boolean {
  return selected === allLabel || values.includes(selected);
}

export function activeFilterCount(filters: Record<string, string>, allLabels: string[] = [ALL_OPTION]): number {
  return Object.values(filters).filter((value) => value && !allLabels.includes(value)).length;
}

export function resultCountLabel(count: number, singular: string, plural = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : plural}`;
}
