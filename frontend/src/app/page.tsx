"use client";

import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { AnimatePresence } from "framer-motion";
import { useDispatch } from "react-redux";
import { setRepoDetails } from "@/store/repoSlice";
import Cookies from "js-cookie";
import { SetupView } from "@/components/views/SetupView";
import { IngestingView } from "@/components/views/IngestingView";
import { Cpu } from "lucide-react";
import { API_BASE_URL } from "@/lib/config";

export default function SetupPage() {
  const router = useRouter();
  const dispatch = useDispatch();
  const [step, setStep] = useState<"SETUP" | "INGESTING">("SETUP");

  const [githubUrl, setGithubUrl] = useState("");
  const [githubPat, setGithubPat] = useState("");
  const [githubBranch, setGithubBranch] = useState("main");
  const [taskId, setTaskId] = useState<string | null>(null);

  // Extract owner/repo safely
  const urlParts = githubUrl.trim().replace(/\/$/, "").split("/");
  const isUrlValid = urlParts.length >= 2 && githubUrl.includes("github.com");
  const parsedOwner = isUrlValid ? urlParts[urlParts.length - 2] : "";
  const parsedRepo = isUrlValid ? urlParts[urlParts.length - 1] : "";

  // Fetch Branches
  const { data: branches, isLoading: isLoadingBranches } = useQuery({
    queryKey: ["githubBranches", parsedOwner, parsedRepo, githubPat],
    queryFn: async () => {
      const res = await fetch(`https://api.github.com/repos/${parsedOwner}/${parsedRepo}/branches`, {
        headers: { Authorization: `Bearer ${githubPat}`, Accept: "application/vnd.github.v3+json" },
      });
      if (!res.ok) throw new Error("Could not fetch branches");
      const data = await res.json();
      return data.map((b: any) => b.name) as string[];
    },
    enabled: isUrlValid && githubPat.length > 10,
  });

  const checkRepoMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE_URL}/api/check-repo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ github_url: githubUrl, github_pat: githubPat, branch: githubBranch }),
      });
      return res.json();
    },
    onSuccess: (data) => {
      // Save details to Redux
      dispatch(setRepoDetails({
        githubUrl, githubPat, githubBranch,
        repoOwner: parsedOwner, repoName: parsedRepo,
        maxLoops: 3
      }));

      if (data.exists) {
        Cookies.set("nf_workspace_active", "true", { expires: 1 });
        router.push(`/workspace`);
      } else {
        ingestMutation.mutate();
      }
    },
  });

  // Start Ingestion
  const ingestMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE_URL}/api/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ github_url: githubUrl, github_pat: githubPat, branch: githubBranch }),
      });
      if (!res.ok) throw new Error("Ingestion failed");
      return res.json();
    },
    onSuccess: (data) => {
      setTaskId(data.task_id);
      dispatch(setRepoDetails({
        githubUrl,
        githubPat,
        githubBranch,
        repoOwner: parsedOwner,
        repoName: parsedRepo,
        maxLoops: 3
      }));
      Cookies.set("nf_workspace_active", "true", { expires: 1 });
      setStep("INGESTING");
    },
  });

  // Poll Status
  useQuery({
    queryKey: ["ingestStatus", taskId],
    queryFn: async () => {
      const res = await fetch(`${API_BASE_URL}/api/status/${taskId}`);
      const data = await res.json();
      if (data.status === "completed") {
        // NAVIGATE TO WORKSPACE PAGE! (Passing data via URL until Redux is set up)
        router.push("/workspace");
      }
      return data;
    },
    refetchInterval: step === "INGESTING" ? 3000 : false,
    enabled: step === "INGESTING" && !!taskId,
  });

  const isConnecting = checkRepoMutation.isPending || ingestMutation.isPending;

  return (
    <main className="max-w-screen mx-auto p-0 flex flex-col items-center justify-center">
      <header className="w-full py-6 px-6 flex items-center gap-3 sticky top-0 z-50">
        <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/20"><Cpu className="w-5 h-5 " /></div>
        <h1 className="text-xl font-semibold tracking-tight">Neural Forge</h1>
      </header>
      <AnimatePresence mode="wait">
        {step === "SETUP" && (
          <SetupView
            githubUrl={githubUrl} setGithubUrl={setGithubUrl}
            githubPat={githubPat} setGithubPat={setGithubPat}
            githubBranch={githubBranch} setGithubBranch={setGithubBranch}
            branches={branches} isLoadingBranches={isLoadingBranches}
            onIngest={() => checkRepoMutation.mutate()} isLoading={isConnecting}
          />
        )}
        {step === "INGESTING" && <IngestingView />}
      </AnimatePresence>
    </main>
  );
}