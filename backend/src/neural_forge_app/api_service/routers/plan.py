from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from neural_forge_app.api_service.helpers.get_dynamic_index_name import get_dynamic_index_name

from ..models import FeaturePlanRequest
from neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase

router = APIRouter(prefix="/api")

@router.post("/plan")
async def generate_plan(request: FeaturePlanRequest):
    dynamic_index = get_dynamic_index_name(request.repo_owner, request.repo_name, request.branch)
    return StreamingResponse(
        execute_planning_phase(request.feature_prompt, request.max_loops, dynamic_index),
        media_type="text/event-stream",
    )
