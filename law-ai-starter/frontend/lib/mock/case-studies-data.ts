export type CaseDataStatus = "demo-structure" | "verified-source" | "needs-source";

export type CaseTimelineEvent = {
  id: string;
  date: string;
  title: string;
  summary: string;
  eventType: "filing" | "hearing" | "order" | "record";
};

export type LinkedLawReference = {
  label: string;
  referenceType: "constitutional" | "statute" | "procedure" | "rules" | "general";
  note: string;
};

export type CaseStudyRecord = {
  id: string;
  title: string;
  citation: string;
  dataStatus: CaseDataStatus;
  sourceNote: string;
  sourceUrl: string | null;
  jurisdiction: string;
  courtLevel: string;
  court: string;
  bench: string;
  orderDate: string;
  orderType: string;
  proceduralPosture: string;
  summary: string;
  holding: string;
  outcome: string;
  disposition: string;
  legalIssues: string[];
  keyFacts: string[];
  researchUse: string;
  linkedProvisions: string[];
  linkedLawReferences: LinkedLawReference[];
  tags: string[];
  timeline: CaseTimelineEvent[];
};

export const caseStudyRecords: CaseStudyRecord[] = [
  {
    id: "lahore-bail-order",
    title: "Illustrative bail order study",
    citation: "Demo research note / Lahore High Court style order",
    dataStatus: "demo-structure",
    sourceNote:
      "Demo-only case research structure. Replace with verified order text, official citation, and source URL before treating as an authority record.",
    sourceUrl: null,
    jurisdiction: "Punjab / Pakistan",
    courtLevel: "High Court",
    court: "Lahore High Court",
    bench: "Single bench",
    orderDate: "2025-02-11",
    orderType: "Bail order",
    proceduralPosture: "Interim relief stage",
    summary:
      "This educational case study shows how an order can separate the allegation background, prosecution stance, and reasons for the interim result.",
    holding:
      "The order emphasized that the stage of proceedings, available record, and specific allegations matter when the court assesses interim liberty questions.",
    outcome: "Interim relief granted subject to conditions in the illustrative order summary.",
    disposition: "Relief granted for the limited interim purpose described in the demo record.",
    legalIssues: ["Interim liberty", "Available record", "Specific allegations"],
    keyFacts: [
      "Complaint and registration sequence appears in the record summary.",
      "The relief request is assessed at an interim stage, not final trial determination.",
    ],
    researchUse: "Useful for showing how bail/order summaries can separate facts, arguments, reasons, and result.",
    linkedProvisions: ["Code of Criminal Procedure, 1898", "Pakistan Penal Code, 1860"],
    linkedLawReferences: [
      {
        label: "Code of Criminal Procedure, 1898",
        referenceType: "procedure",
        note: "Procedure framework connected to bail and criminal-case process.",
      },
      {
        label: "Pakistan Penal Code, 1860",
        referenceType: "statute",
        note: "Substantive offence law referenced in many criminal-order records.",
      },
    ],
    tags: ["bail", "criminal procedure", "illustrative"],
    timeline: [
      {
        id: "lb-1",
        date: "2024-12-19",
        title: "Initial complaint context",
        summary: "The study begins with the complaint and registration sequence discussed in the record summary.",
        eventType: "record",
      },
      {
        id: "lb-2",
        date: "2025-01-22",
        title: "Arguments on relief",
        summary: "The parties' positions on interim relief were summarized before the order was announced.",
        eventType: "hearing",
      },
      {
        id: "lb-3",
        date: "2025-02-11",
        title: "Order announced",
        summary: "The court issued a short order and explained the immediate result in concise terms.",
        eventType: "order",
      },
    ],
  },
  {
    id: "islamabad-constitutional-order",
    title: "Illustrative constitutional petition order",
    citation: "Demo research note / Islamabad High Court style order",
    dataStatus: "demo-structure",
    sourceNote:
      "Demo-only research record for interface structure. It is not a verified case-law authority or official order reproduction.",
    sourceUrl: null,
    jurisdiction: "Islamabad Capital Territory / Pakistan",
    courtLevel: "High Court",
    court: "Islamabad High Court",
    bench: "Division bench",
    orderDate: "2025-03-05",
    orderType: "Interim constitutional order",
    proceduralPosture: "Preliminary hearing",
    summary:
      "This study focuses on how a court order can frame maintainability, public authority action, and interim directions without resolving the full case.",
    holding:
      "The order noted that interim directions depend on the immediate record, urgency, and whether the public action challenged is sufficiently identified.",
    outcome: "Notice issued and the matter fixed for a fuller hearing in the illustrative timeline.",
    disposition: "Notice and listing direction recorded for the demo procedural stage.",
    legalIssues: ["Maintainability", "Public authority action", "Interim direction"],
    keyFacts: [
      "The challenged public action is identified at the preliminary stage.",
      "The matter is not finally resolved in the interim order structure.",
    ],
    researchUse: "Useful for showing how constitutional-order summaries distinguish interim directions from final holdings.",
    linkedProvisions: ["Constitution of the Islamic Republic of Pakistan, 1973", "Public authority procedure"],
    linkedLawReferences: [
      {
        label: "Constitution of the Islamic Republic of Pakistan, 1973",
        referenceType: "constitutional",
        note: "Constitutional framework referenced in rights/public-authority matters.",
      },
      {
        label: "Public authority procedure",
        referenceType: "general",
        note: "General procedural context for public authority action.",
      },
    ],
    tags: ["constitutional", "interim order", "administrative action"],
    timeline: [
      {
        id: "ihc-1",
        date: "2025-02-26",
        title: "Petition filed",
        summary: "The petitioner challenged a public decision and requested interim protective directions.",
        eventType: "filing",
      },
      {
        id: "ihc-2",
        date: "2025-03-05",
        title: "Preliminary hearing",
        summary: "The bench heard opening submissions on maintainability and interim urgency.",
        eventType: "hearing",
      },
      {
        id: "ihc-3",
        date: "2025-03-05",
        title: "Notice and listing order",
        summary: "The matter was listed for a later date after notice and limited interim directions.",
        eventType: "order",
      },
    ],
  },
  {
    id: "service-tribunal-order",
    title: "Illustrative service matter order",
    citation: "Demo research note / Service tribunal summary",
    dataStatus: "demo-structure",
    sourceNote:
      "Demo-only tribunal-order structure. Replace with verified tribunal/court source material before using as a real case record.",
    sourceUrl: null,
    jurisdiction: "Pakistan",
    courtLevel: "Tribunal",
    court: "Service Tribunal",
    bench: "Two-member bench",
    orderDate: "2024-11-28",
    orderType: "Final order",
    proceduralPosture: "Final decision stage",
    summary:
      "This example shows how a final service-related order may frame facts, departmental record, and relief in a more structured way than an interim order.",
    holding:
      "The order turned on the documentary service record and whether the challenged action was supported by the material placed before the tribunal.",
    outcome: "Matter remanded for reconsideration in the educational order summary.",
    disposition: "Remand-style outcome described for educational structure only.",
    legalIssues: ["Departmental record", "Administrative decision", "Remand direction"],
    keyFacts: [
      "The challenged order and departmental correspondence are central to the record.",
      "The decision turns on whether the material supports the administrative action.",
    ],
    researchUse: "Useful for showing how final-order summaries can identify record, reasoning, and operative direction.",
    linkedProvisions: ["Service rules", "Departmental procedure"],
    linkedLawReferences: [
      {
        label: "Service rules",
        referenceType: "rules",
        note: "Rules or service framework relevant to employment/service disputes.",
      },
      {
        label: "Departmental procedure",
        referenceType: "procedure",
        note: "Internal decision-making process considered in service matters.",
      },
    ],
    tags: ["service law", "tribunal", "final order"],
    timeline: [
      {
        id: "st-1",
        date: "2024-09-09",
        title: "Appeal record assembled",
        summary: "The file included departmental correspondence and the challenged order.",
        eventType: "record",
      },
      {
        id: "st-2",
        date: "2024-10-21",
        title: "Hearing concluded",
        summary: "The bench reserved the matter after hearing both sides on the record.",
        eventType: "hearing",
      },
      {
        id: "st-3",
        date: "2024-11-28",
        title: "Final order released",
        summary: "The tribunal issued a final structured order explaining the outcome and next procedural step.",
        eventType: "order",
      },
    ],
  },
  {
    id: "consumer-forum-order",
    title: "Illustrative consumer forum order",
    citation: "Demo research note / Consumer dispute order",
    dataStatus: "demo-structure",
    sourceNote:
      "Demo-only consumer-order structure for research UI development. It is not a verified official order.",
    sourceUrl: null,
    jurisdiction: "Pakistan / provincial consumer forum context",
    courtLevel: "Forum",
    court: "Consumer court / forum",
    bench: "Presiding officer",
    orderDate: "2025-01-17",
    orderType: "Consumer complaint order",
    proceduralPosture: "Complaint disposition stage",
    summary:
      "This example highlights how a consumer order may summarize the complaint, response, documentary record, and the reasoning behind compensation or dismissal.",
    holding:
      "The order focused on the record available, the nature of the transaction, and whether the respondent's conduct fit the complaint narrative.",
    outcome: "Partial relief described in the illustrative order study.",
    disposition: "Partial-relief structure shown for educational purposes only.",
    legalIssues: ["Complaint record", "Transaction documents", "Relief assessment"],
    keyFacts: [
      "Transaction documents and complaint narrative are the primary record points.",
      "The respondent response is compared against the complainant record.",
    ],
    researchUse: "Useful for showing how forum orders can organize complaint, response, record, and disposition.",
    linkedProvisions: ["Consumer protection law", "Complaint procedure"],
    linkedLawReferences: [
      {
        label: "Consumer protection law",
        referenceType: "statute",
        note: "Consumer protection framework varies by jurisdiction and source.",
      },
      {
        label: "Complaint procedure",
        referenceType: "procedure",
        note: "Procedural path for filing and responding to consumer complaints.",
      },
    ],
    tags: ["consumer rights", "complaint", "forum order"],
    timeline: [
      {
        id: "cf-1",
        date: "2024-12-02",
        title: "Complaint lodged",
        summary: "The complainant submitted transaction documents and the requested relief.",
        eventType: "filing",
      },
      {
        id: "cf-2",
        date: "2024-12-19",
        title: "Response filed",
        summary: "The respondent disputed the complaint and attached its own record.",
        eventType: "record",
      },
      {
        id: "cf-3",
        date: "2025-01-17",
        title: "Order issued",
        summary: "The forum issued a short educationally summarized order setting out the disposition.",
        eventType: "order",
      },
    ],
  },
];
