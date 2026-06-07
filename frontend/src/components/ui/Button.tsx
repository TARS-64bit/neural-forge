import { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader2 } from "lucide-react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
    variant?: "primary" | "secondary" | "outline";
    isLoading?: boolean;
}

export function Button({ children, variant = "primary", isLoading, className = "", disabled, ...props }: Readonly<ButtonProps>) {
    const baseStyles = "px-4 py-2 rounded-md cursor-pointer text-sm font-medium flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary: "bg-black/50 text-white/70 hover:bg-black hover:text-white hover:shadow-[0_0_10px_0px_rgb(255,255,255,0.1)]",
        secondary: "bg-[#2C5EAD] text-white hover:bg-[#1591DC]",
        outline: "bg-transparent border border-zinc-800 text-zinc-300 hover:bg-black/50"
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