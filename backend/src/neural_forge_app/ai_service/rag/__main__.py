from neural_forge_app.ai_service.rag.embedder import embed_chunks
from neural_forge_app.integrations.github_api import ephemeral_clone
from neural_forge_app.ai_service.rag.preprocessor import preprocess_codebase
from neural_forge_app.integrations.ingestion_pipeline import ingest_codebase

def initialize_codebase_index(repo_owner: str, repo_name: str, branch: str = "main"):
    """
    Clones the target repository, processes the code into vectors, 
    and uploads it to Azure AI Search for the Agents to use.
    """
    print(f"Starting RAG Initialization for: {repo_owner}/{repo_name} (Branch: {branch})")
    
    # The 'with' block opens the temporary workspace securely
    with ephemeral_clone(repo_owner, repo_name, branch=branch) as (repo_path, git_repo):
        
        print("1. Pre-processing codebase for RAG...")
        # Reads the code and breaks it into AST syntax-aware chunks
        raw_chunks = preprocess_codebase(repo_path)
        
        print(f"2. Generating embeddings for {len(raw_chunks)} chunks...")
        # Calls Azure OpenAI to vectorize the text
        embedded_chunks = embed_chunks(raw_chunks)

        print("3. Uploading to Azure AI Search...")
        # Creates the Index schema (if missing) and uploads the chunks
        ingest_codebase(create_index=True, code_chunks=embedded_chunks)
        
    # Once the 'with' block ends, the temp directory is instantly deleted!
    print("✅ Initialization complete! The codebase is ready for the Planner Agent.")

if __name__ == "__main__":
    initialize_codebase_index(repo_owner="TARS-64bit", repo_name="dummy")