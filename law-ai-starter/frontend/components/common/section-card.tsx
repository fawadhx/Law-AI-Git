import Link from "next/link";
import type { ReactNode } from "react";

type SectionCardProps = {
  title: string;
  text: string;
  href?: string;
  icon?: ReactNode;
  eyebrow?: string;
  className?: string;
};

export function SectionCard({ title, text, href, icon, eyebrow, className }: SectionCardProps) {
  const content = (
    <>
      {icon ? <div className="section-card-icon">{icon}</div> : null}
      {eyebrow ? <div className="section-card-eyebrow">{eyebrow}</div> : null}
      <h3>{title}</h3>
      <p>{text}</p>
    </>
  );

  if (href) {
    return (
      <Link href={href} className={className}>
        {content}
      </Link>
    );
  }

  return <div className={className}>{content}</div>;
}
