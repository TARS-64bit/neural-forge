import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.core.tools import parse_resource_id

load_dotenv(override=True)

def is_mock_mode() -> bool:
    """Returns True if the app should use mock data instead of real LLM calls."""
    return os.getenv("USE_MOCK_PLAN", "false").lower() == "true"

# Environment configuration
project_endpoint = os.environ.get("PROJECT_ENDPOINT")
project_resource_id = os.environ.get("PROJECT_RESOURCE_ID")
agent_model = os.getenv("AGENT_MODEL", "gpt-4.1-mini")
endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openai_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
azure_openai_embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

knowledge_source_name = os.getenv("AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME")
project_connection_name = os.getenv("PROJECT_CONNECTION_NAME")
index_name = os.getenv("AZURE_SEARCH_INDEX")
base_name = os.getenv("AZURE_SEARCH_KNOWLEDGE_BASE_NAME")

# Azure clients / credentials
credential = DefaultAzureCredential()

# Parse the resource ID to extract subscription and other components (if provided)
parsed_resource_id = None
subscription_id = resource_group = account_name = project_name = None
if project_resource_id:
    try:
        parsed_resource_id = parse_resource_id(project_resource_id)
        subscription_id = parsed_resource_id.get('subscription')
        resource_group = parsed_resource_id.get('resource_group')
        account_name = parsed_resource_id.get('name')
        project_name = parsed_resource_id.get('child_name_1')
    except Exception:
        parsed_resource_id = None
