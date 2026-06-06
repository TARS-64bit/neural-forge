import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function PromptView({ featurePrompt, setFeaturePrompt, onPlan }: any) {
    return (
        <motion.div key="prompt" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
            <div>
                <h2 className="text-xl font-medium">Command Center</h2>
                <p className="text-zinc-400 text-sm">Describe the feature or architecture change.</p>
            </div>
            <textarea
                rows={6}
                className="w-full bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all font-mono resize-none"
                placeholder="e.g., Add a JWT authentication middleware..."
                value={featurePrompt}
                onChange={(e) => setFeaturePrompt(e.target.value)}
            />
            <Button variant="secondary" onClick={onPlan} disabled={!featurePrompt}>
                <Sparkles className="w-4 h-4" /> Forge Agentic Plan
            </Button>
        </motion.div>
    );
}