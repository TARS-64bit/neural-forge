import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const pathname = request.nextUrl.pathname;
    const isAuthenticated = request.cookies.has("nf_auth_token");
    const isLoginPage = pathname.startsWith("/login");

    // 1. AUTH GUARD: If NOT logged in and not on the login page -> Redirect to /login
    if (!isAuthenticated && !isLoginPage) {
        return NextResponse.redirect(new URL("/login", request.url));
    }

    // 2. LOGIN REDIRECT: If they ARE logged in and try to go to the login page -> Redirect to /
    if (isAuthenticated && isLoginPage) {
        return NextResponse.redirect(new URL("/", request.url));
    }

    // 3. WORKSPACE GUARD: Check if they are trying to access the workspace
    if (pathname.startsWith('/workspace')) {
        const hasWorkspace = request.cookies.has('nf_workspace_active');

        // If they don't have an active workspace, boot them back to the Setup page
        if (!hasWorkspace) {
            return NextResponse.redirect(new URL('/', request.url));
        }
    }

    return NextResponse.next();
}

// 4. MATCHER: Run on ALL routes EXCEPT api routes, static files, and images
export const config = {
    matcher: [
        '/((?!api|_next/static|_next/image|favicon.ico).*)',
    ],
};