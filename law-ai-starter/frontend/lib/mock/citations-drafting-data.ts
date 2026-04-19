export type ResearchDataStatus = "demo" | "verified" | "needs-source";

export type CitationPart = {
  label: string;
  value: string;
};

export type CitationExample = {
  id: string;
  title: string;
  citationType: "statute" | "section" | "rule" | "notification" | "case-citation";
  jurisdiction: string;
  sourceStatus: ResearchDataStatus;
  sourceNote: string;
  formatLabel: string;
  example: string;
  citationParts: CitationPart[];
  useWhen: string;
  commonMistakes: string[];
  note: string;
  tags: string[];
};

export type DraftComponent = {
  label: string;
  purpose: string;
};

export type DraftTemplate = {
  id: string;
  title: string;
  templateType: "complaint" | "notice" | "petition" | "affidavit";
  purpose: string;
  sourceStatus: ResearchDataStatus;
  educationalBoundary: string;
  summary: string;
  components: DraftComponent[];
  sections: string[];
  checklist: string[];
  sampleOpening: string;
};

export type DraftChecklist = {
  id: string;
  title: string;
  scope: string;
  stage: "before-drafting" | "review" | "submission";
  appliesTo: string[];
  items: string[];
};

export type DraftSectionGuide = {
  id: string;
  key: "heading" | "parties" | "facts" | "grounds" | "prayer" | "annexures";
  label: string;
  plainMeaning: string;
  description: string;
  draftingHint: string;
  avoid: string;
};

export const citationExamples: CitationExample[] = [
  {
    id: "crpc-1898-statute",
    title: "Statute title format",
    citationType: "statute",
    jurisdiction: "Pakistan federal law",
    sourceStatus: "demo",
    sourceNote: "Educational citation-format example; verify the latest official title from the relevant official source before use.",
    formatLabel: "Act / code title",
    example: "Code of Criminal Procedure, 1898",
    citationParts: [
      { label: "Instrument", value: "Code of Criminal Procedure" },
      { label: "Year", value: "1898" },
    ],
    useWhen: "Use when introducing a law or code for the first time in a research note or draft.",
    commonMistakes: ["Dropping the year from the first reference", "Using a short abbreviation before defining it"],
    note: "Use the full official title when first referencing a statute or code in educational legal writing.",
    tags: ["criminal procedure", "statute title"],
  },
  {
    id: "crpc-154-section",
    title: "Section reference format",
    citationType: "section",
    jurisdiction: "Pakistan federal law",
    sourceStatus: "demo",
    sourceNote: "Educational section-citation pattern; the section number should be checked against the current official text.",
    formatLabel: "Section citation",
    example: "Code of Criminal Procedure, 1898, s. 154",
    citationParts: [
      { label: "Instrument", value: "Code of Criminal Procedure, 1898" },
      { label: "Section", value: "s. 154" },
    ],
    useWhen: "Use when the research note or draft relies on a specific statutory section.",
    commonMistakes: ["Citing only the section number without the law name", "Mixing s., sec., and section inconsistently"],
    note: "Cite the statute name first, then the section. Short forms can be used only after the full form is already clear.",
    tags: ["FIR", "section reference"],
  },
  {
    id: "police-rules-rule",
    title: "Rule citation format",
    citationType: "rule",
    jurisdiction: "Pakistan police procedure",
    sourceStatus: "demo",
    sourceNote: "Educational rule-citation pattern; confirm whether the rule applies in the relevant jurisdiction and current version.",
    formatLabel: "Rule citation",
    example: "Police Rules, 1934, r. 25.2",
    citationParts: [
      { label: "Rules", value: "Police Rules, 1934" },
      { label: "Rule", value: "r. 25.2" },
    ],
    useWhen: "Use when referencing subordinate rules rather than an Act or Code section.",
    commonMistakes: ["Treating a rule citation as if it were an Act section", "Leaving out the rule number"],
    note: "Rules are usually cited by the instrument name followed by the rule number.",
    tags: ["police", "rules"],
  },
  {
    id: "gazette-notification",
    title: "Notification reference format",
    citationType: "notification",
    jurisdiction: "Official publication",
    sourceStatus: "demo",
    sourceNote: "Educational notification format; real notifications should be tied to the issuing authority and official publication details.",
    formatLabel: "Notification / gazette format",
    example: "Notification No. SO(ADMN) 3-9/2024, Gazette of Pakistan, 12 March 2024",
    citationParts: [
      { label: "Notification number", value: "Notification No. SO(ADMN) 3-9/2024" },
      { label: "Publication", value: "Gazette of Pakistan" },
      { label: "Date", value: "12 March 2024" },
    ],
    useWhen: "Use when citing an official notification, SRO, or Gazette-published administrative instrument.",
    commonMistakes: ["Omitting the notification number", "Not recording the issuing authority or publication date"],
    note: "Include the notification number, issuing source, and date where available.",
    tags: ["notification", "gazette"],
  },
  {
    id: "pld-case-citation",
    title: "Case citation format",
    citationType: "case-citation",
    jurisdiction: "Pakistan case-law reporting example",
    sourceStatus: "demo",
    sourceNote: "Educational citation-format example only; it is not a representation that the platform has verified the underlying case text.",
    formatLabel: "Reported case format",
    example: "PLD 1972 SC 139",
    citationParts: [
      { label: "Report series", value: "PLD" },
      { label: "Year", value: "1972" },
      { label: "Court", value: "SC" },
      { label: "Page", value: "139" },
    ],
    useWhen: "Use when identifying a reported decision by law-report reference.",
    commonMistakes: ["Confusing the court abbreviation with the party name", "Treating a citation format example as verified case content"],
    note: "This is an educational format example showing the report series, court abbreviation, and page number.",
    tags: ["reported cases", "citation style"],
  },
];

