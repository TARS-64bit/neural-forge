import { InputHTMLAttributes, ReactNode } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label: string;
    icon?: ReactNode;
}

export function Input({ label, icon, className = "", ...props }: Readonly<InputProps>) {
    return (
        <div className={`space-y-2 ${className}`}>
            <label className="text-xs font-medium text-zinc-400 flex items-center gap-2">
                {icon}
                {label}
            </label>
            <input
                className="w-full bg-zinc-950 border border-zinc-800 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all text-zinc-100 placeholder:text-zinc-600"
                {...props}
            />
        </div>
    );
}