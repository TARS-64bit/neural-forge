from fastapi import APIRouter, HTTPException

from ..task_registry import TASK_DB

router = APIRouter(prefix="/api")


@router.get("/status/{task_id}")
async def check_status(task_id: str):
    status = TASK_DB.get(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task_id": task_id, "status": status}
