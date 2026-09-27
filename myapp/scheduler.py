import asyncio
import logging

from myapp.api.sourcecraft_client import fetch_repository_snapshot, SourceCraftError
from analytics.transform import to_analyzer_input
from analytics.analyzer import analyze_repo
from db.repository_store import get_repos_due_for_recheck, mark_repo_checked, save_analysis

logger = logging.getLogger("recheck_scheduler")

CHECK_INTERVAL_SECONDS = 60 * 60 * 6  # раз в 6 часов проверяем, не пора ли кому-то на перепроверку


async def _recheck_repo(repo_url: str, pat: str, repo_id: int) -> None:
    try:
        data = await fetch_repository_snapshot(repo_url, pat)
        analyzer_input = to_analyzer_input(data, pat=pat)
        result = analyze_repo(analyzer_input)
        save_analysis(result)
    except SourceCraftError as exc:
        logger.warning("Не удалось перепроверить %s: %s", repo_url, exc)
    except Exception:
        logger.exception("Ошибка при перепроверке %s", repo_url)
    finally:
        # last_checked_at двигаем в любом случае — иначе упавший репозиторий
        # будет пытаться перепроверяться на каждом цикле, а не раз в неделю
        mark_repo_checked(repo_id)


async def recheck_loop():
    while True:
        due = get_repos_due_for_recheck(days=7)
        for item in due:
            await _recheck_repo(item["repo_url"], item["pat"], item["id"])
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)