import reflex as rx
from ..components.app.header import header
from ..components.app.tutorial import tutorial
from ..components.app.repository_form import repository_form
from ..components.app.footer import footer
from ..state.auth_state import AuthState


class HomeState(rx.State):
    @rx.event
    def load_user(self):
        params = self.router.page.params
        if params.get("uid"):
            auth = self.get_state(AuthState)
            auth.set_user(
                user_id=params.get("uid", ""),
                name=params.get("name", ""),
                email=params.get("email", ""),
            )


def home_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            tutorial(),
            repository_form(),
            class_name="mx-auto w-full max-w-[1000px] flex-1 px-5 pt-10 sm:px-10 sm:pt-14",
        ),
        footer(),
        rx.script(
            "document.documentElement.classList.add('scroll-smooth', 'motion-reduce:scroll-auto');"
        ),
        class_name="flex min-h-dvh flex-col bg-[#faf9f6] font-['Inter',Arial,sans-serif] text-[#17161C] selection:bg-[#F06B45]/20",
    )