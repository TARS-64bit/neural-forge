import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ..helpers.background import run_background_ingestion
from ..models import RepoIngestRequest
from ..task_registry import TASK_DB

router = APIRouter(prefix="/api")


@router.post("/ingest")
async def start_ingestion(request: RepoIngestRequest, background_tasks: BackgroundTasks):
    try:
        parts = request.github_url.rstrip("/").split("/")
        repo_owner, repo_name = parts[-2], parts[-1]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format.")

    task_id = str(uuid.uuid4())
    TASK_DB[task_id] = "processing"

    background_tasks.add_task(
        run_background_ingestion,
        task_id,
        repo_owner,
        repo_name,
        request.branch,
        request.github_pat,
    )

    return {
        "message": "Ingestion started",
        "task_id": task_id,
        "repo_owner": repo_owner,
        "repo_name": repo_name,
    }
