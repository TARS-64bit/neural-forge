import os

def is_mock_mode() -> bool:
    """Returns True if the app should use mock data instead of real LLM calls."""
    return os.getenv("USE_MOCK_PLAN", "false").lower() == "true"