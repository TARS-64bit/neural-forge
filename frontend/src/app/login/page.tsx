"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Cpu, Key, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { motion } from "framer-motion";

export default function LoginPage() {
    const router = useRouter();
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");

        try {
            const res = await fetch("/api/auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password }),
            });

            const data = await res.json();

            if (data.success) {
                // Cookie is set! Refresh the router to trigger the middleware, 
                // which will instantly redirect them to the '/' setup page.
                router.refresh();
            } else {
                setError(data.message);
            }
        } catch (err) {
            setError("An error occurred connecting to the server.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="w-full h-screen bg-zinc-950 text-zinc-50 flex items-center justify-center p-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-sm space-y-8"
            >

                {/* Header */}
                <div className="flex flex-col items-center justify-center text-center space-y-4">
                    <div className="p-3 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
                        <Cpu className="w-8 h-8 text-cyan-400" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-medium tracking-tight">Neural Forge</h1>
                        <p className="text-sm text-zinc-500 mt-1">Autonomous Multi-Agent SDLC</p>
                    </div>
                </div>

                {/* Login Form */}
                <Card className="!p-6 space-y-6">
                    <form onSubmit={handleLogin} className="space-y-4">
                        <Input
                            label="System Access Code"
                            icon={<Key className="w-4 h-4" />}
                            type="password"
                            placeholder="Enter master password..."
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setError(""); // Clear error when typing
                            }}
                        />

                        {error && (
                            <p className="text-xs text-red-400 font-mono bg-red-500/10 p-2 rounded border border-red-500/20 text-center">
                                {error}
                            </p>
                        )}

                        <Button
                            type="submit"
                            className="w-full !py-2.5"
                            isLoading={isLoading}
                            disabled={!password || isLoading}
                        >
                            Authenticate <ChevronRight className="w-4 h-4" />
                        </Button>
                    </form>
                </Card>

            </motion.div>
        </main>
    );
}