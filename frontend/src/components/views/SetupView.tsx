import { motion } from "framer-motion";
import { GitBranch, Key, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";

export function SetupView({ 
  githubUrl, setGithubUrl, githubPat, setGithubPat, onIngest, isLoading 
}: any) {
  return (
    <motion.div key="setup" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6 max-w-xl">
      <div>
        <h2 className="text-xl font-medium">Initialize Workspace</h2>
        <p className="text-zinc-400 text-sm">Connect a GitHub repository to begin AST indexing.</p>
      </div>
      <Card className="space-y-4">
        <Input label="Repository URL" icon={<GitBranch className="w-4 h-4" />} placeholder="https://github.com/owner/repo" value={githubUrl} onChange={(e) => setGithubUrl(e.target.value)} />
        <Input label="Personal Access Token" icon={<Key className="w-4 h-4" />} type="password" placeholder="ghp_..." value={githubPat} onChange={(e) => setGithubPat(e.target.value)} />
      </Card>
      <Button onClick={onIngest} isLoading={isLoading} disabled={!githubUrl || !githubPat}>
        Connect & Ingest <ChevronRight className="w-4 h-4" />
      </Button>
    </motion.div>
  );
}