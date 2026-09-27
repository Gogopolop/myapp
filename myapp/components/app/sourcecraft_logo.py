import reflex as rx


def sourcecraft_logo(icon_class: str, wordmark_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("asterisk", class_name="h-3/5 w-3/5 stroke-[3] text-white"),
            class_name=icon_class,
        ),
        rx.el.span(
            "SourceCraft",
            class_name=wordmark_class,
        ),
        class_name="flex items-center gap-2",
    )
