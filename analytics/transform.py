"""Переходник: сырые данные SourceCraft API → формат для analyzer.py."""
from analytics.metrics import calc_code_health_from_zip


def to_analyzer_input(raw: dict, pat: str = "") -> dict:
    repo = raw.get("repository", {}) or {}
    org = (repo.get("organization") or {}).get("slug", "")
    repo_slug = repo.get("slug", "")
    branch = repo.get("default_branch", "main")

    # Считаем code_health через ZIP
    code_health = None
    if org and repo_slug and branch and pat:
        code_health = calc_code_health_from_zip(org, repo_slug, branch, pat)

    return {
        "repo": repo_slug,
        "branches": raw.get("branches", []),
        "contributors": raw.get("contributors", []),
        "releases": raw.get("releases", []),
        "files": _flatten_file_names(raw.get("tree", [])),
        "ci_runs": [_normalize_ci(run) for run in raw.get("ci_runs", [])],
        "appsec_findings": [],
        "issues": [_normalize_issue(i) for i in raw.get("issues", [])],
        "pull_requests": raw.get("pull_requests", []),
        "likes": (repo.get("rating") or {}).get("value", 0),
        "language": (repo.get("language") or {}).get("name", ""),
        "code_health_score": code_health,   # готовое значение
    }


def _normalize_ci(run: dict) -> dict:
    status = run.get("status", "")
    return {**run, "status": "success" if status == "success" else "failed"}


def _normalize_issue(issue: dict) -> dict:
    status_type = (issue.get("status") or {}).get("status_type")
    state = "closed" if status_type in ("completed", "cancelled") else "open"
    return {**issue, "state": state}


def _flatten_file_names(tree) -> list[str]:
    if isinstance(tree, list):
        entries = tree
    elif isinstance(tree, dict):
        entries = tree.get("trees") or tree.get("entries") or []
    else:
        entries = []

    names = []
    for entry in entries:
        if isinstance(entry, dict):
            name = entry.get("name") or entry.get("path")
            if name:
                names.append(name)
    return names