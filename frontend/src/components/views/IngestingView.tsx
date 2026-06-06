import { motion } from "framer-motion";
import { Terminal } from "lucide-react";
import { Card } from "@/components/ui/Card";

export function IngestingView() {
    return (
        <motion.div key="ingest" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="max-w-xl">
            <Card className="overflow-hidden relative">
                <div className="absolute top-0 left-0 h-1 bg-cyan-500 animate-pulse w-full"></div>
                <div className="flex items-center gap-4 mb-4 text-cyan-400">
                    <Terminal className="w-5 h-5 animate-pulse" />
                    <span className="text-sm font-mono">Ingestion Pipeline Running...</span>
                </div>
                <div className="space-y-2 font-mono text-xs text-zinc-500">
                    <p>{">"} Cloning ephemeral workspace securely into /tmp</p>
                    <p>{">"} Parsing AST syntax for code chunks</p>
                    <p className="text-zinc-300 animate-pulse">{">"} Vectorizing & Uploading to Azure AI Search...</p>
                </div>
            </Card>
        </motion.div>
    );
}