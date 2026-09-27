"""Асинхронный клиент публичного REST API SourceCraft."""
from __future__ import annotations

import asyncio
from urllib.parse import urlparse

import httpx

API_BASE = "https://api.sourcecraft.tech"


class SourceCraftError(Exception):
    """Ошибка запроса к SourceCraft."""


def parse_repo_url(url: str) -> tuple[str, str]:
    """Достаёт (org_slug, repo_slug) из ссылки."""
    url = url.strip()
    if not url:
        raise SourceCraftError("Ссылка на репозиторий не указана")

    path = urlparse(url).path if "://" in url else url
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        raise SourceCraftError("Не удалось распознать организацию и репозиторий")
    return parts[0], parts[1]


async def _get(client: httpx.AsyncClient, path: str, pat: str):
    resp = await client.get(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {pat}"},
    )
    if resp.status_code == 401:
        raise SourceCraftError("Неверный или истёкший PAT-токен")
    if resp.status_code == 404:
        raise SourceCraftError("Репозиторий не найден")
    if resp.is_error:
        raise SourceCraftError(f"Ошибка SourceCraft API ({resp.status_code})")
    return resp.json()


async def _get_with_retry(client, path, pat, retries=3, params=None):
    """Запрос с 3 попытками только для временных ошибок."""
    last_error = None
    for attempt in range(retries):
        try:
            resp = await client.get(
                f"{API_BASE}{path}",
                headers={"Authorization": f"Bearer {pat}"},
                params=params,
                timeout=30.0,
            )
            if resp.status_code == 401:
                raise SourceCraftError("Неверный или истёкший PAT-токен")
            if resp.status_code == 403:
                raise SourceCraftError("Нет доступа к репозиторию (403). Проверьте права токена.")
            if resp.status_code == 404:
                raise SourceCraftError("Репозиторий не найден (404)")
            if resp.status_code == 429:
                last_error = SourceCraftError("Rate limit (429)")
                await asyncio.sleep(5)
                continue
            if resp.status_code >= 500:
                last_error = SourceCraftError(f"Ошибка сервера ({resp.status_code})")
                await asyncio.sleep(2)
                continue
            if resp.is_error:
                raise SourceCraftError(f"Ошибка API ({resp.status_code})")
            return resp.json()
        except SourceCraftError:
            raise
        except Exception as e:
            last_error = e
            await asyncio.sleep(0.5)
    raise last_error or SourceCraftError("Не удалось получить данные")


async def fetch_repository_snapshot(repo_url: str, pat: str) -> dict:
    org_slug, repo_slug = parse_repo_url(repo_url)
    base = f"/repos/{org_slug}/{repo_slug}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Сначала — главное (репозиторий и CI)
        repo = await _get_with_retry(client, base, pat)
        runs_resp = await _get_with_retry(client, f"{base}/cicd/runs", pat)

        # Потом — остальное параллельно
        results = await asyncio.gather(
            _get_with_retry(client, f"{base}/trees", pat),
            _get_with_retry(client, f"{base}/branches", pat),
            _get_with_retry(client, f"{base}/contributors", pat),
            _get_with_retry(client, f"{base}/issues", pat),
            _get_with_retry(client, f"{base}/releases", pat),
            _get_with_retry(client, f"{base}/pulls", pat),
            return_exceptions=True,
        )

    tree, branches, contributors, issues_resp, releases_resp, pulls_resp = results

    def _or_empty(v, default):
        return default if isinstance(v, Exception) else v

    issues_resp = _or_empty(issues_resp, {})
    releases_resp = _or_empty(releases_resp, {})
    pulls_resp = _or_empty(pulls_resp, {})

    return {
        "repository": repo,
        "tree": _or_empty(tree, []),
        "branches": _or_empty(branches, []),
        "contributors": _or_empty(contributors, []),
        "issues": issues_resp.get("issues", []) if isinstance(issues_resp, dict) else [],
        "ci_runs": runs_resp.get("runs", []) if isinstance(runs_resp, dict) else [],
        "releases": releases_resp.get("releases", []) if isinstance(releases_resp, dict) else [],
        "pull_requests": pulls_resp.get("pull_requests", []) if isinstance(pulls_resp, dict) else [],
    }