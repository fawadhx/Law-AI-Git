export const SAVED_ITEMS_STORAGE_KEY = "law-ai-saved-items-v1";

export type SavedItemType =
  | "chat"
  | "officer-authority"
  | "citation"
  | "draft-template"
  | "draft-checklist"
  | "draft-guide"
  | "case-study";

export type SavedItem = {
  id: string;
  type: SavedItemType;
  title: string;
  subtitle: string;
  summary: string;
  href: string;
  tags: string[];
  metadata: Record<string, string | number | boolean>;
  sourceId: string;
  savedAt: string;
};

export const savedItemTypeLabels: Record<SavedItemType, string> = {
  chat: "Chat answers",
  "officer-authority": "Officer authority",
  citation: "Citation examples",
  "draft-template": "Draft templates",
  "draft-checklist": "Draft checklists",
  "draft-guide": "Draft guides",
  "case-study": "Case studies",
};

export function createStableHash(input: string): string {
  let hash = 0;
  for (let index = 0; index < input.length; index += 1) {
    hash = (hash << 5) - hash + input.charCodeAt(index);
    hash |= 0;
  }
  return Math.abs(hash).toString(36);
}

export function readSavedItems(): SavedItem[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = window.localStorage.getItem(SAVED_ITEMS_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(isSavedItem);
  } catch {
    return [];
  }
}

export function writeSavedItems(items: SavedItem[]): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(SAVED_ITEMS_STORAGE_KEY, JSON.stringify(items));
}

export function upsertSavedItem(items: SavedItem[], item: SavedItem): SavedItem[] {
  const withoutCurrent = items.filter((current) => current.id !== item.id);
  return [{ ...item, savedAt: new Date().toISOString() }, ...withoutCurrent];
}

export function removeSavedItem(items: SavedItem[], id: string): SavedItem[] {
  return items.filter((item) => item.id !== id);
}

function isSavedItem(value: unknown): value is SavedItem {
  if (!value || typeof value !== "object") return false;
  const item = value as Partial<SavedItem>;
  return (
    typeof item.id === "string" &&
    typeof item.type === "string" &&
    typeof item.title === "string" &&
    typeof item.subtitle === "string" &&
    typeof item.summary === "string" &&
    typeof item.href === "string" &&
    Array.isArray(item.tags) &&
    typeof item.metadata === "object" &&
    item.metadata !== null &&
    typeof item.sourceId === "string" &&
    typeof item.savedAt === "string"
  );
}
