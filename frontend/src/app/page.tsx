"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { AnimatePresence, motion } from "framer-motion";
import { Cpu, CheckCircle2 } from "lucide-react";

import { SetupView } from "@/components/views/SetupView";
import { IngestingView } from "@/components/views/IngestingView";
import { WorkspaceView, ChatTurn } from "@/components/views/WorkspaceView"; // <-- Import New View

type AppStep = "SETUP" | "INGESTING" | "WORKSPACE";

export default function NeuralForgeApp() {
  const [step, setStep] = useState<AppStep>("SETUP");

  const [githubUrl, setGithubUrl] = useState("");
  const [githubPat, setGithubPat] = useState("");
  const [repoOwner, setRepoOwner] = useState("");
  const [repoName, setRepoName] = useState("");

  const [taskId, setTaskId] = useState<string | null>(null);

  // NEW: Chat History State
  const [featurePrompt, setFeaturePrompt] = useState("");
  const [history, setHistory] = useState<ChatTurn[]>([]);

  // --- API CALLS ---
  const ingestMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch("http://127.0.0.1:8000/api/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ github_url: githubUrl, github_pat: githubPat }),
      });
      if (!res.ok) throw new Error("Ingestion failed");
      return res.json();
    },
    onSuccess: (data) => {
      setTaskId(data.task_id);
      setRepoOwner(data.repo_owner);
      setRepoName(data.repo_name);
      setStep("INGESTING");
    },
  });

  useQuery({
    queryKey: ["ingestStatus", taskId],
    queryFn: async () => {
      const res = await fetch(`http://127.0.0.1:8000/api/status/${taskId}`);
      const data = await res.json();
      if (data.status === "completed") setStep("WORKSPACE"); // Go straight to Workspace
      return data;
    },
    refetchInterval: step === "INGESTING" ? 3000 : false,
    enabled: step === "INGESTING" && !!taskId,
  });

  const planMutation = useMutation({
    mutationFn: async (promptText: string) => {
      const res = await fetch("http://127.0.0.1:8000/api/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feature_prompt: promptText, repo_owner: repoOwner, repo_name: repoName }),
      });
      if (!res.ok) throw new Error("Planning failed");
      return res.json();
    },
    // Triggers BEFORE the API call
    onMutate: (promptText) => {
      const turnId = Date.now().toString();
      // 1. Add User message and Agent loading state to history
      setHistory((prev) => [...prev, { id: turnId, prompt: promptText, status: "planning" }]);
      // 2. Clear input box immediately
      setFeaturePrompt("");
      return { turnId };
    },
    // Triggers AFTER the API call succeeds
    onSuccess: (data, variables, context) => {
      // 3. Update the loading message with the final data!
      setHistory((prev) => prev.map((turn) =>
        turn.id === context?.turnId
          ? { ...turn, status: "completed", planData: data.plan }
          : turn
      ));
    },
  });

  return (
    <main className="max-w-5xl mx-auto p-6 h-screen flex flex-col">
      <header className="mb-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
            <Cpu className="w-6 h-6 text-cyan-400" />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">Neural Forge</h1>
        </div>
        {step === "WORKSPACE" && (
          <div className="flex items-center gap-2 px-3 py-1 bg-zinc-900 border border-zinc-800 rounded-full text-xs text-zinc-400">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{repoOwner}/{repoName} Indexed</span>
          </div>
        )}
      </header>

      <div className="flex-1 overflow-hidden">
        <AnimatePresence mode="wait">
          {step === "SETUP" && (
            <SetupView
              githubUrl={githubUrl} setGithubUrl={setGithubUrl}
              githubPat={githubPat} setGithubPat={setGithubPat}
              onIngest={() => ingestMutation.mutate()}
              isLoading={ingestMutation.isPending}
            />
          )}

          {step === "INGESTING" && <IngestingView />}

          {/* THE NEW CHAT WORKSPACE */}
          {step === "WORKSPACE" && (
            <motion.div key="workspace" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full">
              <WorkspaceView
                history={history}
                featurePrompt={featurePrompt}
                setFeaturePrompt={setFeaturePrompt}
                onPlan={() => planMutation.mutate(featurePrompt)}
                isPlanning={planMutation.isPending}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}