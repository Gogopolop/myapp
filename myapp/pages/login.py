import reflex as rx
from myapp.components.landing.header import header
from myapp.components.landing.hero import hero
from myapp.components.landing.health_section import health_section
from myapp.components.landing.footer import footer


def index_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(hero(), health_section()),
        footer(),
        id="top",
        lang="ru",
        class_name="h-dvh w-full overflow-y-auto overflow-x-hidden scroll-smooth motion-reduce:scroll-auto bg-[#faf9f6] text-[#272722] font-['Inter',Arial,sans-serif] selection:bg-[#f8cbb8]",
    )
