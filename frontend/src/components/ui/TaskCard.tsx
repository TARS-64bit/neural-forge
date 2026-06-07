import { useState } from "react";
import { GitCommitIcon, Edit2, Trash2, Check, X } from "lucide-react";
import { Button } from "./Button"; // Ensure this import path is correct

export function TaskCard({
    task,
    onExport,
    onUpdate
}: Readonly<{
    task: any,
    onExport?: () => void,
    onUpdate?: (task: any | null) => void
}>) {
    const [isEditing, setIsEditing] = useState(false);

    // Local state for the edit form
    const [editTitle, setEditTitle] = useState(task.title);
    const [editDesc, setEditDesc] = useState(task.description);

    const handleSave = () => {
        if (onUpdate) {
            onUpdate({ ...task, title: editTitle, description: editDesc });
        }
        setIsEditing(false);
    };

    const handleDelete = () => {
        // Pass null to tell the parent to delete this task
        if (onUpdate && confirm("Are you sure you want to delete this task?")) {
            onUpdate(null);
        }
    };

    const handleCancel = () => {
        setEditTitle(task.title);
        setEditDesc(task.description);
        setIsEditing(false);
    };

    if (isEditing) {
        // --- EDIT MODE UI ---
        return (
            <div className="p-4 bg-zinc-900/90 border backdrop-blur-lg border-[#1591DC]/50 shadow-[0_0_15px_rgba(6,182,212,0.1)] rounded-xl space-y-4 transition-all">
                <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
                    <span className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-400">{task.id}</span>
                    <span className="text-xs text-[#4BB8FA] font-medium">EDITING TASK</span>
                </div>

                <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full bg-zinc-950/70 border border-zinc-800 rounded-md px-3 py-2 text-sm text-zinc-100 focus:outline-none focus:border-[#4BB8FA]"
                />

                <textarea
                    rows={3}
                    value={editDesc}
                    onChange={(e) => setEditDesc(e.target.value)}
                    className="w-full bg-zinc-950/70 border border-zinc-800 rounded-md px-3 py-2 text-sm text-zinc-100 focus:outline-none focus:border-[#4BB8FA] resize-none"
                />

                <div className="flex items-center justify-end gap-2 pt-2">
                    <Button variant="outline" className="!py-1 !px-3" onClick={handleCancel}>
                        <X className="w-3 h-3" /> Cancel
                    </Button>
                    <Button className="!py-1 !px-3" onClick={handleSave}>
                        <Check className="w-3 h-3" /> Save Changes
                    </Button>
                </div>
            </div>
        );
    }

    // --- STANDARD VIEW MODE UI ---
    return (
        <div className="group p-5 bg-zinc-900/80 border backdrop-blur-lg border-zinc-800 rounded-xl space-y-3 hover:border-zinc-700 transition-colors relative">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <span className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-400">{task.id}</span>
                    <span className="px-2 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-500 rounded-full text-[10px] uppercase font-bold tracking-wider">
                        {task.type}
                    </span>
                </div>

                {/* Action Buttons (Visible on Hover) */}
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    {onUpdate && (
                        <>
                            <button onClick={() => setIsEditing(true)} title="Edit Task" className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-500 hover:text-cyan-400 transition-colors">
                                <Edit2 className="w-4 h-4" />
                            </button>
                            <button onClick={handleDelete} title="Delete Task" className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-500 hover:text-red-400 transition-colors">
                                <Trash2 className="w-4 h-4" />
                            </button>
                        </>
                    )}
                    {onExport && (
                        <button onClick={onExport} title="Create GitHub Issue" className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-500 hover:text-zinc-300 transition-colors">
                            <GitCommitIcon className="w-4 h-4" />
                        </button>
                    )}
                </div>
            </div>

            <h4 className="font-medium text-zinc-100">{task.title}</h4>
            <p className="text-sm text-zinc-400 leading-relaxed">{task.description}</p>

            {task.acceptance_criteria && task.acceptance_criteria.length > 0 && (
                <div className="pt-3 border-t border-zinc-800/50">
                    <p className="text-xs font-medium text-zinc-500 mb-2 uppercase tracking-wider">Acceptance Criteria</p>
                    <ul className="space-y-1">
                        {task.acceptance_criteria.map((crit: string, i: number) => (
                            <li key={i} className="text-xs text-zinc-300 flex items-start gap-2">
                                <span className="mt-1 w-1 h-1 rounded-full bg-cyan-500/50 shrink-0"></span>
                                {crit}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}