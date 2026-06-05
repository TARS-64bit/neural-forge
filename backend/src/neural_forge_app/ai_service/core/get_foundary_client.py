
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import os
from dotenv import load_dotenv
load_dotenv()

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL = os.getenv("AGENT_MODEL", "gpt-4.1-mini")

def get_foundary_client():
    return FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        model=MODEL,
        credential=AzureCliCredential(),
    )