
from agent_framework import Agent
from neural_forge_app.ai_service.agents.tech_lead_agent.instructions import build_tech_lead_instructions
from neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client
from neural_forge_app.ai_service.agents.tech_lead_agent.models import TechLeadEvaluation

def create_tech_lead_agent():
    client = get_foundary_client()
    return Agent(
        client=client,
        name="TechLeadAgent",
        instructions=build_tech_lead_instructions(),
        default_options={"response_format": TechLeadEvaluation}, # type: ignore
    )
    


