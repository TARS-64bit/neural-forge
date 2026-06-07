import os
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)

# Keep the basic configs you still need
endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
credential = DefaultAzureCredential()
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openai_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
azure_openai_embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Import only index builder and uploader
from .index_builder import build_and_create_index
from .uploader import upload_code

def ingest_codebase(index_name: str, create_index: bool = True, code_chunks: list | None = None):
    """Orchestrate index creation and code upload."""
    
    if create_index:
        build_and_create_index(index_name)
        print(f"Index '{index_name}' created or updated successfully")
        
    if code_chunks is not None:
        upload_code(index_name, code_chunks)
        print(f"Uploaded {len(code_chunks)} code chunks to index '{index_name}'")
        
    print("Codebase ingestion complete!")