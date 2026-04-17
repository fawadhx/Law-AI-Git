import Link from "next/link";
import styles from "./page.module.css";

const rightsCards = [
  {
    title: "Police Interactions",
    text: "Verified information on your rights during stops, searches, and detentions.",
  },
  {
    title: "Housing & Tenancy",
    text: "Essential information on eviction processes, security deposits, and habitability laws.",
  },
  {
    title: "Consumer Rights",
    text: "Understanding warranties, refund policies, and protection against deceptive practices.",
  },
  {
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
          <div className={styles.heroGrid}>
            <div className={styles.heroCopy}>
              <div className={styles.heroPill}>Empowering legal literacy</div>
              <h1>Legal Transparency for Every Citizen.</h1>
              <p className={styles.heroBody}>
                Access verified legal information, understand officer authorities, and navigate
                the law with confidence. Law AI helps bridge the gap between complex statutes
                and public understanding.
              </p>

              <div className={styles.heroActions}>
                <Link href="/chat" className={styles.primaryLink}>
                  Open Legal Chat
                </Link>
                <Link href="/admin" className={styles.secondaryLink}>
                  View Admin Prototype
                </Link>
              </div>
            </div>

            <div className={styles.heroPanel}>
              <div className={styles.visualCard}>
                <div className={styles.visualCardLabel}>Live authority search</div>
                <div className={styles.visualResultCard}>
                  <div className={styles.visualResultHead}>
                    <span>Officer Authority: Detainment</span>
                    <span className={styles.verifiedTag}>Verified</span>
                  </div>
                  <p>Does an officer have the right to detain you without reasonable suspicion?</p>
                  <div className={styles.visualResultGrid}>
                    <div className={styles.answerBox}>
                      <strong>No</strong>
                      <span>Requires articulable facts of criminal activity.</span>
                    </div>
                    <div className={styles.basisBox}>
                      <strong>Legal Basis</strong>
                      <span>Terry v. Ohio, 392 U.S. 1 (1968)</span>
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
                Clear, verified information on the most common legal interactions. Categorized
                for quick navigation and public awareness.
              </p>
            </div>

            <Link href="/chat" className={styles.sectionLink}>
              View All Categories <span>-&gt;</span>
            </Link>
          </div>

          <div className={styles.rightsGrid}>
            {rightsCards.map((item) => (
              <article key={item.title} className={styles.rightCard}>
                <div className={styles.cardIcon}>{item.title.slice(0, 2)}</div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.shell}>
          <div className={styles.trustSection}>
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
                    <div className={styles.trustCheck}>OK</div>
                    <div>
                      <div className={styles.trustItemTitle}>{item.title}</div>
                      <div className={styles.trustItemText}>{item.text}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.heroPanel}>
              <div className={styles.visualCard}>
                <div className={styles.visualCardLabel}>Live authority search</div>
                <div className={styles.visualResultCard}>
                  <div className={styles.visualResultHead}>
                    <span>Officer Authority: Detainment</span>
                    <span className={styles.verifiedTag}>Verified</span>
                  </div>
                  <p>Does an officer have the right to detain you without reasonable suspicion?</p>
                  <div className={styles.visualResultGrid}>
                    <div className={styles.answerBox}>
                      <strong>No</strong>
                      <span>Requires articulable facts of criminal activity.</span>
                    </div>
                    <div className={styles.basisBox}>
                      <strong>Legal Basis</strong>
                      <span>Terry v. Ohio, 392 U.S. 1 (1968)</span>
                    </div>
                  </div>
                </div>

                <div className={styles.referenceCard}>
                  <div className={styles.referenceRow}>
                    <span>Officer Authority: Search</span>
                    <span className={styles.referenceTag}>Reference</span>
                  </div>
                  <div className={styles.referenceLine} />
                  <div className={`${styles.referenceLine} ${styles.referenceLineShort}`} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.closingSection}>
        <div className={styles.shell}>
          <div className={styles.boundaryCard}>
            <h2>Important legal boundary</h2>
            <p>
              This product is intended for legal information, public awareness, and structured
              law exploration. It should not claim to replace a licensed lawyer, court filing
              strategy, or professional legal representation.
            </p>

            <div className={styles.heroActions}>
              <Link href="/chat" className={styles.primaryLink}>
                Continue to Chat
              </Link>
              <Link href="/officer-authority" className={styles.secondaryLink}>
                Explore Officer Authority
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
