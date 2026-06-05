import logging
from agent_framework import AgentExecutorRequest, Message, WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState
from neural_forge_app.ai_service.models.shared_responses import Plan

logger = logging.getLogger(__name__)


@executor(id="extract_next_task")
async def extract_next_task(iteration_state: TaskIterationState, ctx: WorkflowContext[AgentExecutorRequest | TaskIterationState]) -> None:
    """Extract the next task from the plan and send it for analysis/refinement.

    If a task is already marked atomic, advances the index without sending a
    refinement request. Otherwise constructs a task context and sends it.
    """
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        logger.exception("extract_next_task: plan not found or wrong type")
        raise ValueError("plan content state not found")

    task = plan.tasks[iteration_state.curr_index]

    logger.info("Extracting task for iteration %s, index %s: %s", iteration_state.curr_loop, iteration_state.curr_index, task.title)

    if task.is_sufficiently_atomic:
        logger.debug("Task '%s' is marked as sufficiently atomic. Skipping refinement.", task.title)
        iteration_state.curr_index += 1
        ctx.set_state("iteration_state", iteration_state)
        await ctx.send_message(iteration_state)
        return

    task_context = f"Title: {task.title}\nDescription: {task.description}\nCriteria: {task.acceptance_criteria}"

    await ctx.send_message(
        AgentExecutorRequest(messages=[Message("user", contents=[task_context])], should_respond=True)
    )
