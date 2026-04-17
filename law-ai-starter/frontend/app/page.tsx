import Link from "next/link";
import styles from "./page.module.css";

const trendingTopics = [
  "Traffic Stop Rights",
  "Public Records Access",
  "Tenant Protections",
];

const rightsCards = [
  {
    icon: "PI",
    title: "Police Interactions",
    text: "Verified information on your rights during stops, searches, and detentions.",
  },
  {
    icon: "HT",
    title: "Housing & Tenancy",
    text: "Essential information on eviction processes, security deposits, and habitability laws.",
  },
  {
    icon: "CR",
    title: "Consumer Rights",
    text: "Understanding warranties, refund policies, and protection against deceptive practices.",
  },
  {
    icon: "EL",
    title: "Employment Law",
    text: "Workplace safety, wage theft, discrimination, and fair labor standard information.",
  },
];

const trustPoints = [
  {
    title: "Direct Source Citations",
    text: "Every piece of information links back to the original statute or case law.",
  },
  {
    title: "Regularly Audited Content",
    text: "Our database is updated weekly to reflect new legislative changes and rulings.",
  },
  {
    title: "Neutral Authority",
    text: "We provide objective information without bias or advocacy.",
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <section className={styles.noticeBar}>
        <div className={styles.shell}>
          <span className={styles.noticeIcon}>i</span>
          <span>
            <strong>LEGAL INFORMATION ONLY:</strong> This platform provides automated legal
            information for transparency and literacy. It does not provide legal advice or
            create an attorney-client relationship.
          </span>
        </div>
      </section>

      <section className={styles.heroSection}>
        <div className={styles.shell}>
          <div className={styles.heroFrame}>
            <div className={styles.heroGrid}>
              <div className={styles.heroLeft}>
                <div className={styles.heroPill}>Empowering legal literacy</div>
                <h1>Legal Transparency for Every Citizen.</h1>
                <p className={styles.heroBody}>
                  Access verified legal information, understand officer authorities, and
                  navigate the law with confidence. LawBridge AI bridges the gap between
                  complex statutes and public understanding.
                </p>

                <form action="/chat" className={styles.searchBar}>
                  <span className={styles.searchIcon}>Q</span>
                  <input
                    name="q"
                    type="text"
                    placeholder="Ask about rights, police powers, or specific laws..."
                  />
                  <button type="submit">Search</button>
                </form>

                <div className={styles.trendingRow}>
                  <span className={styles.trendingLabel}>Trending:</span>
                  <div className={styles.trendingPills}>
                    {trendingTopics.map((item) => (
                      <Link key={item} href="/chat" className={styles.topicPill}>
                        {item}
                      </Link>
                    ))}
                  </div>
                </div>
              </div>

              <div className={styles.heroVisual}>
                <div className={styles.visualWindow} />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="rights" className={styles.section}>
        <div className={styles.shell}>
          <div className={styles.sectionHead}>
            <div>
              <h2>Know Your Rights</h2>
              <p>
                Clear, verified information on the most common legal interactions. Categorized
                for quick navigation and public awareness.
              </p>
            </div>

            <Link href="/chat" className={styles.sectionLink}>
              View All Categories <span>-&gt;</span>
            </Link>
          </div>

          <div className={styles.cardGrid}>
            {rightsCards.map((item) => (
              <article key={item.title} className={styles.infoCard}>
                <div className={styles.cardIcon}>{item.icon}</div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className={styles.trustSection}>
        <div className={styles.shell}>
          <div className={styles.trustGrid}>
            <div className={styles.trustCopy}>
              <h2>Government-Grade Trust, Modern Accessibility.</h2>
              <p className={styles.trustLead}>
                We source data directly from official legislative records, department
                policies, and court precedents. Every answer is cited and verified by legal
                professionals.
              </p>

              <div className={styles.trustList}>
                {trustPoints.map((item) => (
                  <div key={item.title} className={styles.trustItem}>
                    <div className={styles.checkCircle}>OK</div>
                    <div>
                      <div className={styles.trustItemTitle}>{item.title}</div>
                      <div className={styles.trustItemText}>{item.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.authorityPanel}>
              <div className={styles.panelChrome}>
                <span />
                <span />
                <span />
              </div>
              <div className={styles.panelTitle}>Live Authority Search</div>

              <div className={styles.authorityCard}>
                <div className={styles.authorityHeader}>
                  <div>Officer Authority: Detainment</div>
                  <span>Verified</span>
                </div>
                <p>Does an officer have the right to detain you without reasonable suspicion?</p>

                <div className={styles.authorityMeta}>
                  <div className={styles.answerBlock}>
                    <strong>No</strong>
                    <span>Requires articulable facts of criminal activity.</span>
                  </div>
                  <div className={styles.basisBlock}>
                    <strong>Legal Basis</strong>
                    <span>Terry v. Ohio, 392 U.S. 1 (1968)</span>
                  </div>
                </div>
              </div>

              <div className={styles.referenceCard}>
                <div className={styles.referenceHeader}>
                  <span>Officer Authority: Search</span>
                  <em>Reference</em>
                </div>
                <div className={styles.referenceLine} />
                <div className={`${styles.referenceLine} ${styles.referenceLineShort}`} />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
