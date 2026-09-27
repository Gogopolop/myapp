import asyncio #проверка функции обновления репозиторев
from myapp.scheduler import _recheck_repo
from db.repository_store import get_repos_due_for_recheck

async def main():
    due = get_repos_due_for_recheck(days=0)  # days=0 — берём вообще все, игнорируя срок
    print(f"Найдено репозиториев для перепроверки: {len(due)}")
    for item in due:
        print(f"Перепроверяю {item['repo_url']}...")
        await _recheck_repo(item["repo_url"], item["pat"], item["id"])
        print("Готово")

asyncio.run(main())