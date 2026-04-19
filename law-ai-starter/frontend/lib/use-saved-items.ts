"use client";

import { useCallback, useEffect, useState } from "react";
import {
  SAVED_ITEMS_STORAGE_KEY,
  readSavedItems,
  removeSavedItem,
  type SavedItem,
  upsertSavedItem,
  writeSavedItems,
} from "@/lib/saved-items";

export function useSavedItems() {
  const [items, setItems] = useState<SavedItem[]>([]);

  useEffect(() => {
    setItems(readSavedItems());

    function handleStorage(event: StorageEvent) {
      if (event.key === SAVED_ITEMS_STORAGE_KEY) {
        setItems(readSavedItems());
      }
    }

    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  const persist = useCallback((nextItems: SavedItem[]) => {
    setItems(nextItems);
    writeSavedItems(nextItems);
  }, []);

  const save = useCallback(
    (item: SavedItem) => {
      setItems((current) => {
        const nextItems = upsertSavedItem(current, item);
        writeSavedItems(nextItems);
        return nextItems;
      });
    },
    [],
  );

  const remove = useCallback((id: string) => {
    setItems((current) => {
      const nextItems = removeSavedItem(current, id);
      writeSavedItems(nextItems);
      return nextItems;
    });
  }, []);

  const isSaved = useCallback((id: string) => items.some((item) => item.id === id), [items]);

  const toggle = useCallback(
    (item: SavedItem) => {
      if (isSaved(item.id)) {
        remove(item.id);
        return;
      }
      save(item);
    },
    [isSaved, remove, save],
  );

  return { items, isSaved, persist, remove, save, toggle };
}
