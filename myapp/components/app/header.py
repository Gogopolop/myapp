import reflex as rx
from ...state.auth_state import AuthState

from myapp.components.app.sourcecraft_logo import sourcecraft_logo

PRODUCT = "RepoPuls"
LOGOUT = "Выйти"


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                sourcecraft_logo(
                    "flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#FF5F3D]",
                    "font-bold tracking-[-0.04em] text-[#17161C] text-lg sm:text-xl",
                ),
                rx.el.span(class_name="mx-1 h-5 w-px bg-[#DCD8CE] sm:mx-3"),
                rx.el.span(
                    PRODUCT, class_name="text-base font-medium sm:text-lg"
                ),
                class_name="flex items-center gap-2 text-[#17161C]",
            ),
            rx.el.button(
                LOGOUT,
                rx.icon("log-out", class_name="h-4 w-4"),
                type="button",
                on_click=AuthState.logout,
                class_name="flex items-center gap-2 rounded-full border border-[#DCD8CE] bg-transparent px-4 py-2.5 text-sm font-medium text-[#17161C] transition-colors hover:border-[#17161C] hover:bg-[#faf9f6] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#F06B45]",
            ),
            class_name="mx-auto flex min-h-24 w-full max-w-[1280px] items-center justify-between gap-3 px-5 sm:px-10",
        ),
        class_name="shrink-0 border-b border-[#E3DFD5] bg-[#faf9f6]",
    )
