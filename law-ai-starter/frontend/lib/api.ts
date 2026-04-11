import type { ChatResponse } from "@/types/chat";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function askLawQuestion(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch legal response.");
  }

  return response.json();
}
