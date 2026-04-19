"use client";

import { useSavedItems } from "@/lib/use-saved-items";
import type { SavedItem } from "@/lib/saved-items";

type SaveButtonProps = {
  item: SavedItem | null;
  className?: string;
};

export function SaveButton({ item, className = "" }: SaveButtonProps) {
  const { isSaved, toggle } = useSavedItems();
  const saved = item ? isSaved(item.id) : false;
  const label = saved ? "Saved" : "Save";
  const classNames = ["save-button", saved ? "save-button-active" : "", className].filter(Boolean).join(" ");

  return (
    <button
      type="button"
      className={classNames}
      disabled={!item}
      aria-label={item ? `${saved ? "Remove saved" : "Save"} ${item.title}` : "Save unavailable"}
      onClick={() => {
        if (item) toggle(item);
      }}
    >
      <span aria-hidden="true">{saved ? "●" : "○"}</span>
      {label}
    </button>
  );
}
