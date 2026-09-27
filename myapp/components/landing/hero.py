import reflex as rx
from myapp.data.content import UI, LINKS
from myapp.components.landing.header import login_link
from myapp.components.landing.decorative_graphics import corner_graphics


def hero() -> rx.Component:
    return rx.el.section(
        corner_graphics(),
        rx.el.div(
            rx.el.p(
                UI["eyebrow"],
                class_name="mb-7 text-[10px] sm:text-xs font-medium tracking-[0.19em] text-[#858176]",
            ),
            rx.el.h1(
                rx.el.span(UI["hero_title"], class_name="block"),
                rx.el.span(
                    UI["hero_accent"], class_name="block text-[#f2613c]"
                ),
                class_name="text-[46px] leading-[1.07] tracking-[-2.5px] sm:text-6xl lg:text-[80px] lg:tracking-[-4.5px] font-medium text-[#272722]",
            ),
            rx.el.p(
                UI["hero_description"],
                class_name="mt-7 whitespace-pre-line text-base leading-7 text-[#737068] md:text-lg md:leading-8",
            ),
            rx.el.div(
                login_link(),
                rx.el.a(
                    UI["preview"],
                    rx.icon("arrow-down-right", class_name="h-4 w-4"),
                    href=LINKS["health"],
                    class_name="inline-flex items-center justify-center gap-4 rounded-lg border border-[#ccc9bf] px-6 py-3 text-sm font-medium text-[#302f29] transition-colors hover:bg-[#eeece5] focus-visible:outline-orange-500",
                ),
                class_name="mt-8 flex flex-wrap justify-center gap-3",
            ),
            rx.el.p(UI["hero_note"], class_name="mt-5 text-xs text-[#969184]"),
            class_name="relative z-10 mx-auto max-w-[760px] px-5 pt-14 text-center md:pt-20",
        ),
        rx.el.a(
            rx.el.span(UI["scroll"]),
            rx.icon("arrow-down", class_name="h-4 w-4"),
            href=LINKS["health"],
            class_name="relative z-10 mx-auto mt-16 mb-10 flex w-fit flex-col items-center gap-3 text-xs text-[#858074] hover:text-[#f2613c]",
        ),
        class_name="relative overflow-hidden pb-5 md:pb-9",
    )
