import Link from "next/link";

export type RelatedPanelItem = {
  id: string;
  title: string;
  subtitle?: string;
  tags?: string[];
  href?: string;
  onSelect?: () => void;
};

type RelatedItemsPanelProps = {
  title?: string;
  items: RelatedPanelItem[];
};

export function RelatedItemsPanel({ title = "Related records", items }: RelatedItemsPanelProps) {
  return (
    <section className="research-card">
      <div className="research-card-header">
        <div className="research-eyebrow">Related</div>
        <h3>{title}</h3>
      </div>
      {items.length === 0 ? (
        <p className="research-muted">No closely related records are available in this current dataset.</p>
      ) : (
        <div className="related-list">
          {items.map((item) => {
            const content = (
              <>
                <strong>{item.title}</strong>
                {item.subtitle ? <span>{item.subtitle}</span> : null}
                {item.tags?.length ? <small>{item.tags.slice(0, 3).join(" / ")}</small> : null}
              </>
            );

            if (item.onSelect) {
              return (
                <button key={item.id} type="button" className="related-item" onClick={item.onSelect}>
                  {content}
                </button>
              );
            }

            return (
              <Link key={item.id} href={item.href ?? "#"} className="related-item">
                {content}
              </Link>
            );
          })}
        </div>
      )}
    </section>
  );
}
