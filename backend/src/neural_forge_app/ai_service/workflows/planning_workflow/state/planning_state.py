from pydantic import BaseModel
from typing import Any, Literal, List

from neural_forge_app.ai_service.models.shared_responses import Task

# Shared state and helper utilities for the planning workflow.

class TaskIterationState(BaseModel):
    curr_index: int
    curr_loop: int
    total_tasks: int
    max_loops: int


DecompositionStatus = Literal["complete", "pending_decomposition", "complete_decomposition"]


def is_loop_status(expected: DecompositionStatus):
    """Return a predicate that checks the current loop/index status."""

    def condition(iteration_state: Any) -> bool:
        if not isinstance(iteration_state, TaskIterationState):
            return False

        if expected == "complete":
            return iteration_state.curr_loop >= iteration_state.max_loops

        if expected == "pending_decomposition":
            return (iteration_state.curr_loop < iteration_state.max_loops) and (
                iteration_state.curr_index < iteration_state.total_tasks
            )

        return iteration_state.curr_index >= iteration_state.total_tasks

    return condition


def is_task_atomic(expected: bool):
    """Return a predicate that checks whether an agent marked a task atomic."""

    def condition(response: Any) -> bool:
        # The response is expected to be an AgentExecutorResponse with an
        # `agent_response.value` that exposes `is_atomic`.
        if not getattr(response, "agent_response", None):
            return False

        return bool(response.agent_response.value.is_atomic) is expected

    return condition


class FlattenTasksResult(BaseModel):
    tasks: List[Any]
    no_decomposition_happened: bool


def flatten_tasks(tasks: list[Task]) -> FlattenTasksResult:
    """Flatten one level of subtasks into the task list.

    Returns a tuple-like object with the flattened list and a flag indicating
    whether any decomposition happened.
    """
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


def check_extractor_output(expected: ExtractorOutcome):
    """Return a predicate to check the extractor output shape and intent."""

    def condition(data: Any) -> bool:
        if expected == "to_tech_lead":
            # A request object means we should route to a human/agent for
            # refinement.
            from agent_framework import AgentExecutorRequest

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


def transform_initial_plan_to_plan(initial_plan: Any) -> Any:
    """Convert the PM agent's InitialPlan object into the workflow Plan model.

    This function intentionally keeps a dynamic signature so it can be used
    without causing import-time cycles. Callers should import `InitialPlan`
    and `Plan` from the PM agent models as needed.
    """
    # Defer imports to avoid module-level cycles
    from neural_forge_app.ai_service.models.shared_responses import InitialPlan, Plan

    if not isinstance(initial_plan, InitialPlan):
        raise ValueError("expected InitialPlan")

    return Plan(
        tasks=[task.to_task() for task in initial_plan.tasks],
        scope_analysis=initial_plan.scope_analysis,
        technical_assumptions=initial_plan.technical_assumptions,
    )
