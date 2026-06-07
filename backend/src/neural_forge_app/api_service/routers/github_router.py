import httpx
from ..models import ExportIssuesRequest
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api")

@router.post("/export-issues")
async def github_router(request: ExportIssuesRequest):
    """Creates GitHub Issues using the provided PAT."""
    headers = {
        "Authorization": f"Bearer {request.github_pat}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f"https://api.github.com/repos/{request.repo_owner}/{request.repo_name}/issues"
    
    created_urls = []
    
    async with httpx.AsyncClient() as client:
        for issue in request.issues:
            response = await client.post(url, headers=headers, json={
                "title": issue.title,
                "body": issue.body
            })
            
            if response.status_code == 201:
                created_urls.append(response.json().get("html_url"))
            else:
                # If one fails, stop and return the error
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    return {"status": "success", "urls": created_urls}