from db.database import get_connection, init_db

init_db()


def save_user(yandex_uid: str, name: str = "", email: str = "") -> int:
    """Создаёт пользователя, если его ещё нет, иначе обновляет имя/email. Возвращает id."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (yandex_uid, name, email)
            VALUES (?, ?, ?)
            ON CONFLICT(yandex_uid) DO UPDATE SET name=excluded.name, email=excluded.email
            """,
            (yandex_uid, name, email),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id FROM users WHERE yandex_uid = ?", (yandex_uid,)
        ).fetchone()
        return row["id"]

