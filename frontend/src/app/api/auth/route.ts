import { NextResponse } from "next/server";

export async function POST(request: Request) {
    const { password } = await request.json();
    const serverPassword = process.env.ADMIN_ACCESS_PASSWORD;

    if (password === serverPassword) {
        // Password matches! Create a response and set a secure cookie
        const response = NextResponse.json({ success: true });

        // Cookie expires in 7 days. httpOnly prevents XSS attacks.
        response.cookies.set("nf_auth_token", "authorized", {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            maxAge: 60 * 60 * 24 * 7,
            path: "/",
        });

        return response;
    }

    // Password failed
    return NextResponse.json(
        { success: false, message: "Invalid access code." },
        { status: 401 }
    );
}