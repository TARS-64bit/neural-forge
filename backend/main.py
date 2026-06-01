import asyncio

from src.neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase

async def main() -> None:
    await execute_planning_phase("We want to create a simple html portfolio page.")


if __name__ == "__main__":
    asyncio.run(main())