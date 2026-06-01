from pydantic import BaseModel, Field

class Task(BaseModel):
    task_id: int
    task_type: str
    title: str
    description: str
    acceptance_criteria: list[str]
    dependencies: list[int]
    is_sufficiently_atomic: bool = Field(description="Must be True ONLY if this task cannot be broken down into smaller database/backend/frontend components.")

class TaskList(BaseModel):
    tasks: list[Task]

class Plan(TaskList):
    scope_analysis: str = Field(description="Analyze the PO's requirement. What sub-systems need to be built? What are the hidden complexities?")
    technical_assumptions: list[str] = Field(description="List assumptions made about the tech stack or missing details.")