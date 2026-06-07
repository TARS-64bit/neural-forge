from pydantic import BaseModel, Field

class RepoIngestRequest(BaseModel):
    github_url: str
    github_pat: str
    branch: str = "main"

class FeaturePlanRequest(BaseModel):
    feature_prompt: str
    repo_owner: str 
    repo_name: str
    branch: str = "main"
    max_loops: int = Field(
        default=3, 
        ge=1, # Greater than or equal to 1
        le=8, # Less than or equal to 8
        description="The maximum number of agentic decomposition loops. Must be between 1 and 8."
    )

class GitHubIssue(BaseModel):
    title: str
    body: str

class ExportIssuesRequest(BaseModel):
    github_pat: str
    repo_owner: str
    repo_name: str
    issues: list[GitHubIssue]
