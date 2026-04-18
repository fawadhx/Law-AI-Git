import { describe, expect, it } from "vitest";
import { NextRequest } from "next/server";

import { middleware } from "@/middleware";

describe("admin middleware", () => {
  it("redirects unauthenticated admin requests to the login page", () => {
    const request = new NextRequest("http://localhost:3000/admin");
    const response = middleware(request);

    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("http://localhost:3000/admin/login?next=%2Fadmin");
  });

  it("allows the admin login route without a token", () => {
    const request = new NextRequest("http://localhost:3000/admin/login");
    const response = middleware(request);

    expect(response.headers.get("location")).toBeNull();
  });

  it("allows authenticated admin requests when the token cookie is present", () => {
    const request = new NextRequest("http://localhost:3000/admin");
    request.cookies.set("law_ai_admin_token", "test-token");

    const response = middleware(request);

    expect(response.headers.get("location")).toBeNull();
  });
});
