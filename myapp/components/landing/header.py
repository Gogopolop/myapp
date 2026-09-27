import reflex as rx
from myapp.data.content import BRAND, PRODUCT, UI, LINKS



def brand() -> rx.Component:
    return rx.el.a(
        rx.el.span(
            rx.icon("asterisk", class_name="h-7 w-7 stroke-[2.5]"),
            class_name="flex h-10 w-10 items-center justify-center rounded-full bg-[#fa6035] text-[#fffaf5]",
        ),
        rx.el.span(BRAND, class_name="text-xl font-semibold tracking-[-0.8px]"),
        href=LINKS["home"],
        class_name="inline-flex items-center gap-2.5 text-[#252522] rounded-md focus-visible:outline-2 focus-visible:outline-orange-500",
    )


def login_link() -> rx.Component:
    return rx.el.a(
        UI["login"],
        href="http://localhost:8000/auth/yandex/login",  # явный порт
        rel="noopener noreferrer",
        title=UI["login_hint"],
        class_name="inline-flex items-center justify-center rounded-lg bg-[#242422] px-7 py-3 text-sm font-medium text-white transition-colors hover:bg-[#fa6035] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-orange-500",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.a(
            UI["skip"],
            href=LINKS["health"],
            class_name="sr-only focus:not-sr-only focus:absolute focus:top-3 bg-white text-black",
        ),
        rx.el.nav(
            brand(),
            rx.el.a(
                PRODUCT,
                href=LINKS["health"],
                class_name="mr-auto border-l border-[#d9d7d1] pl-5 text-sm text-[#66645e] hover:text-[#ed572f] hidden sm:block",
            ),
            login_link(),
            class_name="mx-auto flex max-w-[1280px] items-center gap-6 px-5 py-6 md:px-12",
        ),
        class_name="relative z-20 w-full bg-[#faf9f6]",
    )
