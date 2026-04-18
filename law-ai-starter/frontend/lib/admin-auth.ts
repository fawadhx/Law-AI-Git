import { API_BASE_URL } from "@/lib/runtime-config";

const ADMIN_TOKEN_KEY = "law-ai-admin-access-token";
const ADMIN_TOKEN_COOKIE = "law_ai_admin_token";

export type AdminSessionUser = {
  username: string;
  display_name: string;
  role: string;
};

export type AdminLoginResponse = {
  access_token: string;
  token_type: string;
  expires_in_seconds: number;
  admin: AdminSessionUser;
};

export type AdminMeResponse = {
  authenticated: boolean;
  admin: AdminSessionUser;
};

async function readApiError(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.clone().json();
    if (payload && typeof payload.detail === "string" && payload.detail.trim()) {
      const boundaryNote =
        typeof payload.boundary_note === "string" && payload.boundary_note.trim()
          ? ` ${payload.boundary_note.trim()}`
          : "";
      return `${payload.detail.trim()}${boundaryNote}`.trim();
    }
  } catch {
    // Ignore JSON parsing errors and keep falling back.
  }

  try {
    const text = (await response.text()).trim();
    if (text) {
      return text;
    }
  } catch {
    // Ignore text parsing errors and use the fallback.
  }

  return fallback;
}

export async function loginAdmin(username: string, password: string): Promise<AdminLoginResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/auth/admin/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });
  } catch {
    throw new Error("Unable to reach the admin service right now. Please try again shortly.");
  }

  if (!response.ok) {
    throw new Error(await readApiError(response, "Invalid admin credentials."));
  }

  return response.json();
}

export async function fetchAdminMe(token: string): Promise<AdminMeResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/auth/admin/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });
  } catch {
    throw new Error("Unable to verify the admin session right now. Please sign in again.");
  }

  if (!response.ok) {
    throw new Error(await readApiError(response, "Admin session is not valid."));
  }

  return response.json();
}

export function getStoredAdminToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(ADMIN_TOKEN_KEY);
}

export function storeAdminToken(token: string) {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(ADMIN_TOKEN_KEY, token);
  document.cookie = `${ADMIN_TOKEN_COOKIE}=${encodeURIComponent(token)}; Path=/; SameSite=Lax`;
}

export function clearAdminToken() {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(ADMIN_TOKEN_KEY);
  document.cookie = `${ADMIN_TOKEN_COOKIE}=; Path=/; Max-Age=0; SameSite=Lax`;
}

export function roleAllowsAdminWrite(role: string | null | undefined) {
  return role === "admin";
}
