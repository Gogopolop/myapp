from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from yandexid import YandexOAuth, YandexID
from urllib.parse import urlencode
import secrets

from db.user_store import save_user
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, FRONTEND_URL

router = APIRouter(prefix="/auth/yandex", tags=["Yandex OAuth"])


def _make_oauth() -> YandexOAuth:
    return YandexOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )


@router.get("/login")
async def yandex_login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    params = urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "login:email login:info",
        "state": state,
    })
    return RedirectResponse(url=f"https://oauth.yandex.ru/authorize?{params}")


@router.get("/callback")
async def yandex_callback(request: Request, code: str, state: str):
    expected_state = request.session.pop("oauth_state", None)
    if not expected_state or state != expected_state:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=invalid_state")

    try:
        oauth = _make_oauth()
        token = oauth.get_token_from_code(code)
        user_info = YandexID(token.access_token).get_user_info_json()
    except Exception as exc:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=oauth_failed&detail={exc}")

    name = user_info.real_name or user_info.display_name or ""
    email = user_info.default_email or ""
    save_user(str(user_info.id), name, email)

    params = urlencode({
        "uid": user_info.id,
        "name": name,
        "email": email,
    })
    return RedirectResponse(url=f"{FRONTEND_URL}?{params}")