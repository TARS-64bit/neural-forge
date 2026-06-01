from agent_framework import Agent
from src.neural_forge_app.ai_service.agents.refinement_agent.instructions import build_refinement_instructions
from src.neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client
from src.neural_forge_app.ai_service.agents.pm_agent.models import InitialTaskList

def create_refinement_agent():
    client = get_foundary_client()
    return Agent(
        client=client,
        instructions=build_refinement_instructions(),
        default_options={"response_format": InitialTaskList}, # type: ignore
        name="RefinementAgent",
    )


    # async def generate_plan(self, po_prompt: str, ctx: WorkflowContext[Plan | None]) -> Plan | None:
    #     """Asks the LLM to generate an initial plan from the user's prompt."""
    #     # response = await self._agent.run(
    #     #     po_prompt, 
    #     #     options={"response_format": Plan}
    #     # )
    #     return self._agent
    #     await ctx.send_message(response.value)

    # async def expand_vague_task(self, vague_task: Task) -> TaskList | None:
    #     """Asks the LLM to break down a specific vague task into smaller subtasks."""
    #     instructions = build_pm_refinement_instructions(vague_task)
    #     self._agent.
    #     response = await self._agent.run(
    #         instructions, 
    #         options={"response_format": TaskList}
    #     )
    #     return response.value 