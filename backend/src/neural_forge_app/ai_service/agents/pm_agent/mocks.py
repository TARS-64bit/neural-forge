# from src.neural_forge_app.agents.pm_agent.models import Plan, Task

# def get_mock_initial_plan() -> Plan:
#     """Returns a hardcoded Plan to bypass the LLM during testing."""
#     return Plan(
#         scope_analysis="Mock analysis for project management tool.",
#         technical_assumptions=["Using Python", "Using PostgreSQL"],
#         tasks=[
#             # Task 1: Good, atomic task
#             Task(
#                 task_id=1,
#                 task_type="setup",
#                 title="Initialize PostgreSQL Database Connection",
#                 description="Create the SQLAlchemy engine and base models.",
#                 acceptance_criteria=["DB connects successfully."],
#                 dependencies=[],
#                 is_sufficiently_atomic=True
#             ),
#             # Task 2: VAGUE (Will be caught by Tech Lead Agent)
#             Task(
#                 task_id=2,
#                 task_type="feature",
#                 title="Implement User Authentication",
#                 description="Build the login API, JWT generation, and User DB model.",
#                 acceptance_criteria=["User can log in."],
#                 dependencies=[1],
#                 is_sufficiently_atomic=True # The AI *thinks* it's atomic, but the Tech Lead should catch it!
#             ),
#             # Task 3: VAGUE (Will be caught by Python heuristic 'dashboard' rule)
#             Task(
#                 task_id=3,
#                 task_type="feature",
#                 title="Build Project Dashboard",
#                 description="Create the frontend React page showing all projects.",
#                 acceptance_criteria=["Dashboard loads."],
#                 dependencies=[2],
#                 is_sufficiently_atomic=True
#             )
#         ]
#     )