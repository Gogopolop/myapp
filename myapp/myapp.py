import reflex as rx
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .state.rating_state import RatingState
from .pages.rating import rating_page
import asyncio
from .scheduler import recheck_loop

from .auth.yandex_auth import router as yandex_auth_router
from .auth.config import SESSION_SECRET
from .data.content import PAGE_TITLE
from .pages.login import index_page
from .pages.home import home_page
from .pages.dashboard import dashboard_page


# === FastAPI для OAuth-роутов ===
fastapi_app = FastAPI(title="Auth API")
fastapi_app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
fastapi_app.include_router(yandex_auth_router)


# === Единственное приложение Reflex ===
app = rx.App(
    api_transformer=fastapi_app,
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    rating_page,
    route="/rating",
    title="Рейтинг репозиториев",
    on_load=RatingState.load_top_repos,
)

app.add_page(index_page, route="/", title=PAGE_TITLE)
app.add_page(home_page, route="/app", title="SourceCraft RepoPuls")
app.add_page(dashboard_page, route="/dashboard", title="Dashboard")
@fastapi_app.on_event("startup")
async def _start_recheck_scheduler():
    asyncio.create_task(recheck_loop())