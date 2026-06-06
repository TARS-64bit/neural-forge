import logging
from agent_framework import AgentExecutorResponse, WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState
from neural_forge_app.ai_service.models.shared_responses import Plan

logger = logging.getLogger(__name__)


@executor(id="insert_subtasks")
async def insert_subtasks(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    """Insert subtasks returned by the refinement agent into the plan.

    Validates the incoming subtasks, updates the current task's `subtasks`
    field, advances index, and emits the updated iteration state.
    """
    logger.debug("Received subtasks from Refinement Agent: %s", response.agent_response.value)

    if not response.agent_response.value or response.agent_response.value.tasks is None:
        logger.exception("insert_subtasks: response missing tasks")
        raise ValueError("response content state not found")

    iteration_state = ctx.get_state("iteration_state")
    plan = ctx.get_state("plan")

    if not isinstance(iteration_state, TaskIterationState):
        logger.exception("iteration_state missing or wrong type")
        raise ValueError("iteration_state content state not found or of wrong type")

    if not isinstance(plan, Plan):
        logger.exception("plan missing or wrong type")
        raise ValueError("plan content state not found or of wrong type")

    new_subtasks = response.agent_response.value.tasks

    if not new_subtasks:
        logger.warning("No subtasks found to expand vague task: %s", plan.tasks[iteration_state.curr_index].title)
    else:
        plan.tasks[iteration_state.curr_index].subtasks = new_subtasks

    iteration_state.curr_index += 1
    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)
