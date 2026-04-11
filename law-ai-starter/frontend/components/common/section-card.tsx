type SectionCardProps = {
  title: string;
  text: string;
};

export function SectionCard({ title, text }: SectionCardProps) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p className="muted">{text}</p>
    </div>
  );
}
