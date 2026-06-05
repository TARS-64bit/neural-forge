from azure.search.documents import SearchIndexingBufferedSender

from  neural_forge_app.ai_service.core.config import endpoint, credential, index_name


def upload_code(code_chunks: list | None = None) -> None:

    if not code_chunks:
        print("No code chunks to upload.")
        return
    
    if not isinstance(code_chunks[0], dict):
        print("Code chunks are not in the expected dictionary format. Please check the preprocessor output.")
        return
    
    if not endpoint:
        print("Azure Search endpoint is not configured. Please set the AZURE_SEARCH_ENDPOINT environment variable.")
        return

    with SearchIndexingBufferedSender(endpoint=endpoint, index_name=index_name, credential=credential) as client:
        client.upload_documents(documents=code_chunks)
