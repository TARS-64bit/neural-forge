from agent_framework import Agent

from src.neural_forge_app.ai_service.core.get_foundary_client import get_foundary_client

"""
Multi-Turn Conversations — Use AgentSession to maintain context

This sample shows how to keep conversation history across multiple calls
by reusing the same session object.
"""


async def session_chat_agent() -> None:
    # <create_agent>
    client = get_foundary_client()

    agent = Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    # </create_agent>

    # <multi_turn>
    # Create a session to maintain conversation history
    session = agent.create_session()

    # First turn
    result = await agent.run("My name is Alice and I love hiking.", session=session)
    print(f"Agent: {result}\n")
    print(f"Agent result.text: {result.text}\n")
    print(f"Agent result.messages: {result.messages}\n")
    # Access individual content items
    for message in result.messages:    
        print(f"message.role: {message.role}, message.text: {message.text}, ")

    # Second turn — the agent should remember the user's name and hobby
    result = await agent.run("What do you remember about me?", session=session)
    print(f"Agent: {result}")
    # </multi_turn>