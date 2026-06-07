import { AnimatePresence, motion } from "framer-motion";
import { GitBranch, Loader2, RefreshCw, LogOut, Settings, X, Layers } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function SettingsModal({
    isOpen,
    selectedBranch,
    setSelectedBranch,
    selectedLoops,
    setSelectedLoops,
    githubBranch,
    maxLoops,
    branches,
    isLoadingBranches,
    onReindex,
    onSaveSettings,
    onDisconnect,
    onClose,
}: Readonly<{
    isOpen: boolean;
    selectedBranch: string;
    setSelectedBranch: (branch: string) => void;
    selectedLoops: number;
    setSelectedLoops: (loops: number) => void;
    githubBranch: string;
    maxLoops: number;
    branches?: string[];
    isLoadingBranches?: boolean;
    onReindex?: (newBranch: string) => void;
    onSaveSettings: (newBranch: string, newMaxLoops: number) => void;
    onDisconnect?: () => void;
    onClose: () => void;
}>) {
    return (
        <AnimatePresence>
            {isOpen && (
                <div className="absolute inset-0 z-[60] flex items-center justify-center p-4">
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="absolute inset-0 bg-black/60 backdrop-blur-sm cursor-pointer"
                    />

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 10 }}
                        className="relative w-full max-w-md bg-zinc-900/60 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden"
                    >
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 p-1 cursor-pointer rounded-md text-zinc-500 hover:text-red-400 transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                        <div className="p-6 space-y-6">
                            <div>
                                <h2 className="text-xl font-medium text-zinc-100 flex items-center gap-2">
                                    <Settings className="w-5 h-5 text-zinc-400" /> Workspace Settings
                                </h2>
                                <p className="text-sm text-zinc-400 mt-2">
                                    Update the target branch to re-index the codebase, or disconnect to switch to a different repository.
                                </p>
                            </div>

                            <div className="space-y-3 bg-zinc-950/50 p-4 rounded-xl border border-zinc-800/50">
                                <label className="text-xs font-medium text-zinc-400 flex items-center gap-2">
                                    <GitBranch className="w-4 h-4" /> Target Branch
                                </label>
                                {isLoadingBranches ? (
                                    <div className="text-xs text-zinc-500 flex items-center gap-2">
                                        <Loader2 className="w-3 h-3 animate-spin" /> Fetching branches...
                                    </div>
                                ) : (
                                    <select
                                        className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-3 py-2.5 text-sm text-zinc-300 focus:outline-none focus:border-cyan-500 transition-colors cursor-pointer appearance-none"
                                        value={selectedBranch}
                                        onChange={(e) => setSelectedBranch(e.target.value)}
                                    >
                                        {branches?.map((b) => (
                                            <option key={b} value={b}>{b}</option>
                                        ))}
                                    </select>
                                )}
                                {/* 2. AGENTIC DEPTH (MAX LOOPS) SLIDER */}
                                <div>
                                    <label className="text-xs font-medium text-zinc-400 flex items-center justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                            <Layers className="w-4 h-4" /> Agentic Depth (Max Loops)
                                        </div>
                                        <span className="text-[#1591DC] font-mono text-sm">{selectedLoops}</span>
                                    </label>
                                    <input
                                        type="range"
                                        min="1" max="8" step="1"
                                        value={selectedLoops}
                                        onChange={(e) => setSelectedLoops(parseInt(e.target.value))}
                                        className="w-full accent-[#1591DC] cursor-pointer h-1.5 bg-zinc-800 rounded-lg appearance-none"
                                    />
                                    <p className="text-[10px] text-zinc-500 mt-2 leading-relaxed">
                                        ⚠️ High depth increases response size and wait times. The workflow will naturally stop before reaching this limit if all generated tasks are deemed atomic.
                                    </p>
                                </div>

                                {/* 3. SAVE BUTTON */}
                                <Button
                                    className="w-full !py-2 mt-4"
                                    disabled={selectedBranch === githubBranch && selectedLoops === maxLoops}
                                    onClick={() => {
                                        onClose();
                                        onSaveSettings(selectedBranch, selectedLoops);
                                    }}
                                >
                                    <RefreshCw className="w-4 h-4" /> Save Workspace Settings
                                </Button>

                                <Button
                                    className="w-full !py-2 mt-2"
                                    disabled={selectedBranch === "" || !onReindex}
                                    onClick={() => {
                                        onClose();
                                        if (onReindex) onReindex(selectedBranch);
                                    }}
                                >
                                    <RefreshCw className="w-4 h-4" /> Sync & Re-Index Branch
                                </Button>
                            </div>

                            <div className="pt-2">
                                <Button
                                    variant="outline"
                                    className="w-full !py-2 border-red-500/20 text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors"
                                    onClick={() => {
                                        onClose();
                                        if (onDisconnect) onDisconnect();
                                    }}
                                >
                                    <LogOut className="w-4 h-4" /> Disconnect Repository
                                </Button>
                            </div>
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}
