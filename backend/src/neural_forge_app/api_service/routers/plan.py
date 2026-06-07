from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from neural_forge_app.api_service.helpers.get_dynamic_index_name import get_dynamic_index_name

from ..models import FeaturePlanRequest
from neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase
from ..helpers.rate_limiter import limiter  

router = APIRouter(prefix="/api")

@router.post("/plan")
@limiter.limit("10/minute")
async def generate_plan(req: FeaturePlanRequest, request: Request):
    dynamic_index = get_dynamic_index_name(req.repo_owner, req.repo_name, req.branch)
    return StreamingResponse(
        execute_planning_phase(req.feature_prompt, req.max_loops, dynamic_index),
        media_type="text/event-stream",
    )
