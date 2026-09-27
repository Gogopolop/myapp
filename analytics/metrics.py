import io
import re
import zipfile

import httpx


def calc_activity(data: dict) -> float | None:
    """Активность: ветки, контрибьюторы, релизы, MR."""
    branches = data.get("branches", [])
    contributors = data.get("contributors", [])
    releases = data.get("releases", [])
    pulls = data.get("pull_requests", [])

    if not (branches or contributors or releases or pulls):
        return None

    score = 0
    score += min(30, len(branches) * 5)
    score += min(30, len(contributors) * 10)
    score += min(20, len(releases) * 5)
    score += min(20, len(pulls) * 2)

    return round(min(100.0, score), 2)


def calc_documentation(files: list) -> float | None:
    if not files:
        return None

    names = [f.lower() for f in files]
    score = 0
    if any(n.startswith("readme") for n in names):
        score += 40
    if any(n == "license" or n.startswith("license.") for n in names):
        score += 30
    if any("contributing" in n for n in names):
        score += 15
    if any(n in ("docs", "documentation") for n in names):
        score += 15

    return round(float(score), 2)


def calc_ci(ci_runs: list) -> float | None:
    if not ci_runs:
        return None
    total = len(ci_runs)
    success = sum(1 for run in ci_runs if run.get("status") == "success")
    return round((success / total) * 100, 2)


def calc_security(appsec_findings: list) -> float | None:
    if not appsec_findings:
        return 100.0
    weights = {"critical": 40, "high": 20, "medium": 10, "low": 5}
    penalty = sum(
        weights.get(f.get("severity", "low"), 5)
        for f in appsec_findings
        if f.get("status") == "open"
    )
    return round(max(0.0, 100.0 - penalty), 2)


def calc_issues(issues: list) -> float | None:
    if not issues:
        return None
    total = len(issues)
    closed = sum(1 for i in issues if i.get("state") == "closed")
    return round((closed / total) * 100, 2)


def calc_code_health_from_zip(
    org_slug: str,
    repo_slug: str,
    branch: str,
    pat: str,
) -> float | None:
    """Скачивает ZIP репозитория, считает TODO/FIXME, возвращает 0-100."""
    if not org_slug or not repo_slug or not branch or not pat:
        return None

    url = (
        f"https://codeload.sourcecraft.tech/{org_slug}/{repo_slug}"
        f"/zipball/refs/heads/{branch}"
    )

    try:
        r = httpx.get(
            url,
            headers={"Authorization": f"Bearer {pat}"},
            timeout=60.0,
        )
        if r.status_code != 200:
            return None

        z = zipfile.ZipFile(io.BytesIO(r.content))

        code_ext = (
            ".py", ".js", ".ts", ".tsx", ".jsx",
            ".java", ".go", ".rs", ".rb", ".php",
            ".c", ".cpp", ".h", ".cs", ".kt", ".swift",
        )

        todo_count = 0
        files_checked = 0

        for name in z.namelist():
            if not name.endswith(code_ext):
                continue
            if "/node_modules/" in name or "/.venv/" in name:
                continue
            try:
                content = z.read(name).decode("utf-8", errors="ignore")
                todo_count += len(
                    re.findall(r"\b(TODO|FIXME|XXX|HACK)\b", content, re.IGNORECASE)
                )
                files_checked += 1
            except Exception:
                continue

        z.close()

        if files_checked == 0:
            return None

        score = max(0.0, 100.0 - (todo_count * 2))
        return round(score, 2)

    except Exception:
        return None