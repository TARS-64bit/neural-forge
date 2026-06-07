import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from ..helpers.background import run_background_ingestion
from ..models import RepoIngestRequest
from ..task_registry import TASK_DB
from ..helpers.rate_limiter import limiter

router = APIRouter(prefix="/api")


@router.post("/ingest")
@limiter.limit("5/minute")
async def start_ingestion(req: RepoIngestRequest, background_tasks: BackgroundTasks, request: Request):
    try:
        parts = req.github_url.rstrip("/").split("/")
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
        req.branch,
        req.github_pat,
    )

    return {
        "message": "Ingestion started",
        "task_id": task_id,
        "repo_owner": repo_owner,
        "repo_name": repo_name,
    }
