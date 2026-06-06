import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";

export function PlanningView() {
    return (
        <motion.div key="planning" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-xl space-y-6">
            <Card className="space-y-6">
                <h3 className="text-sm font-medium border-b border-zinc-800 pb-4">Multi-Agent Workflow Active</h3>
                <div className="space-y-4">
                    <div className="flex items-center gap-3 text-sm">
                        <div className="w-2 h-2 rounded-full bg-cyan-500 animate-ping"></div>
                        <span className="text-zinc-300">PM Agent: Searching codebase via Azure Hybrid Search...</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm opacity-50">
                        <div className="w-2 h-2 rounded-full bg-zinc-700"></div>
                        <span className="text-zinc-500">Tech Lead: Decomposing into atomic tasks...</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm opacity-50">
                        <div className="w-2 h-2 rounded-full bg-zinc-700"></div>
                        <span className="text-zinc-500">QA Refiner: Validating testable criteria...</span>
                    </div>
                </div>
            </Card>
        </motion.div>
    );
}