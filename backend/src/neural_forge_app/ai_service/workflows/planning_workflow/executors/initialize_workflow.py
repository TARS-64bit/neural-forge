import logging
from agent_framework import AgentExecutorRequest, Message, WorkflowContext, executor
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import POPrompt, TaskIterationState

logger = logging.getLogger(__name__)


@executor(id="initialize_workflow")
async def initialize_workflow(po_prompt: POPrompt, ctx: WorkflowContext[AgentExecutorRequest]) -> None:
    """Initialize iteration state and send the initial prompt to the PM agent.

    Sets `iteration_state` in the workflow context and dispatches the initial
    `AgentExecutorRequest` containing the PO prompt.
    """
    ctx.set_state("iteration_state", TaskIterationState(curr_index=0, curr_loop=0, total_tasks=0, max_loops=po_prompt.max_loops))

    logger.debug("Initialized iteration_state with max_loops=%s", po_prompt.max_loops)

    await ctx.send_message(
        AgentExecutorRequest(messages=[Message("user", contents=[po_prompt.prompt])], should_respond=True)
    )
