const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";
const ADMIN_TOKEN_KEY = "law-ai-admin-access-token";

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

export async function loginAdmin(username: string, password: string): Promise<AdminLoginResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/admin/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error("Invalid admin credentials.");
  }

  return response.json();
}

export async function fetchAdminMe(token: string): Promise<AdminMeResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/admin/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Admin session is not valid.");
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
}

export function clearAdminToken() {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(ADMIN_TOKEN_KEY);
}
