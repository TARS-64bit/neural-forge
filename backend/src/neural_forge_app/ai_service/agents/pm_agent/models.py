from pydantic import BaseModel, Field

class SubTask(BaseModel):
    """A leaf-level task — cannot have further subtasks."""
    id: int
    type: str
    title: str
    description: str
    acceptance_criteria: list[str]
    dependencies: list[int]

    def to_task(self, is_sufficiently_atomic: bool | None = None) -> "Task":
        return Task(
            **self.model_dump(),
            subtasks=None,
            is_sufficiently_atomic=is_sufficiently_atomic
        )

class Task(BaseModel):
    id: int
    type: str
    title: str
    description: str
    acceptance_criteria: list[str]
    subtasks: list[SubTask] | None = None   # max 1 level, enforced by type
    dependencies: list[int]
    is_sufficiently_atomic: bool | None = Field(description="Ignore, do not fill this field, keep it None.")

class TaskList(BaseModel):
    tasks: list[Task]

class InitialTaskList(BaseModel):
    tasks: list[SubTask]

class Plan(TaskList):
    scope_analysis: str = Field(description="Analyze the PO's requirement. What sub-systems need to be built? What are the hidden complexities?")
    technical_assumptions: list[str] = Field(description="List assumptions made about the tech stack or missing details.")

class InitialPlan(InitialTaskList):
    scope_analysis: str = Field(description="Analyze the PO's requirement. What sub-systems need to be built? What are the hidden complexities?")
    technical_assumptions: list[str] = Field(description="List assumptions made about the tech stack or missing details.")