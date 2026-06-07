from agent_framework import Agent
from neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client
from neural_forge_app.ai_service.agents.pm_agent.instructions import build_pm_instructions
from neural_forge_app.ai_service.models.shared_responses import InitialPlan
from neural_forge_app.ai_service.tools.codebase_search_tools.get_code_search_tool import CodebaseSearchTools

def create_pm_agent(index_name: str):
        """Initializes the inner MAF Agent with client and instructions."""
        client = get_foundary_client()
        search_tools = CodebaseSearchTools(index_name=index_name)
        
        return Agent(
            name="PMAgent",
            client=client,
            instructions=build_pm_instructions(),
            default_options={"response_format": InitialPlan}, # type: ignore
            tools=[search_tools.search_codebase]
        )