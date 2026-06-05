import asyncio

from neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase

async def main() -> None:
    await execute_planning_phase("Update the main page to remove the next js logo")
    


if __name__ == "__main__":
    asyncio.run(main())