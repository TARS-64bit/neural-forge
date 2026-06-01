from agent_framework import Agent

from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

import os
from dotenv import load_dotenv

from neural_forge_app.ai_service.tools.weather import get_weather
load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
MODEL = os.getenv("FOUNDRY_MODEL", "gpt-4.1-mini")

async def weather_agent() -> None:
    # <create_agent>
    client = FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        model=MODEL,
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=[get_weather],
    )
    # </create_agent>

    # <run_agent>
    # Non-streaming: get the complete response at once
    # result = await agent.run("What's the weather like in Seattle?")
    # print(f"Agent: {result}")
    # </run_agent>

    # <run_agent_streaming>
    # Streaming: receive tokens as they are generated
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("What's the weather like in Seattle?", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
    # </run_agent_streaming>


