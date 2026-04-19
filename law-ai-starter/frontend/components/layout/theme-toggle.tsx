"use client";

import { useEffect, useState } from "react";

const THEME_STORAGE_KEY = "law-ai-theme";

type ThemeMode = "light" | "dark";

function applyTheme(mode: ThemeMode) {
  document.documentElement.dataset.theme = mode;
  window.localStorage.setItem(THEME_STORAGE_KEY, mode);
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<ThemeMode>("light");
  const nextTheme = theme === "light" ? "dark" : "light";

  useEffect(() => {
    const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
    const resolvedTheme: ThemeMode = storedTheme === "dark" ? "dark" : "light";
    setTheme(resolvedTheme);
    applyTheme(resolvedTheme);
  }, []);

  function handleToggle() {
    const updatedTheme: ThemeMode = theme === "light" ? "dark" : "light";
    setTheme(updatedTheme);
    applyTheme(updatedTheme);
  }

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={handleToggle}
      aria-label={`Switch to ${nextTheme} mode`}
      title={`Switch to ${nextTheme} mode`}
    >
      <span className="theme-toggle-icon" aria-hidden="true">
        {theme === "light" ? "◐" : "○"}
      </span>
    </button>
  );
}
