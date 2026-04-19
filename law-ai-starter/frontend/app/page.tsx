import Link from "next/link";
import type { ReactNode } from "react";
import { SectionCard } from "@/components/common/section-card";
import styles from "./page.module.css";

type RightsCard = {
  title: string;
  text: string;
  eyebrow: string;
  icon: ReactNode;
};

const rightsCards: RightsCard[] = [
  {
    title: "Police Interactions",
    eyebrow: "Public Safety",
    text: "Understand common questions around stopping, questioning, detention, and documentation requests in Pakistan.",
    icon: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 3.5 18 6v5.7c0 3.8-2.4 7.2-6 8.8-3.6-1.6-6-5-6-8.8V6l6-2.5Z" />
      </svg>
    ),
  },
  {
    title: "Housing & Tenancy",
    eyebrow: "Everyday Rights",
    text: "Explore rent agreements, eviction process basics, landlord obligations, and local tenancy-related rules.",
    icon: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-4.5v-5h-5v5H5a1 1 0 0 1-1-1v-9.5Z" />
      </svg>
    ),
  },
  {
    title: "Consumer Rights",
    eyebrow: "Transactions",
    text: "Get information on unfair practices, complaint pathways, product disputes, and buyer protections.",
    icon: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M6 6h15l-1.5 7.5H9L7.2 5H4" />
        <circle cx="10" cy="19" r="1.7" />
        <circle cx="18" cy="19" r="1.7" />
      </svg>
    ),
  },
  {
    title: "Employment & Wages",
    eyebrow: "Workplace",
    text: "Review pay, working conditions, notice, and labor-related information in a clearer public format.",
    icon: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 8.5A1.5 1.5 0 0 1 5.5 7h13A1.5 1.5 0 0 1 20 8.5V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V8.5Z" />
        <path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7" />
      </svg>
    ),
  },
];

const trendingTopics = [
  {
    label: "FIR and complaint process",
    href: `/chat?q=${encodeURIComponent("FIR and complaint process")}`,
  },
  {
    label: "Officer authority lookup",
    href: "/officer-authority",
  },
  {
    label: "Citation formats",
    href: "/citations-drafting",
  },
  {
    label: "Case order summaries",
    href: "/case-studies",
  },
];

