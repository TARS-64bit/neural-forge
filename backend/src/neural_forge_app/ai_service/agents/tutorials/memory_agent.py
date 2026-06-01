from agent_framework import Agent
from src.neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client
from src.neural_forge_app.ai_service.providers.user_memory_provider import UserMemoryProvider

async def memory_agent() -> None:
    # <create_agent>
    client = get_foundary_client()

    agent = Agent(
        client=client,
        name="MemoryAgent",
        instructions="You are a friendly assistant.",
        context_providers=[UserMemoryProvider()],
    )
    # </create_agent>

    # <run_with_memory>
    session = agent.create_session()

    # The provider doesn't know the user yet — it will ask for a name
    result = await agent.run("Hello! What's the square root of 9?", session=session)
    print(f"Agent: {result}\n")

    # Now provide the name — the provider stores it in session state
    result = await agent.run("My name is Alice", session=session)
    print(f"Agent: {result}\n")

    # Subsequent calls are personalized — name persists via session state
    result = await agent.run("What is 2 + 2?", session=session)
    print(f"Agent: {result}\n")

    # Inspect session state to see what the provider stored
    provider_state = session.state.get("user_memory", {})
    print(f"[Session State] Stored user name: {provider_state.get('user_name')}")
    # </run_with_memory>