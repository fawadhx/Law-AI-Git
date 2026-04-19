import { normalizeComparable } from "@/lib/research-utils";

export type CompareField = {
  label: string;
  left: string | number | boolean | null | undefined;
  right: string | number | boolean | null | undefined;
};

type ComparePanelProps = {
  title?: string;
  leftTitle: string;
  rightTitle?: string;
  fields: CompareField[];
};

export function ComparePanel({
  title = "Side-by-side comparison",
  leftTitle,
  rightTitle,
  fields,
}: ComparePanelProps) {
  return (
    <section className="research-card">
      <div className="research-card-header">
        <div className="research-eyebrow">Compare</div>
        <h3>{title}</h3>
      </div>

      {!rightTitle ? (
        <p className="research-muted">Choose another record to compare against the selected item.</p>
      ) : (
        <div className="compare-grid">
          <div className="compare-title">{leftTitle}</div>
          <div className="compare-title">{rightTitle}</div>
          {fields.map((field) => {
            const same = normalizeComparable(field.left) === normalizeComparable(field.right);
            return (
              <div key={field.label} className="compare-row">
                <div>
                  <strong>{field.label}</strong>
                  <span>{field.left || "Not listed"}</span>
                </div>
                <div>
                  <strong>{same ? "Same" : "Different"}</strong>
                  <span>{field.right || "Not listed"}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
