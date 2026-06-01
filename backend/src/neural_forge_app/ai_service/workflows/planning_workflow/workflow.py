from agent_framework import (AgentExecutorRequest, AgentExecutorResponse, Case, Default, WorkflowContext, executor, WorkflowBuilder, Message)
from src.neural_forge_app.ai_service.agents.refinement_agent.agent import create_refinement_agent
from src.neural_forge_app.ai_service.agents.pm_agent.agent import  create_pm_agent
from src.neural_forge_app.ai_service.agents.pm_agent.models import InitialPlan, Plan,Task
from src.neural_forge_app.ai_service.agents.tech_lead_agent.agent import  create_tech_lead_agent
# from src.neural_forge_app.core.config import is_mock_mode
from pydantic import BaseModel
from typing import Any, Literal

#### Pending tasks: ID and ordering logic for tasks and subtasks. For now we are relying on list order, but this is brittle and we should have explicit IDs and parent-child relationships.

class TaskIterationState(BaseModel):
    curr_index:int
    curr_loop:int
    total_tasks: int
    max_loops: int

DecompositionStatus = Literal["complete", "pending_decomposition", "complete_decomposition"]

def is_loop_status(expected:DecompositionStatus):

    def condition(iteration_state: Any) -> bool:
        # Defensive guard. If a non LoopIndexes appears end decomposition.
        if not isinstance(iteration_state, TaskIterationState):
            return False

        if expected == "complete":
            return  iteration_state.curr_loop >= iteration_state.max_loops

        if expected == "pending_decomposition":
            # Only pending if we haven't hit max loops AND we have tasks left
            return (iteration_state.curr_loop < iteration_state.max_loops) and \
                   (iteration_state.curr_index < iteration_state.total_tasks)

        return iteration_state.curr_index >= iteration_state.total_tasks

    return condition

def is_task_atomic(expected: bool):

    def condition(response: AgentExecutorResponse) -> bool:
       
        print(f"\nEvaluating atomicity condition with expected={expected} and actual response={response.agent_response.value}\n")
        if not response.agent_response.value:
            return False

        return bool(response.agent_response.value.is_atomic) is expected

    return condition

class FlattenTasksResult(BaseModel):
    tasks: list[Task]
    no_decomposition_happened: bool

def flatten_tasks(tasks: list[Task]) -> FlattenTasksResult:
    result: list[Task] = []
    no_decomposition_happened = True
    for task in tasks:
        if task.subtasks:
            no_decomposition_happened = False
            result.extend(subtask.to_task() for subtask in task.subtasks)
        else:
            result.append(task)
    return FlattenTasksResult(tasks=result, no_decomposition_happened=no_decomposition_happened)

ExtractorOutcome = Literal["loopback", "to_tech_lead", "to_flatten_tasks"]

def check_extractor_output(expected:ExtractorOutcome):

    def condition(data: AgentExecutorRequest | TaskIterationState) -> bool:
        if expected == "to_tech_lead":
            return isinstance(data, AgentExecutorRequest)
        if expected == "loopback":
            return isinstance(data, TaskIterationState) and data.curr_index < data.total_tasks
        if expected == "to_flatten_tasks":
            return isinstance(data, TaskIterationState) and data.curr_index >= data.total_tasks
        return False
    
    return condition

class POPrompt(BaseModel):
    prompt: str
    max_loops: int = 3

@executor(id="initialize_workflow")
async def initialize_workflow(po_prompt: POPrompt, ctx: WorkflowContext[AgentExecutorRequest]) -> None:
    ctx.set_state("iteration_state", TaskIterationState(curr_index=0, curr_loop=0, total_tasks=0, max_loops=po_prompt.max_loops))

    await ctx.send_message(
        AgentExecutorRequest(messages=[Message("user", contents=[po_prompt.prompt])], should_respond=True)
    )

def transform_initial_plan_to_plan(initial_plan: InitialPlan) -> Plan:
    return Plan(
        tasks=[task.to_task() for task in initial_plan.tasks],
        scope_analysis=initial_plan.scope_analysis,
        technical_assumptions=initial_plan.technical_assumptions
    )

