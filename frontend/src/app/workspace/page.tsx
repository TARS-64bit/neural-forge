"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { WorkspaceView, ChatTurn } from "@/components/views/WorkspaceView";
import { useDispatch, useSelector } from "react-redux";
import { AppRootState } from "@/store";
import { AGENT_MAP } from "@/constants/agent_map";
import { clearRepoDetails, setRepoDetails } from "@/store/repoSlice";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/lib/config";


export default function WorkspacePage() {
    const dispatch = useDispatch();
    const router = useRouter();
    const handleDisconnect = () => {
        dispatch(clearRepoDetails()); // Wipes Redux
        Cookies.remove("nf_workspace_active"); // Wipes Cookie
        router.replace("/"); // Sends to Setup page
    };
    const { githubUrl, repoOwner, repoName, githubPat, githubBranch, maxLoops } = useSelector((state: AppRootState) => state.repo);

    const [featurePrompt, setFeaturePrompt] = useState("");
    const [history, setHistory] = useState<ChatTurn[]>([]);
    const [ingestTaskId, setIngestTaskId] = useState<string | null>(null);

    // 1. Fetch Branches for the Dropdown
    const { data: branches, isLoading: isLoadingBranches } = useQuery({
        queryKey: ["githubBranches", repoOwner, repoName, githubPat],
        queryFn: async () => {
            const res = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}/branches`, {
                headers: { Authorization: `Bearer ${githubPat}`, Accept: "application/vnd.github.v3+json" },
            });
            if (!res.ok) throw new Error("Could not fetch branches");
            const data = await res.json();
            return data.map((b: any) => b.name) as string[];
        },
        enabled: !!repoOwner && !!githubPat,
    });

    // 2. Start the Re-Index process
    const ingestMutation = useMutation({
        mutationFn: async (newBranch: string) => {
            const res = await fetch(`${API_BASE_URL}/api/ingest`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ github_url: githubUrl, github_pat: githubPat, branch: newBranch }),
            });
            if (!res.ok) throw new Error("Ingestion failed");

            // Update Redux state immediately so the UI badge updates
            dispatch(setRepoDetails({ githubUrl, githubPat, githubBranch: newBranch, repoOwner, repoName, maxLoops }));

            return res.json();
        },
        onSuccess: (data) => {
            setIngestTaskId(data.task_id); // Triggers the polling below
        },
    });

    // 3. Poll for Re-Index completion
    useQuery({
        queryKey: ["ingestStatus", ingestTaskId],
        queryFn: async () => {
            const res = await fetch(`${API_BASE_URL}/api/status/${ingestTaskId}`);
            const data = await res.json();
            if (data.status === "completed") {
                setIngestTaskId(null); // Stop polling
            }
            return data;
        },
        refetchInterval: ingestTaskId ? 3000 : false,
        enabled: !!ingestTaskId,
    });

    const planMutation = useMutation({
        mutationFn: async (promptText: string) => {
            const res = await fetch(`${API_BASE_URL}/api/plan`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    feature_prompt: promptText,
                    repo_owner: repoOwner,
                    repo_name: repoName,
                    branch: githubBranch,
                    max_loops: maxLoops
                }),
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));
                throw new Error(errorData.detail || "Server failed to generate a plan.");
            }

            const reader = res.body!.getReader();
            const decoder = new TextDecoder("utf-8");
            let finalPlanData = null;

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split("\n\n");

                for (const line of lines) {
                    if (line.trim().startsWith("data: ")) {
                        const data = JSON.parse(line.replace("data: ", ""));

                        if (data.type === "status" && AGENT_MAP[data.executor]) {
                            const logMsg = AGENT_MAP[data.executor];
                            setHistory((prev) => prev.map((turn) => {
                                if (turn.status === "planning") {
                                    const currentLogs = turn.logs || [];
                                    if (currentLogs[currentLogs.length - 1] !== logMsg) {
                                        return { ...turn, logs: [...currentLogs, logMsg] };
                                    }
                                }
                                return turn;
                            }));
                        } else if (data.type === "completed") {
                            finalPlanData = data.plan;
                        }
                    }
                }
            }
            return finalPlanData;
        },
        onMutate: (promptText) => {
            const turnId = Date.now().toString();
            setHistory((prev) => [...prev, { id: turnId, prompt: promptText, status: "planning", logs: ["Initializing Neural Forge..."] }]);
            setFeaturePrompt("");
            return { turnId };
        },
        onSuccess: (data, variables, context) => {
            if (!data) {
                setHistory((prev) => prev.map((turn) => turn.id === context?.turnId ? { ...turn, status: "error", errorMsg: "Workflow returned an empty response." } : turn));
                return;
            }
            setHistory((prev) => prev.map((turn) => turn.id === context?.turnId ? { ...turn, status: "completed", planData: data } : turn));
        },
        onError: (error, variables, context) => {
            setHistory((prev) => prev.map((turn) => turn.id === context?.turnId ? { ...turn, status: "error", errorMsg: error.message } : turn));
        }
    });

    const formatTaskToMarkdown = (task: any) => {
        let body = `**Type:** ${task.type}\n\n${task.description}\n\n`;
        if (task.acceptance_criteria?.length) {
            body += `### Acceptance Criteria\n`;
            task.acceptance_criteria.forEach((crit: string) => {
                body += `- [ ] ${crit}\n`; // Markdown checkboxes!
            });
        }
        if (task.dependencies?.length) {
            body += `\n**Dependencies:** ${task.dependencies.join(", ")}`;
        }
        return body;
    };

    const exportIssuesMutation = useMutation({
        mutationFn: async (tasksToExport: any[]) => {
            const issuesPayload = tasksToExport.map(t => ({
                title: `[${t.type.toUpperCase()}] ${t.title}`,
                body: formatTaskToMarkdown(t)
            }));

            const res = await fetch(`${API_BASE_URL}/api/export-issues`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    github_pat: githubPat,
                    repo_owner: repoOwner,
                    repo_name: repoName,
                    issues: issuesPayload
                }),
            });
            if (!res.ok) throw new Error("Failed to export issues");
            return res.json();
        },
        onSuccess: (data) => {
            alert(`Successfully created ${data.urls.length} GitHub Issue(s)!`);
        },
        onError: (err) => {
            alert(`Error exporting issues: ${err.message}`);
        }
    });

    const handleUpdateTask = (turnId: string, taskId: string, updatedTask: any | null) => {
        setHistory((prev) => prev.map((turn) => {
            if (turn.id === turnId && turn.planData) {
                let newTasks;

                if (updatedTask === null) {
                    // DELETE task
                    newTasks = turn.planData?.tasks?.filter((t: any) => t.id !== taskId);
                } else {
                    // EDIT task
                    newTasks = turn.planData?.tasks?.map((t: any) =>
                        t.id === taskId ? updatedTask : t
                    );
                }

                return {
                    ...turn,
                    planData: { ...turn.planData, tasks: newTasks }
                };
            }
            return turn;
        }));
    };


    const handleExport = (tasks: any | any[]) => {
        // Works for both a single task object OR an array of task objects
        const tasksArray = Array.isArray(tasks) ? tasks : [tasks];
        exportIssuesMutation.mutate(tasksArray);
    };


    const handleSaveSettings = (newBranch: string, newMaxLoops: number) => {
        // 1. Update Redux immediately
        dispatch(setRepoDetails({
            githubUrl, githubPat, githubBranch: newBranch, repoOwner, repoName, maxLoops: newMaxLoops
        }));

        // 2. Only trigger a backend re-index if the branch actually changed
        if (newBranch !== githubBranch) {
            ingestMutation.mutate(newBranch);
        }
    };


    const isReindexing = ingestMutation.isPending || !!ingestTaskId;

    return (
        <main className="max-w-5xl mx-auto flex-1 max-h-screen flex-col">
            <WorkspaceView
                history={history}
                featurePrompt={featurePrompt}
                setFeaturePrompt={setFeaturePrompt}
                onPlan={() => planMutation.mutate(featurePrompt)}
                onRetry={(failedPrompt: string) => planMutation.mutate(failedPrompt)}
                isPlanning={planMutation.isPending}
                branches={branches}
                isLoadingBranches={isLoadingBranches}
                onReindex={(newBranch: string) => ingestMutation.mutate(newBranch)}
                isReindexing={isReindexing}
                onDisconnect={handleDisconnect}
                maxLoops={maxLoops}
                onSaveSettings={handleSaveSettings}
                onExport={handleExport}
                isExporting={exportIssuesMutation.isPending}
                onUpdateTask={handleUpdateTask}
            />
        </main>
    );
}