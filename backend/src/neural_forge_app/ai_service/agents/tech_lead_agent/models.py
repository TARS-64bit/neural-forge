from pydantic import BaseModel, Field

class TechLeadEvaluation(BaseModel):
    """Output schema for the Tech Lead Agent's evaluation"""
    is_atomic: bool
    reasoning: str = Field(
        description="Brief technical explanation of why the task is or is not atomic."
    )
    suggested_breakdown: list[str] | None = Field(
        description="If is_atomic is False, provide 2-4 brief titles for how this should be broken down. If True, leave empty.",
        default=None
    )