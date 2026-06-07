import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { OverlayScrollbarsComponent } from "overlayscrollbars-react";
import { AppRootState } from "@/store";
import { useSelector } from "react-redux";
import { WorkspaceHeader } from "@/components/views/workspace/WorkspaceHeader";
import { SettingsModal } from "@/components/views/workspace/SettingsModal";
import { ChatTimeline } from "@/components/views/workspace/ChatTimeline";
import { ChatInput } from "@/components/views/workspace/ChatInput";

export type PlanData = {
    scope_analysis?: string;
    tasks?: Array<Record<string, unknown>>;
};

export type ChatTurn = {
    id: string;
    prompt: string;
    status: "planning" | "completed" | "error";
    logs?: string[];
    planData?: PlanData;
    errorMsg?: string;
};

export function WorkspaceView({
    history,
    featurePrompt,
    setFeaturePrompt,
    onPlan,
    isPlanning,
    onRetry,
    branches,
    isLoadingBranches,
    onReindex,
    isReindexing,
    onDisconnect,
    maxLoops, onSaveSettings,
    onExport, isExporting,
    onUpdateTask
}: Readonly<{
    history: ChatTurn[];
    featurePrompt: string;
    setFeaturePrompt: (prompt: string) => void;
    onPlan: () => void;
    isPlanning: boolean;
    onRetry: (failedPrompt: string) => void;
    branches?: string[];
    isLoadingBranches?: boolean;
    onReindex?: (newBranch: string) => void;
    isReindexing?: boolean;
    onDisconnect?: () => void;
    maxLoops: number;
    onSaveSettings: (newBranch: string, newMaxLoops: number) => void;
    onExport?: (tasks: any | any[]) => void;
    isExporting?: boolean;
    onUpdateTask?: (turnId: string, taskId: string, updatedTask: any | null) => void;
}>) {
    const { githubUrl, githubBranch } = useSelector((state: AppRootState) => state.repo);
    const [showSettingsModal, setShowSettingsModal] = useState(false);
    const [selectedBranch, setSelectedBranch] = useState(githubBranch);
    const [selectedLoops, setSelectedLoops] = useState(maxLoops);

    useEffect(() => {
        setSelectedBranch(githubBranch);
        setSelectedLoops(maxLoops);
    }, [githubBranch, maxLoops]);

    return (
        <>
            <SettingsModal
                isOpen={showSettingsModal}
                selectedBranch={selectedBranch}
                setSelectedBranch={setSelectedBranch}
                branches={branches}
                isLoadingBranches={isLoadingBranches}
                onReindex={onReindex}
                onDisconnect={onDisconnect}
                onClose={() => setShowSettingsModal(false)}
                setSelectedLoops={setSelectedLoops}
                selectedLoops={selectedLoops}
                maxLoops={maxLoops}
                onSaveSettings={onSaveSettings}
                githubBranch={githubBranch}
            />
            <AnimatePresence>
                {isReindexing && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute inset-0 z-[100] bg-zinc-950/80 backdrop-blur-sm flex flex-col items-center justify-center rounded-xl"
                    >
                        <Loader2 className="w-8 h-8 text-cyan-500 animate-spin mb-4" />
                        <h2 className="text-lg font-medium text-zinc-200">Syncing Codebase...</h2>
                        <p className="text-sm text-zinc-400 font-mono mt-2">Parsing AST & updating Azure AI Search</p>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex flex-col h-screen min-h-[calc(100vh-140px)] relative">
                <OverlayScrollbarsComponent
                    element="div"
                    className="h-full space-y-8 pr-3"
                    options={{ scrollbars: { theme: 'os-theme-light', autoHide: 'leave', autoHideDelay: 300 } }}
                    defer
                >
                    <WorkspaceHeader
                        githubUrl={githubUrl}
                        githubBranch={githubBranch}
                        onOpenSettings={() => {
                            setSelectedBranch(githubBranch);
                            setShowSettingsModal(true);
                        }}
                    />

                    <ChatTimeline history={history} onRetry={onRetry} onExport={onExport} isExporting={isExporting} onUpdateTask={onUpdateTask} />

                    <ChatInput
                        featurePrompt={featurePrompt}
                        setFeaturePrompt={setFeaturePrompt}
                        onPlan={onPlan}
                        isPlanning={isPlanning}
                    />
                </OverlayScrollbarsComponent>
            </div>
        </>
    );
}
