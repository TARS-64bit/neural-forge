def get_dynamic_index_name(owner: str, repo: str, branch: str) -> str:
    safe_owner = "".join(e for e in owner if e.isalnum()).lower()
    safe_repo = "".join(e for e in repo if e.isalnum()).lower()
    safe_branch = "".join(e for e in branch if e.isalnum()).lower()
    return f"idx-{safe_owner}-{safe_repo}-{safe_branch}"