export const draftTemplates: DraftTemplate[] = [
  {
    id: "complaint-application",
    title: "Complaint / application structure",
    templateType: "complaint",
    purpose: "Basic complaint or public-facing application guidance",
    sourceStatus: "demo",
    educationalBoundary: "Template guidance only; users should adapt structure to the relevant forum and should not treat it as personalized advice.",
    summary:
      "Use a short heading, identify the parties or office addressed, state the relevant facts in sequence, and end with a clear request.",
    components: [
      { label: "Heading", purpose: "Identifies the document type and receiving authority." },
      { label: "Facts", purpose: "Sets out dates, place, parties, and incident sequence." },
      { label: "Relief sought", purpose: "States the action requested from the authority." },
    ],
    sections: ["Heading", "Parties / addressee", "Facts", "Relief sought", "Supporting documents"],
    checklist: [
      "Identify the correct office or authority",
      "State dates, names, and place details clearly",
      "Attach copies of relevant documents if available",
      "Keep the relief sought practical and specific",
    ],
    sampleOpening: "The applicant respectfully submits the following facts for consideration.",
  },
  {
    id: "legal-notice",
    title: "Notice structure",
    templateType: "notice",
    purpose: "Educational notice layout",
    sourceStatus: "demo",
    educationalBoundary: "This is a neutral structure guide and does not decide whether a notice is legally required in a specific matter.",
    summary:
      "A notice should identify the sender and recipient, summarize the issue, mention the basis of the complaint, and state the requested next step.",
    components: [
      { label: "Recipient details", purpose: "Shows who is being placed on record." },
      { label: "Issue summary", purpose: "Explains the dispute or request in short factual terms." },
      { label: "Response period", purpose: "Records the requested time frame for a response where appropriate." },
    ],
    sections: ["Sender / recipient", "Issue summary", "Factual background", "Demand or request", "Response period"],
    checklist: [
      "Confirm recipient details",
      "Keep the issue statement factual",
      "State any supporting documents relied on",
      "Use a clear response deadline where appropriate",
    ],
    sampleOpening: "This notice is issued to place the relevant facts and request on record.",
  },
  {
    id: "petition-format",
    title: "Petition structure",
    templateType: "petition",
    purpose: "Educational petition-format guidance",
    sourceStatus: "demo",
    educationalBoundary: "Petition formats vary by forum; this outlines common components only.",
    summary:
      "A petition-style structure usually separates facts, grounds, and prayer so the reader can track the legal and factual narrative more easily.",
    components: [
      { label: "Facts", purpose: "Provides a numbered factual background." },
      { label: "Grounds", purpose: "Separates legal or procedural objections from facts." },
      { label: "Prayer", purpose: "Lists the precise relief requested." },
    ],
    sections: ["Title / court heading", "Parties", "Facts", "Grounds", "Prayer", "Annexures"],
    checklist: [
      "Use a clear heading and case title format",
      "Separate facts from legal grounds",
      "Number paragraphs for readability",
      "List annexures in the same order they are referenced",
    ],
    sampleOpening: "The petitioner respectfully states as follows.",
  },
  {
    id: "affidavit-format",
    title: "Affidavit basic format guidance",
    templateType: "affidavit",
    purpose: "Educational affidavit outline",
    sourceStatus: "demo",
    educationalBoundary: "This is format guidance only; attestation and verification requirements can vary by forum and context.",
    summary:
      "An affidavit-style document usually identifies the deponent, states verified facts in numbered form, and ends with a verification section.",
    components: [
      { label: "Deponent details", purpose: "Identifies the person making the statement." },
      { label: "Numbered statements", purpose: "Keeps verified facts separated and readable." },
      { label: "Verification", purpose: "Records the affirmation/verification basis." },
    ],
    sections: ["Deponent details", "Numbered statements", "Verification", "Signatures / attestation"],
    checklist: [
      "Ensure the deponent is identified accurately",
      "Keep factual statements separate and numbered",
      "Include a verification clause",
      "Check local attestation requirements before use",
    ],
    sampleOpening: "I, the undersigned deponent, do hereby solemnly affirm the following.",
  },
];

