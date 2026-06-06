import { ReactNode } from "react";

export function Card({
    children,
    className = ""
}: Readonly<{
    children: ReactNode,
    className?: string
}>) {
    return (
        <div className={`p-6 bg-zinc-900/50 border border-zinc-800 rounded-xl ${className}`}>
            {children}
        </div>
    );
}