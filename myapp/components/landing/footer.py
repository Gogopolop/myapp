import reflex as rx
from myapp.data.content import UI, LINKS
from myapp.components.landing.header import brand


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    UI["footer"],
                    class_name="text-xl font-medium tracking-[-0.5px] text-[#45453b]",
                ),
                rx.el.p(
                    UI["footer_sub"], class_name="mt-1 text-sm text-[#938c7e]"
                ),
            ),
            rx.el.a(
                UI["back"],
                rx.icon("arrow-up", class_name="h-4 w-4"),
                href=LINKS["home"],
                class_name="inline-flex items-center gap-3 text-sm text-[#777164] hover:text-[#ee6038]",
            ),
            class_name="flex items-center justify-between gap-6 border-b border-[#e3dfd5] pb-8",
        ),
        rx.el.div(
            brand(),
            rx.el.p(UI["footer_note"], class_name="text-[11px] text-[#9b9486]"),
            class_name="flex flex-wrap items-center justify-between gap-5 pt-7",
        ),
        class_name="mx-auto max-w-[1160px] border-t border-[#e2dfd5] px-5 py-10 md:px-12",
    )
