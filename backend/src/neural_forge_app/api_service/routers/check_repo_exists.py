import os
from typing import Dict, Union

from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.core.exceptions import ResourceNotFoundError
from fastapi import APIRouter, HTTPException

from ..models import RepoIngestRequest

router = APIRouter(prefix="/api")


@router.post("/check-repo")
async def check_repo_exists(request: RepoIngestRequest) -> Dict[str, Union[bool, str]]:
    try:
        parts = request.github_url.rstrip("/").split("/")
        repo_owner, repo_name = parts[-2], parts[-1]

        safe_owner = "".join(e for e in repo_owner if e.isalnum()).lower()
        safe_repo = "".join(e for e in repo_name if e.isalnum()).lower()
        safe_branch = "".join(e for e in request.branch if e.isalnum()).lower()

        dynamic_index_name = f"idx-{safe_owner}-{safe_repo}-{safe_branch}"

        index_client = SearchIndexClient(
            endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )

        try:
            index_client.get_index(dynamic_index_name)
            return {"exists": True, "dynamic_index_name": dynamic_index_name}
        except ResourceNotFoundError:
            return {"exists": False, "dynamic_index_name": dynamic_index_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))