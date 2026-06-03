import logging
from agent_framework import WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState, flatten_tasks
from neural_forge_app.ai_service.agents.pm_agent.models import Plan

logger = logging.getLogger(__name__)


@executor(id="commit_flattened_tasks")
async def commit_flattened_tasks(iteration_state: TaskIterationState, ctx: WorkflowContext[TaskIterationState]) -> None:
    """Flatten subtasks into the main task list and update iteration counters.

    If no decomposition happened we fast-forward the loop counter to avoid
    unnecessary iterations. Resets the `curr_index` and updates `total_tasks`.
    """
    logger.info("Committing flattened tasks for loop %s", iteration_state.curr_loop)
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        logger.exception("commit_flattened_tasks: plan not found or wrong type")
        raise ValueError("plan content state not found")

    flatten_result = flatten_tasks(plan.tasks)
    plan.tasks = flatten_result.tasks
    no_decomposition_happened = flatten_result.no_decomposition_happened

    iteration_state.curr_loop = iteration_state.max_loops if no_decomposition_happened else iteration_state.curr_loop + 1
    iteration_state.curr_index = 0
    iteration_state.total_tasks = len(plan.tasks)

    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)
