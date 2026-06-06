import os
from typing import Annotated
from agent_framework import tool
from azure.identity import DefaultAzureCredential
from pydantic import Field

from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

# We use a Class because it shares dependencies (the clients) 
# exactly as recommended in the "class with multiple function tools" section of the docs.
class CodebaseSearchTools:
    def __init__(self) -> None:
        """Initialize the Azure clients once so they can be reused."""
        self.oai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT", "")
        )
        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
            index_name=os.getenv("AZURE_SEARCH_INDEX", "codebase-search-index"),
            credential=DefaultAzureCredential()
        )
        self.embed_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

    @tool(
        name="search_github_codebase",
        description=(
            "MANDATORY FIRST STEP: Use this tool to search the existing codebase. "
            "Pass specific architectural concepts, filenames, or function names. "
            "If the first query doesn't find what you need, call this tool again with a different query. "
            "Output contains the file path and the raw code."
        )
    )
    def search_codebase(
        self,
        query: Annotated[str, Field(description="The descriptive search query (e.g., 'auth controller logic' or 'User model').")]
    ) -> str:
        """Searches the codebase for specific files, functions, or architecture."""
        print(f"\n[Agent Tool] Searching for: '{query}'")
        
        try:
            print("[Agent Tool] Step A: Contacting Azure OpenAI...")
            embed_res = self.oai_client.embeddings.create(input=query, model=self.embed_model)
            vector_query = VectorizedQuery(vector=embed_res.data[0].embedding, k=5, fields="embedding")
        except Exception as e:
            print(f"[Agent Tool] ERROR during embedding: {str(e)}")
            return f"FAILED AT AZURE OPENAI: {str(e)}"
            
        try:
            print("[Agent Tool] Step B: Contacting Azure AI Search...")
            results = self.search_client.search(
                search_text=query, 
                vector_queries=[vector_query], 
                top=5
            )
        except Exception as e:
            print(f"[Agent Tool] ERROR during AI search: {str(e)}")
            return f"FAILED AT AZURE AI SEARCH: {str(e)}"

        context = ""
        for doc in results:
            context += f"### FILE: {doc['filepath']} (Language: {doc['language']})\n"
            context += f"```\n{doc['content']}\n```\n"
            context += "-" * 50 + "\n"
            
        return context if context else "No matching code found. Try rephrasing your search query."