import reflex as rx
from myapp.data.content import UI
from myapp.data.content import UI, REPOSITORIES
from myapp.components.landing.decorative_graphics import flower, mini_chart
from myapp.components.landing.repo_card import repository_example


def health_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                flower(), class_name="absolute -left-12 -top-8 hidden lg:block"
            ),
            rx.el.div(
                mini_chart(),
                class_name="absolute -right-2 top-3 hidden lg:block",
            ),
            rx.el.p(
                UI["section_number"],
                class_name="text-[10px] font-medium tracking-[0.16em] text-[#a19785]",
            ),
            rx.el.h2(
                UI["section_title"],
                class_name="mx-auto mt-5 max-w-[620px] text-3xl font-medium leading-tight tracking-[-1.1px] text-[#33352d] md:text-[42px]",
            ),
            rx.el.p(
                UI["section_description"],
                class_name="mx-auto mt-5 max-w-[580px] whitespace-pre-line text-sm leading-7 text-[#8d8576]",
            ),
            rx.el.p(UI["demo"], class_name="mt-4 text-[10px] text-[#a09786]"),
            class_name="relative mb-14 text-center md:mb-20",
        ),
        rx.el.div(
            rx.foreach(REPOSITORIES, repository_example),
            class_name="flex flex-col gap-16 md:gap-24",
        ),
        id="health",
        class_name="mx-auto w-full max-w-[1160px] scroll-mt-8 border-t border-[#e2dfd5] px-5 pt-14 pb-20 md:px-12 md:pt-20 md:pb-28",
    )
