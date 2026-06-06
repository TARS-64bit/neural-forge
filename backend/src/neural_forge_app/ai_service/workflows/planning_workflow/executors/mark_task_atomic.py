import logging
from agent_framework import AgentExecutorResponse, WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState
from neural_forge_app.ai_service.models.shared_responses import Plan

logger = logging.getLogger(__name__)


@executor(id="mark_task_atomic")
async def mark_task_atomic(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    """Mark the current task as sufficiently atomic and advance the index.

    Ensures types are correct, toggles `is_sufficiently_atomic` on the current
    task and advances the `curr_index` so subsequent iterations proceed.
    """
    logger.debug("Marking task as atomic: %s", response.agent_response.value)
    if not response.agent_response.value:
        logger.exception("mark_task_atomic: missing response content")
        raise ValueError("response content state not found or of wrong type")

    iteration_state = ctx.get_state("iteration_state")
    plan = ctx.get_state("plan")

    if not isinstance(iteration_state, TaskIterationState):
        logger.exception("iteration_state missing or wrong type")
        raise ValueError("iteration_state content state not found or of wrong type")

    if not isinstance(plan, Plan):
        logger.exception("plan missing or wrong type")
        raise ValueError("plan content state not found or of wrong type")

    plan.tasks[iteration_state.curr_index].is_sufficiently_atomic = True

    iteration_state.curr_index += 1
    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)
