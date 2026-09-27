import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("YANDEX_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET", "")
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-insecure-secret-change-me")

REDIRECT_URI = "http://localhost:8000/auth/yandex/callback"
FRONTEND_URL = "http://localhost:3000/app"

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        "YANDEX_CLIENT_ID / YANDEX_CLIENT_SECRET не заданы. "
        "Проверь файл .env в корне проекта."
    )