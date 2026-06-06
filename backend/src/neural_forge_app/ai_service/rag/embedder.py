import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import List
load_dotenv()

from neural_forge_app.ai_service.rag.models import CodeChunk

oai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT", "")
)
EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

def embed_chunks(chunks: List[CodeChunk]) -> List[CodeChunk]:
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    for chunk in chunks:
        # Call Azure OpenAI to convert the code text into a vector
        response = oai_client.embeddings.create(
            input=chunk["content"], 
            model=EMBEDDING_MODEL
        )
        
        # Save the vector array into the chunk dictionary
        chunk["embedding"] = response.data[0].embedding
        
    return chunks