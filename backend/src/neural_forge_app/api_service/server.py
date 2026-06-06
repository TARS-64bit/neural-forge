import os
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import RepoIngestRequest, FeaturePlanRequest

# Import your AI and Ingestion logic
from neural_forge_app.ai_service.rag.initializer import initialize_codebase_index
from neural_forge_app.ai_service.workflows.planning_workflow.workflow import execute_planning_phase
# Assume you have a function that runs your PM Agent
# from neural_forge_app.ai_service.orchestrator import run_planner_agent 

app = FastAPI(title="Neural Forge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SIMPLE TASK TRACKER ---
# Stores statuses: "processing", "completed", "failed"
TASK_DB = {}

# --- HELPER FUNCTION ---
def run_background_ingestion(task_id: str, repo_owner: str, repo_name: str, pat: str):
    """Runs the long RAG pipeline and updates the Task DB when done."""
    try:
        # Temporarily set the PAT for the Git clone integration
        os.environ["GITHUB_PAT"] = pat
        
        # Call your existing ingestion script
        initialize_codebase_index(repo_owner=repo_owner, repo_name=repo_name)
        
        TASK_DB[task_id] = "completed"
    except Exception as e:
        print(f"Ingestion failed: {e}")
        TASK_DB[task_id] = f"failed: {str(e)}"


# --- ROUTE 1: Start Ingestion ---
@app.post("/api/ingest")
async def start_ingestion(request: RepoIngestRequest, background_tasks: BackgroundTasks):
    # 1. Parse the GitHub URL (e.g., https://github.com/TARS-64bit/dummy)
    try:
        parts = request.github_url.rstrip("/").split("/")
        repo_owner, repo_name = parts[-2], parts[-1]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format.")

    # 2. Generate a unique ID for this loading phase
    task_id = str(uuid.uuid4())
    TASK_DB[task_id] = "processing"

    # 3. Tell FastAPI to run the ingestion in the background!
    background_tasks.add_task(
        run_background_ingestion, 
        task_id, 
        repo_owner, 
        repo_name, 
        request.github_pat
    )

    # 4. Instantly return the ID so the frontend can show a loading spinner
    return {
        "message": "Ingestion started",
        "task_id": task_id,
        "repo_owner": repo_owner,
        "repo_name": repo_name
    }


# --- ROUTE 2: Check Ingestion Status ---
@app.get("/api/status/{task_id}")
async def check_status(task_id: str):
    status = TASK_DB.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_id": task_id, "status": status}



# --- ROUTE 3: Run the Agent ---
@app.post("/api/plan")
async def generate_plan(request: FeaturePlanRequest):
    """
    Called after ingestion is complete. 
    Runs the Multi-Agent Workflow using the newly created Azure Index.
    """
    try:
        # Call your workflow with the user's prompt
        final_plan = await execute_planning_phase(request.feature_prompt)
        
        if not final_plan:
            raise HTTPException(status_code=500, detail="Workflow failed to generate a plan.")
        
        # safe_plan_dict = final_plan.model_dump()
            
        return {
            "status": "success",
            "plan": final_plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))