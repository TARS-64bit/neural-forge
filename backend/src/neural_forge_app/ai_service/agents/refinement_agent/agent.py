from agent_framework import Agent
from neural_forge_app.ai_service.agents.refinement_agent.instructions import build_refinement_instructions
from neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client
from neural_forge_app.ai_service.models.shared_responses import InitialTaskList

def create_refinement_agent():
    client = get_foundary_client()
    return Agent(
        client=client,
        instructions=build_refinement_instructions(),
        default_options={"response_format": InitialTaskList}, # type: ignore
        name="RefinementAgent",
    )