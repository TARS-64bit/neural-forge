import { ReactNode } from "react";

export function Card({
    children,
    className = ""
}: Readonly<{
    children: ReactNode,
    className?: string
}>) {
    return (
        <div className={`p-6 border border-white/10 shadow-[0_0_20px_rgba(0,0,0,0.8)] backdrop-blur-lg bg-black/50! rounded-xl ${className}`}>
            {children}
        </div>
    );
}