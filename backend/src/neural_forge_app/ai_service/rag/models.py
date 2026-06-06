from typing import TypedDict, List, Optional

class CodeChunk(TypedDict):
    id: str
    filepath: str
    language: str
    content: str
    embedding: Optional[List[float]]