export const draftingChecklists: DraftChecklist[] = [
  {
    id: "before-submission",
    title: "Before submission checklist",
    scope: "Complaint, application, and petition-style drafts",
    stage: "submission",
    appliesTo: ["complaint", "application", "petition"],
    items: [
      "Check names, dates, and place references for accuracy",
      "Make sure every attached document is mentioned in the draft",
      "Keep paragraphs short and ordered in sequence",
      "Review whether the request or prayer is clearly written",
    ],
  },
  {
    id: "citation-cleanup",
    title: "Citation cleanup checklist",
    scope: "Educational drafting review",
    stage: "review",
    appliesTo: ["citation", "petition", "notice"],
    items: [
      "Use full title on first reference to a law or rule",
      "Keep citation style consistent throughout the draft",
      "Avoid mixing abbreviations unless already defined",
      "Check whether sections, rules, and dates are complete",
    ],
  },
  {
    id: "supporting-record",
    title: "Supporting record checklist",
    scope: "Document readiness",
    stage: "before-drafting",
    appliesTo: ["annexures", "record index", "supporting documents"],
    items: [
      "List annexures in the same order they are discussed",
      "Ensure each attachment is labeled clearly",
      "Keep a simple index for multi-document sets",
      "Note any missing record that may matter to context",
    ],
  },
];

export const draftSectionGuides: DraftSectionGuide[] = [
  {
    id: "guide-heading",
    key: "heading",
    label: "Heading",
    plainMeaning: "The short label that tells the reader what document they are looking at.",
    description: "Use a short title that identifies the document type and, where needed, the forum or office addressed.",
    draftingHint: "Keep the heading functional and avoid unnecessary phrasing.",
    avoid: "Avoid long argumentative headings or unclear abbreviations.",
  },
  {
    id: "guide-parties",
    key: "parties",
    label: "Parties / Addressee",
    plainMeaning: "The people, office, authority, or forum connected to the document.",
    description: "Identify the sender, respondent, applicant, or office clearly so the reader knows who is involved.",
    draftingHint: "Use the same names consistently throughout the draft.",
    avoid: "Avoid changing names, spellings, or titles midway through the draft.",
  },
  {
    id: "guide-facts",
    key: "facts",
    label: "Facts",
    plainMeaning: "The factual story, usually in date or event order.",
    description: "Present the factual background in a short, chronological sequence.",
    draftingHint: "Separate factual background from argument or opinion.",
    avoid: "Avoid mixing allegations, opinions, and legal conclusions in the same paragraph.",
  },
  {
    id: "guide-grounds",
    key: "grounds",
    label: "Grounds",
    plainMeaning: "The reasons relied on for the request or objection.",
    description: "Explain the legal or procedural basis of the request in plain and organized language.",
    draftingHint: "Keep each ground distinct so it can be reviewed independently.",
    avoid: "Avoid repeating the facts without explaining why they matter.",
  },
  {
    id: "guide-prayer",
    key: "prayer",
    label: "Prayer / Relief sought",
    plainMeaning: "The result or direction requested from the authority or forum.",
    description: "State the exact action or outcome being requested from the receiving authority or forum.",
    draftingHint: "Write the requested relief in practical, concrete terms.",
    avoid: "Avoid vague requests that do not identify what action is being sought.",
  },
  {
    id: "guide-annexures",
    key: "annexures",
    label: "Annexures",
    plainMeaning: "The documents attached to support or explain the draft.",
    description: "List and label the supporting documents attached with the draft.",
    draftingHint: "Match annexure labels with the order they are mentioned in the document.",
    avoid: "Avoid attaching documents without explaining their relevance in the body.",
  },
];
