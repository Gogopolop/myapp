import reflex as rx

from myapp.components.app.sourcecraft_logo import sourcecraft_logo

CAPTION = "Всё начинается с кода."


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            sourcecraft_logo(
                "flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#faf9f6]",
                "font-bold tracking-[-0.04em] text-[#17161C] text-xs",
            ),
            rx.el.p(CAPTION),
            class_name="mx-auto flex w-full max-w-[1280px] flex-col items-center justify-between gap-3 px-5 py-7 text-xs text-[#8D8981] sm:flex-row sm:px-10",
        ),
        class_name="mt-auto border-t border-[#E3DFD5] bg-[#faf9f6]",
    )
