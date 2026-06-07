import asyncio

from neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase

async def main() -> None:
    execute_planning_phase("Update the main page to remove the next js logo and add a sidemenu as well for the about and contact pages")
    


if __name__ == "__main__":
    asyncio.run(main())