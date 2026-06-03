import logging
from agent_framework import WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState
from neural_forge_app.ai_service.agents.pm_agent.models import Plan

logger = logging.getLogger(__name__)


@executor(id="yield_final_plan")
async def yield_final_plan(iteration_state: TaskIterationState, ctx: WorkflowContext[None, Plan]) -> None:
    """Retrieve the final plan from state and yield it as workflow output."""
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        logger.exception("yield_final_plan: plan not found or wrong type")
        raise ValueError("plan content state not found")

    logger.info("Yielding final plan with %s tasks", len(plan.tasks))

    await ctx.yield_output(plan)
