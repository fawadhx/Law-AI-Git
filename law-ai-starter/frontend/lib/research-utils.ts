export type RelatedCandidate = {
  id: string;
};

export type ResearchSummaryInput = {
  title: string;
  subtitle?: string;
  summary?: string;
  fields?: Array<[string, string | number | boolean | null | undefined]>;
  tags?: string[];
};

export async function copyTextToClipboard(text: string): Promise<boolean> {
  const normalized = text.trim();
  if (!normalized) return false;

  try {
    if (typeof navigator !== "undefined" && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(normalized);
      return true;
    }
  } catch {
    return false;
  }

  return false;
}

export function formatResearchSummary(input: ResearchSummaryInput): string {
  const lines = [input.title.trim()];

  if (input.subtitle?.trim()) {
    lines.push(input.subtitle.trim());
  }

  if (input.summary?.trim()) {
    lines.push("", input.summary.trim());
  }

  const fields = (input.fields ?? []).filter(([, value]) => value !== undefined && value !== null && `${value}`.trim());
  if (fields.length) {
    lines.push("", "Key details:");
    fields.forEach(([label, value]) => {
      lines.push(`- ${label}: ${value}`);
    });
  }

  if (input.tags?.length) {
    lines.push("", `Tags: ${input.tags.join(", ")}`);
  }

  return lines.join("\n");
}

export function createTagRelatedItems<T extends RelatedCandidate>(
  items: T[],
  current: T | null,
  getTags: (item: T) => string[],
  limit: number = 3,
): T[] {
  if (!current) return [];

  const currentTags = new Set(getTags(current).map(normalizeToken).filter(Boolean));
  if (currentTags.size === 0) return [];

  return items
    .filter((item) => item.id !== current.id)
    .map((item) => {
      const score = getTags(item).reduce((total, tag) => {
        return total + (currentTags.has(normalizeToken(tag)) ? 1 : 0);
      }, 0);
      return { item, score };
    })
    .filter((entry) => entry.score > 0)
    .sort((first, second) => second.score - first.score)
    .slice(0, limit)
    .map((entry) => entry.item);
}

export function normalizeComparable(value: string | number | boolean | null | undefined): string {
  if (value === undefined || value === null) return "";
  return String(value).trim().toLowerCase();
}

function normalizeToken(value: string): string {
  return value.trim().toLowerCase();
}
