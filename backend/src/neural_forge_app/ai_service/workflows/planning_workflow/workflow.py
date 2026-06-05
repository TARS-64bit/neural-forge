from agent_framework import (
    Case,
    Default,
    WorkflowBuilder
)
from neural_forge_app.ai_service.agents.refinement_agent.agent import create_refinement_agent
from neural_forge_app.ai_service.agents.pm_agent.agent import create_pm_agent
from neural_forge_app.ai_service.models.shared_responses import Plan
from neural_forge_app.ai_service.agents.tech_lead_agent.agent import create_tech_lead_agent
from neural_forge_app.ai_service.workflows.planning_workflow.state.planning_state import (
    POPrompt,
    is_loop_status,
    is_task_atomic,
    check_extractor_output,
)

# Executors have been moved into the `executors` package to keep the workflow
# file focused on wiring and orchestration. Each executor module contains its
# own logging and comments.
from neural_forge_app.ai_service.workflows.planning_workflow.executors import (
    initialize_workflow,
    init_plan_state,
    mark_task_atomic,
    extract_next_task,
    insert_subtasks,
    commit_flattened_tasks,
    yield_final_plan,
)

#### Pending tasks: ID and ordering logic for tasks and subtasks. For now we are relying on list order, but this is brittle and we should have explicit IDs and parent-child relationships.

pm_agent = create_pm_agent()
tech_lead = create_tech_lead_agent()
refinement_agent = create_refinement_agent()

workflow = (
    WorkflowBuilder(start_executor=initialize_workflow)
    .add_edge(initialize_workflow, pm_agent)
    .add_edge(pm_agent, init_plan_state)
    .add_switch_case_edge_group(
        init_plan_state, 
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            Case(is_loop_status("complete_decomposition"), commit_flattened_tasks),
            Default(target=yield_final_plan)
        ]    
    )
    .add_switch_case_edge_group(
        extract_next_task,
        [
            Case(check_extractor_output("loopback"), extract_next_task),
            Case(check_extractor_output("to_flatten_tasks"), commit_flattened_tasks),
            Default(target=tech_lead)  # If for some reason we don't get a clear signal, route to tech lead by default
        ]
    )
    .add_switch_case_edge_group(
        tech_lead,
        [
            Case(is_task_atomic(False), refinement_agent),
            Default(target=mark_task_atomic)  # If for some reason we don't get a clear atomicity signal, assume it's atomic to avoid infinite loops
        ]
    )
    .add_switch_case_edge_group(
        mark_task_atomic,
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            Default(target=commit_flattened_tasks) 
        ]
    )
    .add_edge(refinement_agent, insert_subtasks)
    .add_switch_case_edge_group(
        insert_subtasks,
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            Default(target=commit_flattened_tasks) 
        ]
    )
    .add_switch_case_edge_group(
        commit_flattened_tasks, 
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            Default(target=yield_final_plan)
        ]
    )
    .build()
)

# async def generate_initial_plan(pm_agent: PMAgent, po_prompt: str) -> Plan | None:
#     """
#     Acts as a factory: Returns a mock plan if in local/testing mode, 
#     otherwise makes the real LLM call.
#     """
#     if is_mock_mode():
#         print("🟡 CONFIG: Running in MOCK mode. Returning golden dataset.")
#         # Lazy import: Only loads the mock file if we actually need it
#         from neural_forge_app.agents.pm_agent.mocks import get_mock_initial_plan
#         return get_mock_initial_plan()
    
#     print("🟢 CONFIG: Running in PROD mode. Calling real PM Agent...")
#     response = await pm_agent.generate_plan(po_prompt)
#     return response

async def execute_planning_phase(raw_prompt: str) -> Plan | None:

    initial_input = POPrompt(prompt=raw_prompt, max_loops=3)

    final_plan = await workflow.run(initial_input)
    outputs = final_plan.get_outputs()

    print("✅ Planning Phase Complete!\n\n\n\n\n")
    print(outputs)
    return outputs[0] if outputs else None
