import logging
from agent_framework import AgentExecutorResponse, WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import TaskIterationState, transform_initial_plan_to_plan

logger = logging.getLogger(__name__)


@executor(id="init_plan_state")
async def init_plan_state(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    """Handle the PM agent response, transform and store the plan in state.

    Validates incoming response, converts the InitialPlan into the workflow
    `Plan`, updates the iteration state's `total_tasks`, and forwards the
    iteration state to the next executor.
    """
    if not response.agent_response.value or not response.agent_response.value.tasks:
        logger.error("init_plan_state: response missing or empty tasks: %s", response.agent_response.value)
        raise ValueError("response state not found")

    logger.info("Received initial plan from PM Agent: %s", response.agent_response.value)

    plan = transform_initial_plan_to_plan(response.agent_response.value)

    ctx.set_state("plan", plan)
    iteration_state = ctx.get_state("iteration_state")

    if not isinstance(iteration_state, TaskIterationState):
        logger.exception("iteration_state missing or wrong type")
        raise ValueError("iteration_state content state not found or of wrong type")

    iteration_state.total_tasks = len(plan.tasks)

    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)
