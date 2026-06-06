import { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader2 } from "lucide-react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
    variant?: "primary" | "secondary" | "outline";
    isLoading?: boolean;
}

export function Button({ children, variant = "primary", isLoading, className = "", disabled, ...props }: Readonly<ButtonProps>) {
    const baseStyles = "px-4 py-2 rounded-md text-sm font-medium flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary: "bg-zinc-100 text-zinc-900 hover:bg-white",
        secondary: "bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 border border-cyan-500/20",
        outline: "bg-transparent border border-zinc-800 text-zinc-300 hover:bg-zinc-900"
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${className}`}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            {children}
        </button>
    );
}