const trustPoints = [
  {
    title: "Official-source focus",
    text: "The platform is designed to point people toward statutes, rules, and government source material rather than opinion-led summaries.",
  },
  {
    title: "Jurisdiction-aware structure",
    text: "Federal and provincial material can be separated clearly so users understand which legal layer they are exploring.",
  },
  {
    title: "Review before publish",
    text: "Admin workflows are built around validation, staged publishing, and traceable source metadata before material is surfaced more broadly.",
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <section className={styles.heroSection}>
        <div className={styles.shell}>
          <div className={styles.heroGrid}>
            <div className={styles.heroCopy}>
              <div className={styles.heroPill}>Pakistan legal information, made clearer</div>
              <h1>Search Pakistan legal information quickly.</h1>
              <p className={styles.heroBody}>
                Start with a question, authority lookup, citation format, or case/order summary
                and move directly into the working tools.
              </p>

              <form action="/chat" method="get" className={styles.searchCard}>
                <label htmlFor="home-search" className={styles.searchLabel}>
                  Ask about rights, police powers, tenancy, or public legal procedures
                </label>
                <div className={styles.searchRow}>
                  <input
                    id="home-search"
                    name="q"
                    className={styles.searchInput}
                    placeholder="Ask a legal-information question..."
                  />
                  <button type="submit" className={styles.searchButton}>
                    Start Chat
                  </button>
                </div>
              </form>

              <div className={styles.trendingRow}>
                <span className={styles.trendingLabel}>Trending</span>
                <div className={styles.trendingChips}>
                  {trendingTopics.map((topic) => (
                    <Link
                      key={topic.label}
                      href={topic.href}
                      className={styles.trendingChip}
                    >
                      {topic.label}
                    </Link>
                  ))}
                </div>
              </div>

              <div className={styles.heroActions}>
                <Link href="/chat" className={styles.primaryLink}>
                  Open Legal Chat
                </Link>
                <Link href="/officer-authority" className={styles.secondaryLink}>
                  Explore Officer Authority
                </Link>
              </div>
            </div>

            <div className={styles.heroPanel}>
              <div className={styles.previewFrame}>
                <div className={styles.previewChrome}>
                  <span />
                  <span />
                  <span />
                </div>
                <div className={styles.previewCard}>
                  <div className={styles.previewLabel}>Example workspace</div>
                  <h2>Search result preview</h2>
                  <div className={styles.previewQuery}>
                    Can police ask for identification during a public stop?
                  </div>

                  <div className={styles.previewResponse}>
                    <div className={styles.previewResponseHead}>
                      <span className={styles.previewType}>Legal information</span>
                      <span className={styles.verifiedTag}>Source-backed</span>
                    </div>
                    <p>
                      Responses are designed to summarize the question, show confidence and
                      category context, and point users toward the relevant legal-source trail.
                    </p>
                  </div>

                  <div className={styles.previewMetaGrid}>
                    <div className={styles.metaCard}>
                      <strong>Jurisdiction</strong>
                      <span>Pakistan</span>
                    </div>
                    <div className={styles.metaCard}>
                      <strong>Source trail</strong>
                      <span>Acts, rules, official references</span>
                    </div>
                  </div>

                  <div className={styles.referenceCard}>
                    <div className={styles.referenceRow}>
                      <span>Linked materials</span>
                      <span className={styles.referenceTag}>Traceable</span>
                    </div>
                    <div className={styles.referenceItem}>
                      <span className={styles.referenceTitle}>Officer authority references</span>
                      <span className={styles.referenceMeta}>Public legal-information view</span>
                    </div>
                    <div className={styles.referenceItem}>
                      <span className={styles.referenceTitle}>Source-management review</span>
                      <span className={styles.referenceMeta}>Admin-controlled publishing flow</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.shell}>
          <div className={styles.sectionHead}>
            <div>
              <h2>Know Your Rights</h2>
              <p>
                Clearer public-facing entry points for the legal questions people ask most often.
                Structured for Pakistan-focused legal awareness and faster navigation.
              </p>
            </div>

            <Link href="/chat" className={styles.sectionLink}>
              Explore in Chat <span>-&gt;</span>
            </Link>
          </div>

          <div className={styles.rightsGrid}>
            {rightsCards.map((item) => (
              <SectionCard
                key={item.title}
                title={item.title}
                text={item.text}
                icon={item.icon}
                eyebrow={item.eyebrow}
                href="/chat"
                className={styles.rightCard}
              />
            ))}
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.shell}>
          <div className={styles.trustSection}>
            <div className={styles.trustCopy}>
              <h2>Trust signals that stay close to the product.</h2>
              <p className={styles.trustLead}>
                The goal is not to imitate a law firm website. It is to make structured legal
                information easier to understand, easier to trace, and easier to review as the
                Pakistan law corpus grows.
              </p>

              <div className={styles.trustList}>
                {trustPoints.map((item) => (
                  <div key={item.title} className={styles.trustItem}>
                    <div className={styles.trustCheck}>+</div>
                    <div>
                      <div className={styles.trustItemTitle}>{item.title}</div>
                      <div className={styles.trustItemText}>{item.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.heroPanel}>
              <div className={styles.trustPanel}>
                <div className={styles.trustPanelHeader}>
                  <span>Source management</span>
                  <span className={styles.referenceTag}>Review flow</span>
                </div>

                <div className={styles.trustPanelCard}>
                  <div className={styles.trustPanelTitleRow}>
                    <span>Imported law record</span>
                    <span className={styles.verifiedTag}>Under review</span>
                  </div>
                  <p>
                    Records can retain title, jurisdiction, source URL, citation details,
                    language, cleaned text, and structured sections before wider use.
                  </p>
                  <div className={styles.previewMetaGrid}>
                    <div className={styles.metaCard}>
                      <strong>Jurisdiction</strong>
                      <span>Federal / Provincial</span>
                    </div>
                    <div className={styles.metaCard}>
                      <strong>Provenance</strong>
                      <span>Official-source first</span>
                    </div>
                  </div>
                </div>

                <div className={styles.referenceCard}>
                  <div className={styles.referenceRow}>
                    <span>Review checkpoints</span>
                    <span className={styles.referenceTag}>Reference</span>
                  </div>
                  <div className={styles.referenceChecklist}>
                    <div className={styles.referenceChecklistItem}>Source URL and citation details</div>
                    <div className={styles.referenceChecklistItem}>Jurisdiction and law type</div>
                    <div className={styles.referenceChecklistItem}>Structured sections before retrieval use</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.closingSection}>
        <div className={styles.shell}>
          <div className={styles.boundaryCard}>
            <h2>Open the working areas</h2>
            <p>
              Move from overview into guided chat, officer authority lookup, or the admin
              console that supports source review and publication workflows.
            </p>

            <div className={styles.heroActions}>
              <Link href="/chat" className={styles.primaryLink}>
                Continue to Chat
              </Link>
              <Link href="/admin" className={styles.secondaryLink}>
                Open Admin Console
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
