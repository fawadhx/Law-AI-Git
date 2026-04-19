import { describe, expect, it } from "vitest";
import { createTagRelatedItems, formatResearchSummary } from "@/lib/research-utils";

describe("research utilities", () => {
  it("creates bounded related matches without returning the current item", () => {
    const items = [
      { id: "a", tags: ["FIR", "procedure"] },
      { id: "b", tags: ["procedure", "arrest"] },
      { id: "c", tags: ["tenancy"] },
      { id: "d", tags: ["FIR"] },
    ];

    const related = createTagRelatedItems(items, items[0], (item) => item.tags, 2);

    expect(related.map((item) => item.id)).toEqual(["b", "d"]);
  });

  it("formats a readable research summary", () => {
    const summary = formatResearchSummary({
      title: "Section reference format",
      subtitle: "Citation resource",
      summary: "A short summary.",
      fields: [["Type", "section"]],
      tags: ["FIR", "citation"],
    });

    expect(summary).toContain("Section reference format");
    expect(summary).toContain("- Type: section");
    expect(summary).toContain("Tags: FIR, citation");
  });
});
