import { useEffect, useRef } from "react";

import type { ChatTurn } from "@/components/views/WorkspaceView";
import { ChatTurnRow } from "@/components/views/workspace/ChatTurnRow";

export function ChatTimeline({
    history,
    onRetry,
    onExport, isExporting,
    onUpdateTask
}: Readonly<{
    history: ChatTurn[];
    onRetry: (failedPrompt: string) => void;
    onExport?: (tasks: any | any[]) => void;
    isExporting?: boolean;
    onUpdateTask?: (turnId: string, taskId: string, updatedTask: any | null) => void;
}>) {
    const endOfMessagesRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [history]);

    return (
        <div className="flex-1 min-h-[calc(100vh-220px)] relative">
            {history.length === 0 ? (
                <div className="h-full flex items-center min-h-[calc(100vh-240px)] justify-center text-white-500 text-sm">
                    Workspace ready. Describe your first feature to begin.
                </div>
            ) : (
                history.map((turn) => <ChatTurnRow key={turn.id}
                    turn={turn} onRetry={onRetry}
                    onExport={onExport}
                    isExporting={isExporting}
                    onUpdateTask={onUpdateTask}
                />)
            )}
            <div ref={endOfMessagesRef} />
        </div>
    );
}
