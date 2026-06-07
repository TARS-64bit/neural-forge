import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    // 1. Check if the user is trying to access the workspace
    if (request.nextUrl.pathname.startsWith('/workspace')) {

        // 2. Look for our specific cookie
        const hasWorkspace = request.cookies.has('nf_workspace_active');

        // 3. If missing, boot them back to the root page instantly
        if (!hasWorkspace) {
            return NextResponse.redirect(new URL('/', request.url));
        }
    }

    return NextResponse.next();
}

// 4. Tell Next.js to ONLY run this middleware on the workspace route
export const config = {
    matcher: ['/workspace/:path*'],
};