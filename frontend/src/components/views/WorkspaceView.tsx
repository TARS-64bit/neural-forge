import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Sparkles, Layers, User } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { TaskCard } from "@/components/ui/TaskCard";

export type ChatTurn = {
    id: string;
    prompt: string;
    status: "planning" | "completed" | "error";
    planData?: any;
};

export function WorkspaceView({
    history, featurePrompt, setFeaturePrompt, onPlan, isPlanning
}: any) {

    // Auto-scroll to bottom when new messages arrive
    const endOfMessagesRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [history]);

    return (
        <div className="flex flex-col h-[calc(100vh-140px)]">

            {/* 1. CHAT HISTORY (Scrollable) */}
            <div className="flex-1 overflow-y-auto space-y-8 pb-4 pr-2 custom-scrollbar">
                {history.length === 0 && (
                    <div className="h-full flex items-center justify-center text-zinc-500 text-sm">
                        Workspace ready. Describe your first feature to begin.
                    </div>
                )}

                {history.map((turn: ChatTurn) => (
                    <motion.div key={turn.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">

                        {/* User Prompt Bubble */}
                        <div className="flex items-start gap-4 ml-auto w-3/4 justify-end">
                            <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-2xl rounded-tr-sm px-5 py-3 text-sm text-zinc-300">
                                {turn.prompt}
                            </div>
                            <div className="p-2 bg-zinc-800 rounded-full shrink-0"><User className="w-4 h-4 text-zinc-400" /></div>
                        </div>

                        {/* Agent Status / Result Bubble */}
                        <div className="flex items-start gap-4 w-11/12">
                            <div className="p-2 bg-cyan-500/10 border border-cyan-500/20 rounded-full shrink-0"><Sparkles className="w-4 h-4 text-cyan-400" /></div>

                            <div className="flex-1 space-y-4">
                                {/* Is Planning (Loading Stepper) */}
                                {turn.status === "planning" && (
                                    <Card className="space-y-4 !p-5">
                                        <h3 className="text-sm font-medium border-b border-zinc-800 pb-3">Multi-Agent Workflow Active</h3>
                                        <div className="space-y-3">
                                            <div className="flex items-center gap-3 text-sm"><div className="w-2 h-2 rounded-full bg-cyan-500 animate-ping"></div><span className="text-zinc-300">PM Agent: Searching codebase...</span></div>
                                            <div className="flex items-center gap-3 text-sm opacity-50"><div className="w-2 h-2 rounded-full bg-zinc-700"></div><span className="text-zinc-500">Tech Lead: Decomposing tasks...</span></div>
                                        </div>
                                    </Card>
                                )}

                                {/* Is Completed (Final Plan) */}
                                {turn.status === "completed" && turn.planData && (
                                    <div className="space-y-6">
                                        <Card className="!bg-zinc-900/40 !p-5">
                                            <h3 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Scope Analysis</h3>
                                            <p className="text-sm text-zinc-300 leading-relaxed">{turn.planData.scope_analysis}</p>
                                        </Card>

                                        <div className="space-y-4">
                                            <h3 className="text-md font-medium flex items-center gap-2"><Layers className="w-4 h-4" /> Execution Plan</h3>
                                            <div className="grid gap-3">
                                                {turn.planData.tasks?.map((task: any, index: number) => (
                                                    <TaskCard key={index} task={task} />
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </motion.div>
                ))}
                <div ref={endOfMessagesRef} />
            </div>

            {/* 2. PROMPT INPUT AREA (Pinned to bottom) */}
            <div className="shrink-0 pt-4 border-t border-zinc-800/50 mt-2">
                <div className="relative">
                    <textarea
                        rows={3}
                        className="w-full bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 pr-32 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all font-mono resize-none"
                        placeholder="e.g., Add a JWT authentication middleware..."
                        value={featurePrompt}
                        onChange={(e) => setFeaturePrompt(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                if (featurePrompt && !isPlanning) onPlan();
                            }
                        }}
                    />
                    <div className="absolute bottom-3 right-3">
                        <Button variant="secondary" onClick={onPlan} disabled={!featurePrompt || isPlanning} className="!py-1.5 !px-3">
                            <Sparkles className="w-3 h-3" /> Forge
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}