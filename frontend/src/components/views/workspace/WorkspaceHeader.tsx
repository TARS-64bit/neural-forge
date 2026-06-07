import { Settings } from "lucide-react";
import Image from "next/image";

export function WorkspaceHeader({
    githubUrl,
    githubBranch,
    onOpenSettings,
}: Readonly<{
    githubUrl?: string;
    githubBranch?: string;
    onOpenSettings: () => void;
}>) {
    return (
        <header className="w-full p-4 flex justify-between items-center sticky top-0 backdrop-blur-lg rounded-b-2xl border-2 border-t-0 border-white/10 bg-black/10 z-40">
            <div className="flex gap-3 items-center">
                <Image src="/neural-forge-logo.svg" alt="Neural Forge logo" width={32} height={32} />
                <h1 className="text-xl font-light tracking-tight">Neural Forge</h1>
            </div>

            {githubUrl && githubBranch && (
                <button
                    type="button"
                    onClick={onOpenSettings}
                    className="flex items-center gap-2 p-2 px-3 bg-black/80 hover:bg-black/60 border border-white/5 transition-colors rounded-lg text-xs font-mono text-white/80"
                >
                    <span className="text-white/40 font-light">Repo: </span>
                    {githubUrl.split("/").slice(-2).join("/")}@{githubBranch}
                    <Settings className="w-3 h-3 text-white/40 ml-1" />
                </button>
            )}
        </header>
    );
}
