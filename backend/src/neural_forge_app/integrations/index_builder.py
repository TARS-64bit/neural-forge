from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters,
    HnswAlgorithmConfiguration, SearchField, SearchIndex,
    SemanticConfiguration, SemanticField, SemanticPrioritizedFields,
    SemanticSearch, VectorSearch, VectorSearchProfile
)

from neural_forge_app.ai_service.core.config import (
    endpoint, credential,
    azure_openai_endpoint, azure_openai_embedding_deployment,
    azure_openai_embedding_model
)


def build_and_create_index(index_name: str):
    if not index_name:
        raise ValueError("Azure Search index name is not set. Please set the AZURE_SEARCH_INDEX environment variable.")
    
    index = SearchIndex(
        name=index_name,
        fields=[
            SearchField(name="id", type="Edm.String", key=True, filterable=True, sortable=True, facetable=True),
            SearchField(name="content", type="Edm.String", searchable=True, filterable=False, sortable=False, facetable=False),
            SearchField(
                name="embedding", 
                type="Collection(Edm.Single)", 
                searchable=True,
                stored=False, 
                vector_search_dimensions=1536,  # 1536 if using text-embedding-3-small (use 3072 if using large!)
                vector_search_profile_name="hnsw_profile" # Make sure this matches your profile name
            ),
            SearchField(name="filepath", type="Edm.String", filterable=True, sortable=True, facetable=True),
            SearchField(name="language", type="Edm.String", filterable=True, sortable=True, facetable=True),
        ],
        vector_search=VectorSearch(
            profiles=[VectorSearchProfile(name="hnsw_profile", algorithm_configuration_name="alg", vectorizer_name="azure_openai_text_3_large")],
            algorithms=[HnswAlgorithmConfiguration(name="alg")],
            vectorizers=[
                AzureOpenAIVectorizer(
                    vectorizer_name="azure_openai_text_3_large",
                    parameters=AzureOpenAIVectorizerParameters(
                        resource_url=azure_openai_endpoint,
                        deployment_name=azure_openai_embedding_deployment,
                        model_name=azure_openai_embedding_model
                    )
                )
            ]
        ),
        semantic_search=SemanticSearch(
            default_configuration_name="code_semantic_config",
            configurations=[
                SemanticConfiguration(
                    name="code_semantic_config",
                    prioritized_fields=SemanticPrioritizedFields(
                         # Make filepath act as the "Title" of the chunk
                        title_field=SemanticField(field_name="filepath"), 
                        # Look at the actual code
                        content_fields=[SemanticField(field_name="content")],
                        # Use language as a keyword to boost relevance
                        keywords_fields=[SemanticField(field_name="language")]
                    )
                )
            ]
        )
    )

    if not endpoint:
        raise ValueError("Azure Search endpoint is not configured. Please set the AZURE_SEARCH_ENDPOINT environment variable.")

    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    index_client.create_or_update_index(index)
    return index_client
