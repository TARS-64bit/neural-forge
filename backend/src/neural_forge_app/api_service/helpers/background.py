from neural_forge_app.ai_service.rag.initializer import initialize_codebase_index
from neural_forge_app.api_service.helpers.get_dynamic_index_name import get_dynamic_index_name

from ..task_registry import TASK_DB

def run_background_ingestion(task_id: str, repo_owner: str, repo_name: str, branch: str, pat: str) -> None:
    """Runs the long-running ingestion flow and updates the shared task registry."""
    try:
        dynamic_index = get_dynamic_index_name(repo_owner, repo_name, branch)

        initialize_codebase_index(repo_owner=repo_owner, repo_name=repo_name, branch=branch, pat=pat, index_name=dynamic_index)
        TASK_DB[task_id] = "completed"
    except Exception as exc:
        print(f"Ingestion failed: {exc}")
        TASK_DB[task_id] = f"failed: {str(exc)}"
