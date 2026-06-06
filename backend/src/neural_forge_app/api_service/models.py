from pydantic import BaseModel

class RepoIngestRequest(BaseModel):
    github_url: str
    github_pat: str

class FeaturePlanRequest(BaseModel):
    feature_prompt: str
    repo_owner: str 
    repo_name: str