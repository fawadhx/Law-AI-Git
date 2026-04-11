export type Citation = {
  title: string;
  section: string;
  note: string;
};

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export type ChatResponse = {
  answer: string;
  disclaimer: string;
  citations: Citation[];
};