@executor(id="init_plan_state")
async def init_plan_state(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    if not response.agent_response.value or not response.agent_response.value.tasks:
        raise ValueError("response state not found")
    
    print(f"\nReceived initial plan from PM Agent: {response.agent_response.value}\n")

    # Transform the initial plan to the final plan format
    plan = transform_initial_plan_to_plan(response.agent_response.value)

    ctx.set_state("plan", plan)
    iteration_state = ctx.get_state("iteration_state")
    
    if not isinstance(iteration_state, TaskIterationState):
        raise ValueError("iteration_state content state not found or of wrong type")
    
    iteration_state.total_tasks = len(plan.tasks)

    ctx.set_state("iteration_state", iteration_state)
    
    await ctx.send_message(iteration_state)

@executor(id="mark_task_atomic")
async def mark_task_atomic(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    
    print(f"\nMarking task as atomic: {response.agent_response.value}\n")
    if not response.agent_response.value:
        raise ValueError("response content state not found or of wrong type")

    iteration_state = ctx.get_state("iteration_state")
    plan = ctx.get_state("plan")

    if not isinstance(iteration_state, TaskIterationState):
        raise ValueError("iteration_state content state not found or of wrong type")

    if not isinstance(plan, Plan):
        raise ValueError("plan content state not found or of wrong type")
    
    plan.tasks[iteration_state.curr_index].is_sufficiently_atomic = True

    iteration_state.curr_index += 1
    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)

@executor(id="extract_next_task")
async def extract_next_task(iteration_state: TaskIterationState, ctx: WorkflowContext[AgentExecutorRequest | TaskIterationState]) -> None:
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        raise ValueError("plan content state not found")
    
    task = plan.tasks[iteration_state.curr_index]

    print(f"\nExtracting task for iteration {iteration_state.curr_loop}, index {iteration_state.curr_index}: {task.title}\n")

    if task.is_sufficiently_atomic:
        print(f"\nTask '{task.title}' is marked as sufficiently atomic. Skipping refinement.\n")
        iteration_state.curr_index += 1
        ctx.set_state("iteration_state", iteration_state)
        await ctx.send_message(iteration_state)
        return

    task_context = f"Title: {task.title}\nDescription: {task.description}\nCriteria: {task.acceptance_criteria}"

    await ctx.send_message(
        AgentExecutorRequest(messages=[Message("user", contents=[task_context])], should_respond=True)
    )

@executor(id="insert_subtasks")
async def insert_subtasks(response: AgentExecutorResponse, ctx: WorkflowContext[TaskIterationState]) -> None:
    
    print(f"\nReceived subtasks from Refinement Agent: {response.agent_response.value}\n")

    if not response.agent_response.value or response.agent_response.value.tasks is None:
        raise ValueError("response content state not found")

    iteration_state = ctx.get_state("iteration_state")
    plan = ctx.get_state("plan")

    if not isinstance(iteration_state, TaskIterationState):
        raise ValueError("iteration_state content state not found or of wrong type")
    
    if not isinstance(plan, Plan):
        raise ValueError("plan content state not found or of wrong type")

    new_subtasks = response.agent_response.value.tasks

    # Defensive check
    if not new_subtasks:
        print(f"⚠️ No subtasks found to expand vague task: {plan.tasks[iteration_state.curr_index].title}")
    else:
        plan.tasks[iteration_state.curr_index].subtasks = new_subtasks

    iteration_state.curr_index += 1
    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)

@executor(id="commit_flattened_tasks")
async def commit_flattened_tasks(iteration_state: TaskIterationState, ctx: WorkflowContext[TaskIterationState]) -> None:
    
    print(f"\nCommitting flattened tasks for loop {iteration_state.curr_loop}\n")
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        raise ValueError("plan content state not found")

    flatten_result = flatten_tasks(plan.tasks)
    plan.tasks = flatten_result.tasks
    no_decomposition_happened = flatten_result.no_decomposition_happened

    iteration_state.curr_loop = iteration_state.max_loops if no_decomposition_happened else iteration_state.curr_loop + 1
    iteration_state.curr_index = 0
    iteration_state.total_tasks = len(plan.tasks)

    ctx.set_state("plan", plan)
    ctx.set_state("iteration_state", iteration_state)

    await ctx.send_message(iteration_state)

@executor(id="yield_final_plan")
async def yield_final_plan(iteration_state: TaskIterationState, ctx: WorkflowContext[None, Plan]) -> None:
    plan = ctx.get_state("plan")

    if not isinstance(plan, Plan):
        raise ValueError("plan content state not found")

    await ctx.yield_output(plan)

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
            # Case(is_loop_status("complete"), yield_final_plan),
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            Case(is_loop_status("complete_decomposition"), commit_flattened_tasks),
            Default(target=yield_final_plan)
        ]    
    )
    .add_switch_case_edge_group(
        extract_next_task,
        [
            # Case(check_extractor_output("to_tech_lead"), tech_lead),
            Case(check_extractor_output("loopback"), extract_next_task),
            Case(check_extractor_output("to_flatten_tasks"), commit_flattened_tasks),
            Default(target=tech_lead)  # If for some reason we don't get a clear signal, route to tech lead by default
        ]
    )
    .add_switch_case_edge_group(
        tech_lead,
        [
            # Case(is_task_atomic(True), mark_task_atomic),
            Case(is_task_atomic(False), refinement_agent),
            Default(target=mark_task_atomic)  # If for some reason we don't get a clear atomicity signal, assume it's atomic to avoid infinite loops
        ]
    )
    .add_switch_case_edge_group(
        mark_task_atomic,
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            # Case(is_loop_status("complete_decomposition"), commit_flattened_tasks),
            Default(target=commit_flattened_tasks) 
        ]
    )
    .add_edge(refinement_agent, insert_subtasks)
    .add_switch_case_edge_group(
        insert_subtasks,
        [
            Case(is_loop_status("pending_decomposition"), extract_next_task),
            # Case(is_loop_status("complete_decomposition"), commit_flattened_tasks),
            Default(target=commit_flattened_tasks) 
        ]
    )
    .add_switch_case_edge_group(
        commit_flattened_tasks, 
        [
            # Case(is_loop_status("complete"), yield_final_plan),
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
#         from src.neural_forge_app.agents.pm_agent.mocks import get_mock_initial_plan
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
