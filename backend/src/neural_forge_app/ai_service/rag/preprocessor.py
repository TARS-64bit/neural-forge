import os
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from neural_forge_app.ai_service.rag.models import CodeChunk

def preprocess_codebase(repo_path: str):
    """
    Reads a cloned repo, filters noise, chunks by syntax, and enriches metadata.
    Returns a list of dictionaries ready for Azure AI Search.
    """
    processed_documents : list[CodeChunk] = []
    
    # 1. Define Language Mapping for the Splitter
    EXTENSION_MAPPING = {
        '.py': Language.PYTHON,
        '.js': Language.JS,
        '.jsx': Language.JS, 
        '.ts': Language.TS,
        '.tsx': Language.TS,
        '.go': Language.GO,
        '.java': Language.JAVA,
        '.cpp': Language.CPP,
        '.md': Language.MARKDOWN,
    }

    # 2. Aggressive Filtering
    IGNORE_DIRS = {'.git', 'node_modules', 'venv', 'dist', '__pycache__', 'build', '.idea', '.next', 'next-env.d.ts'}
    IGNORE_FILES = {'package-lock.json', 'yarn.lock'}

    chunk_id = 0

    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file in IGNORE_FILES:
                continue

            ext = os.path.splitext(file)[1].lower()
            if ext not in EXTENSION_MAPPING:
                continue # Skip unsupported files (images, binaries, etc.)

            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, repo_path) # e.g., "src/main.py"

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 3. Syntax-Aware Chunking
                # This ensures we don't break code in the middle of a function
                splitter = RecursiveCharacterTextSplitter.from_language(
                    language=EXTENSION_MAPPING[ext],
                    chunk_size=1500,  # Tokens/Characters per chunk
                    chunk_overlap=150   # Overlap to keep context between chunks
                )
                
                chunks = splitter.split_text(content)

                # 4. Metadata Enrichment
                for chunk in chunks:
                    # Inject context directly into the text for the LLM to read
                    enriched_text = (
                        f"// FILEPATH: {relative_path}\n"
                        f"// LANGUAGE: {ext}\n"
                        f"// REPO_ROOT: {repo_path}\n"
                        f"---\n"
                        f"{chunk}"
                    )

                    validated_chunk: CodeChunk = {
                        "id": str(chunk_id),
                        "filepath": relative_path,
                        "language": ext,
                        "content": enriched_text,
                        "embedding": None
                    }

                    processed_documents.append(validated_chunk)

                    chunk_id += 1

            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

    return processed_documents