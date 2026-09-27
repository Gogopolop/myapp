import json

from .database import get_connection, init_db
from .crypto import encrypt, decrypt

init_db()


def save_analysis(analysis: dict, user_id: int | None = None) -> int:
    """Сохраняет результат анализа в таблицу analyses. Возвращает id записи."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO analyses (repo, score, categories, recommendations, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                analysis.get("repo", "unknown"),
                analysis.get("score"),
                json.dumps(analysis.get("categories", {}), ensure_ascii=False),
                json.dumps(analysis.get("recommendations", []), ensure_ascii=False),
                user_id,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_top_repositories(limit: int = 10) -> list[dict]:
    """Топ-N уникальных репозиториев по лучшему из посчитанных score."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT repo, score, created_at
            FROM analyses a
            WHERE score IS NOT NULL
              AND score = (
                  SELECT MAX(score) FROM analyses b WHERE b.repo = a.repo
              )
            GROUP BY repo
            ORDER BY score DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]


def get_analysis_by_repo(repo: str) -> dict | None:
    """Лучший (по score) сохранённый анализ для конкретного репозитория."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT repo, score, categories, recommendations
            FROM analyses
            WHERE repo = ?
            ORDER BY score DESC, created_at DESC
            LIMIT 1
            """,
            (repo,),
        ).fetchone()
        if not row:
            return None
        return {
            "repo": row["repo"],
            "score": row["score"],
            "categories": json.loads(row["categories"] or "{}"),
            "recommendations": json.loads(row["recommendations"] or "[]"),
        }


def track_repo(repo_url: str, pat: str) -> None:
    """Регистрирует репозиторий на еженедельную перепроверку (или обновляет PAT)."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO tracked_repos (repo_url, pat_encrypted, last_checked_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(repo_url) DO UPDATE SET pat_encrypted = excluded.pat_encrypted
            """,
            (repo_url, encrypt(pat)),
        )
        conn.commit()


def get_repos_due_for_recheck(days: int = 7) -> list[dict]:
    """Репозитории, которые ни разу не проверялись или проверялись >= days дней назад."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, repo_url, pat_encrypted
            FROM tracked_repos
            WHERE last_checked_at IS NULL
               OR datetime(last_checked_at) <= datetime('now', ?)
            """,
            (f"-{days} days",),
        ).fetchall()
        return [
            {"id": r["id"], "repo_url": r["repo_url"], "pat": decrypt(r["pat_encrypted"])}
            for r in rows
        ]


def mark_repo_checked(repo_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE tracked_repos SET last_checked_at = CURRENT_TIMESTAMP WHERE id = ?",
            (repo_id,),
        )
        conn.commit()