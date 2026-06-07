export function TaskCard({ task }: { task: any }) {
    return (
        <div className="p-5 bg-zinc-900/80 border border-zinc-800 backdrop-blur-lg rounded-xl space-y-3 hover:border-zinc-700 transition-colors">
            <div className="flex items-center justify-between">
                <span className="px-2 py-1 bg-zinc-800 rounded text-xs font-mono text-zinc-400">{task.id}</span>
                <span className="px-2 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-500 rounded-full text-[10px] uppercase font-bold tracking-wider">
                    {task.type}
                </span>
            </div>
            <h4 className="font-medium text-zinc-100">{task.title}</h4>
            <p className="text-sm text-zinc-400">{task.description}</p>

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