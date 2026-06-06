import { motion } from "framer-motion";
import { Layers } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { TaskCard } from "@/components/ui/TaskCard";
import { Button } from "@/components/ui/Button";

export function ResultView({ planData, onReset }: any) {
    return (
        <motion.div key="result" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
            <Card className="bg-zinc-900/40!">
                <h3 className="text-sm font-semibold text-cyan-400 uppercase tracking-wider mb-2">Scope Analysis</h3>
                <p className="text-sm text-zinc-300 leading-relaxed">{planData.scope_analysis}</p>
            </Card>

            <div className="space-y-4">
                <h3 className="text-lg font-medium flex items-center gap-2"><Layers className="w-5 h-5" /> Execution Plan</h3>
                <div className="grid gap-4">
                    {planData.tasks?.map((task: any) => (
                        <TaskCard key={task.id} task={task} />
                    ))}
                </div>
            </div>
            <Button variant="outline" onClick={onReset}>
                Plan another feature
            </Button>
        </motion.div>
    );
}