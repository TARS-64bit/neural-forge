import { motion } from "framer-motion";
import { GitBranch, Key, ChevronRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
export function SetupView({
    githubUrl, setGithubUrl,
    githubPat, setGithubPat,
    githubBranch, setGithubBranch,
    branches, isLoadingBranches,
    onIngest, isLoading
}: any) {
    return (
        <motion.div key="setup" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6 max-w-xl">
            <div>
                <h2 className="text-lg font-medium">Initialize Workspace</h2>
                <p className="text-white text-sm">Connect a GitHub repository to begin AST indexing.</p>
            </div>
            <Card className="space-y-4 backdrop-blur-lg bg-black/20!">
                <Input
                    label="Repository URL" icon={<GitBranch className="w-4 h-4" />}
                    placeholder="https://github.com/owner/repo" value={githubUrl} onChange={(e) => setGithubUrl(e.target.value)}
                />

                <Input
                    label="Personal Access Token" icon={<Key className="w-4 h-4" />}
                    type="password" placeholder="ghp_..." value={githubPat} onChange={(e) => setGithubPat(e.target.value)}
                />

                {/* --- DYNAMIC BRANCH DROPDOWN --- */}
                <div className="space-y-2">
                    <label className="text-xs font-medium text-zinc-400 flex items-center gap-2">
                        <GitBranch className="w-4 h-4" /> Target Branch
                    </label>

                    <div className="relative">
                        {isLoadingBranches ? (
                            <div className="w-full bg-zinc-950 border border-zinc-800 rounded-md px-3 py-2 text-sm text-zinc-500 flex items-center gap-2">
                                <Loader2 className="w-4 h-4 animate-spin" /> Fetching branches...
                            </div>
                        ) : branches && branches.length > 0 ? (
                            <select
                                className="w-full bg-zinc-950 border border-zinc-800 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all text-zinc-100 appearance-none cursor-pointer"
                                value={githubBranch}
                                onChange={(e) => setGithubBranch(e.target.value)}
                            >
                                {/* Default fallback just in case */}
                                <option value="main" disabled hidden>Select a branch</option>
                                {branches.map((branch: string) => (
                                    <option key={branch} value={branch}>{branch}</option>
                                ))}
                            </select>
                        ) : (
                            <Input
                                label=""
                                placeholder="main"
                                value={githubBranch}
                                onChange={(e) => setGithubBranch(e.target.value)}
                                disabled={!githubUrl || !githubPat}
                            />
                        )}

                        {/* Custom dropdown arrow for aesthetics */}
                        {branches && branches.length > 0 && !isLoadingBranches && (
                            <ChevronRight className="w-4 h-4 absolute right-3 top-2.5 text-zinc-500 rotate-90 pointer-events-none" />
                        )}
                    </div>
                </div>
                {/* --------------------------------- */}
                <Button onClick={onIngest} isLoading={isLoading} disabled={!githubUrl || !githubPat || !githubBranch}>
                    Connect & Ingest <ChevronRight className="w-4 h-4" />
                </Button>
            </Card>

        </motion.div>
    );
}