import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { User, Sparkles, AlertCircle, RefreshCw, ChevronDown, Layers } from "lucide-react";
import { OverlayScrollbarsComponent } from "overlayscrollbars-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { TaskCard } from "@/components/ui/TaskCard";
import type { ChatTurn, PlanData } from "@/components/views/WorkspaceView";

type PlanTask = Record<string, unknown>;

export function ChatTurnRow({ turn, onRetry }: Readonly<{ turn: ChatTurn; onRetry: (failedPrompt: string) => void }>) {
    return (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6 mt-4">
            <UserBubble prompt={turn.prompt} />
            <AgentBubble turn={turn} onRetry={onRetry} />
        </motion.div>
    );
}

function UserBubble({ prompt }: Readonly<{ prompt: string }>) {
    return (
        <div className="flex items-start gap-4 ml-auto w-3/4 justify-end">
            <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-2xl rounded-tr-sm px-5 py-3 text-sm text-zinc-300">
                {prompt}
            </div>
            <div className="p-2 bg-zinc-800 rounded-full shrink-0">
                <User className="w-4 h-4 text-zinc-400" />
            </div>
        </div>
    );
}

function AgentBubble({ turn, onRetry }: Readonly<{ turn: ChatTurn; onRetry: (failedPrompt: string) => void }>) {
    const isError = turn.status === "error";

    return (
        <div className="flex items-start gap-4 w-11/12">
            <div className={`p-2 border rounded-full shrink-0 ${isError ? "bg-red-500/10 border-red-500/20" : "bg-cyan-500/10 border-cyan-500/20"}`}>
                {isError ? <AlertCircle className="w-4 h-4 text-red-400" /> : <Sparkles className="w-4 h-4 text-cyan-400" />}
            </div>

            <div className="flex-1 space-y-4">
                {turn.status === "planning" && <PlanningStepper logs={turn.logs} />}
                {turn.status === "completed" && turn.planData && <CompletedPlan planData={turn.planData} />}

                {isError && (
                    <Card className="!bg-red-500/5 !border-red-500/20 !p-5">
                        <h3 className="text-sm font-semibold text-red-400 uppercase tracking-wider mb-2">Workflow Failed</h3>
                        <p className="text-sm text-red-200/80 leading-relaxed font-mono mb-4">
                            {turn.errorMsg || "An unknown error occurred during the planning phase."}
                        </p>
                        <Button
                            variant="outline"
                            onClick={() => onRetry(turn.prompt)}
                            className="!py-1.5 !px-3 !text-xs border-red-500/20 hover:bg-red-500/10 text-red-400 transition-colors"
                        >
                            <RefreshCw className="w-3 h-3" /> Retry Prompt
                        </Button>
                    </Card>
                )}
            </div>
        </div>
    );
}

function PlanningStepper({ logs = [] }: Readonly<{ logs?: string[] }>) {
    const [isExpanded, setIsExpanded] = useState(false);
    const logEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (isExpanded) {
            logEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
    }, [logs, isExpanded]);

    const currentLog = logs[logs.length - 1] || "Initializing Neural Forge...";
    const currentAgentName = currentLog.split(":")[0];

    return (
        <Card className="!p-0 overflow-hidden border-zinc-800/60">
            <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-zinc-800/30 transition-colors"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></div>
                    <h3 className="text-sm font-medium text-zinc-200">
                        {currentAgentName} <span className="text-zinc-500 font-normal ml-1">is working...</span>
                    </h3>
                </div>

                <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-zinc-500">{logs.length} steps</span>
                    <motion.div animate={{ rotate: isExpanded ? 180 : 0 }} transition={{ duration: 0.2 }}>
                        <ChevronDown className="w-4 h-4 text-zinc-500" />
                    </motion.div>
                </div>
            </div>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="border-t border-zinc-800/50 bg-zinc-900/30"
                    >
                        <OverlayScrollbarsComponent
                            element="div"
                            className="max-h-48 p-4 space-y-3"
                            options={{
                                scrollbars: {
                                    theme: 'os-theme-light',
                                    autoHide: 'leave',
                                    autoHideDelay: 300,
                                },
                            }}
                            defer
                        >
                            {logs.map((log, index) => {
                                const isLast = index === logs.length - 1;
                                return (
                                    <div key={index} className="flex items-start gap-3 text-sm">
                                        <div className="mt-1.5">
                                            {isLast ? (
                                                <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-ping"></div>
                                            ) : (
                                                <div className="w-1.5 h-1.5 rounded-full bg-zinc-600"></div>
                                            )}
                                        </div>
                                        <span className={`font-mono text-xs ${isLast ? "text-zinc-300" : "text-zinc-500"}`}>
                                            {log}
                                        </span>
                                    </div>
                                );
                            })}
                            <div ref={logEndRef} />
                        </OverlayScrollbarsComponent>
                    </motion.div>
                )}
            </AnimatePresence>
        </Card>
    );
}

function CompletedPlan({ planData }: Readonly<{ planData: PlanData }>) {
    return (
        <div className="space-y-6">
            <Card className="!bg-zinc-900/40 !p-5">
                <h3 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Scope Analysis</h3>
                <p className="text-sm text-zinc-300 leading-relaxed">{planData.scope_analysis}</p>
            </Card>

            <div className="space-y-4">
                <h3 className="text-md font-medium flex items-center gap-2">
                    <Layers className="w-4 h-4" /> Execution Plan
                </h3>
                <div className="grid gap-3">
                    {planData.tasks?.map((task: PlanTask, index: number) => (
                        <TaskCard key={index} task={task} />
                    ))}
                </div>
            </div>
        </div>
    );
}
