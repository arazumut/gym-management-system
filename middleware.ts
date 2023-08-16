import { withAuth, NextRequestWithAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

// ADMIN OR TRAINER
/**
 * ADD USER
 * STUDETNS
 * STUDENTS/[STUDENT]
 * FEES
 * EXERCISE
 * EXERCISE/ASSIGN-EXERCISE
 * EXERCISE/MANAGE-EXERCISE
 *
 * DIET
 * DIET/ASSIGN-DIET
 * DIET/MANAGE-FOOD
 *
 * NOTIFICATIONS
 * PROFILE
 *
 */

// STUDENT
/**
 * PROFILE
 * NOTIFICATIONS
 * USER/FEE
 * USER/EXERCISE
 * USER/DIET
 */

export default withAuth(
  function middleware(request: NextRequestWithAuth) {
    console.log(request.nextUrl.pathname);

    const user =
      request.nextauth.token?.role === "user" &&
      (request.nextUrl.pathname.startsWith("/exercise") ||
        request.nextUrl.pathname.startsWith("/diet") ||
        request.nextUrl.pathname.startsWith("/fees") ||
        request.nextUrl.pathname.startsWith("/add-user") ||
        request.nextUrl.pathname.startsWith("/students"));

    if (user) {
      return NextResponse.rewrite(new URL("/unauthorized", request.url));
    }

    const adminOrTrainer =
      request.nextUrl.pathname.startsWith("/user") &&
      request.nextauth.token?.role !== "user";

    if (adminOrTrainer) {
      return NextResponse.rewrite(new URL("/unauthorized", request.url));
    }
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
);

export const config = {
  matcher: [
    "/",
    "/api",
    "/add-user",
    "/profile",
    "/notiifcations",
    "/students/:path*",
    "/trainers/:path*",
    "/fees",
    "/exercise/:path*",
    "/diet/:path*",
    "/user/:path*",
  ],
};
