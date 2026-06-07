import { useState } from "react";
import clsx from "clsx";
import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function ChatInput({
    featurePrompt,
    setFeaturePrompt,
    onPlan,
    isPlanning,
}: Readonly<{
    featurePrompt: string;
    setFeaturePrompt: (prompt: string) => void;
    onPlan: () => void;
    isPlanning: boolean;
}>) {
    const [isFocused, setIsFocused] = useState(false);

    return (
        <div className="shrink-0 sticky bottom-0 pt-4 mx-6 pb-6 mt-2">
            <div
                className={clsx(
                    "relative backdrop-blur-lg overflow-hidden flex flex-row items-end justify-between bg-zinc-900/50 border rounded-xl p-4 text-sm transition-all font-mono",
                    isFocused ? "border-white/20" : "border-white/10"
                )}
            >
                <textarea
                    rows={3}
                    className="w-full border-none outline-none resize-none bg-transparent text-zinc-100"
                    placeholder="e.g., Add a JWT authentication middleware..."
                    value={featurePrompt}
                    onChange={(e) => setFeaturePrompt(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            if (featurePrompt && !isPlanning) onPlan();
                        }
                    }}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                />

                <div className="bottom-3 right-3">
                    <Button variant="secondary" onClick={onPlan} disabled={!featurePrompt || isPlanning}>
                        <Sparkles className="w-3 h-3" /> Forge
                    </Button>
                </div>
            </div>
        </div>
    );
}
