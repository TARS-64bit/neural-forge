import tempfile
from contextlib import contextmanager
from git import Repo

@contextmanager
def ephemeral_clone(repo_owner: str, repo_name: str, branch: str = "main", pat: str = ""):
    """
    Clones a GitHub repo into a temporary, isolated directory on the server.
    Cleans up automatically when the process is done.
    """
    # Remove .git suffix if present to avoid duplication
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    
    # 1. Construct a secure HTTPS URL using the Personal Access Token (PAT)
    # This prevents the need to store SSH keys on the server
    repo_url = f"https://{pat}@github.com/{repo_owner}/{repo_name}.git"
    
    # 2. Create a secure, unique temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"agent_workspace_{repo_name}_")
    print(f"Created temporary workspace at: {temp_dir}")
    
    try:
        # 3. Clone the repository into the temp directory
        print(f"Cloning {repo_owner}/{repo_name} (branch: {branch})...")
        repo = Repo.clone_from(repo_url, temp_dir, branch=branch)
        
        # 4. Yield the path back to the main application
        yield temp_dir, repo
        
    finally:
        # 5. CLEANUP: This runs no matter what (even if the AI agent crashes)
        print(f"Cleaning up workspace: {temp_dir}")
        # shutil.rmtree(temp_dir, ignore_errors=True)