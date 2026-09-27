import reflex as rx


def corner_graphics() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="absolute top-20 -left-16 h-40 w-60 -rotate-[28deg] bg-[#efb1a0] [clip-path:polygon(0_0,100%_0,100%_48%,40%_48%,40%_100%,0_100%)]"
            ),
            rx.el.div(
                class_name="absolute left-9 top-10 h-52 w-40 rotate-[25deg] border border-[#807e75]"
            ),
            rx.el.div(
                class_name="absolute left-14 top-48 h-2.5 w-2.5 rounded-full border border-[#696960] bg-[#faf9f6]"
            ),
            rx.el.div(
                class_name="absolute -left-20 top-72 h-24 w-64 rotate-[32deg] bg-[#dfbd55]"
            ),
            rx.el.div(
                class_name="absolute left-0 top-96 h-px w-64 -rotate-[28deg] bg-[#77776e]"
            ),
            rx.el.div(
                class_name="absolute left-48 top-[340px] h-2 w-2 rounded-full bg-[#fa6035]"
            ),
            class_name="absolute -left-10 top-8 h-[480px] w-64 lg:left-0",
        ),
        rx.el.div(
            rx.el.div(
                class_name="absolute -right-20 top-10 h-48 w-64 rotate-[28deg] bg-[#bac8d0] [clip-path:polygon(0_0,100%_0,100%_100%,55%_100%,55%_45%,0_45%)]"
            ),
            rx.el.div(
                class_name="absolute -right-4 top-44 h-40 w-52 -rotate-[30deg] border border-[#838278]"
            ),
            rx.el.div(
                class_name="absolute right-36 top-60 h-3 w-3 rounded-full border border-[#77776e] bg-[#faf9f6]"
            ),
            rx.el.div(
                class_name="absolute -right-20 top-80 h-24 w-72 -rotate-[30deg] bg-[#efb1a0]"
            ),
            rx.el.div(
                class_name="absolute -right-10 top-96 h-px w-64 rotate-[28deg] bg-[#77776e]"
            ),
            class_name="absolute -right-10 top-0 h-[490px] w-64 lg:right-0",
        ),
        aria_hidden=True,
        class_name="pointer-events-none absolute inset-0 hidden overflow-hidden md:block",
    )


def flower() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                [
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] -translate-y-8",
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] rotate-60 -translate-y-4 translate-x-7",
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] rotate-120 translate-y-4 translate-x-7",
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] translate-y-8",
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] -rotate-120 translate-y-4 -translate-x-7",
                    "absolute h-20 w-9 rounded-[50%] border border-[#77786d] -rotate-60 -translate-y-4 -translate-x-7",
                ],
                lambda classes: rx.el.div(class_name=classes),
            ),
            rx.el.div(
                class_name="z-10 h-7 w-7 rounded-full border border-[#77786d] bg-[#ecc768]"
            ),
            class_name="absolute left-16 top-12 flex h-16 w-16 items-center justify-center",
        ),
        rx.el.div(
            class_name="absolute left-24 top-28 h-28 w-10 rounded-bl-[100%] border-l border-[#77786d]"
        ),
        rx.el.div(
            class_name="absolute left-[99px] top-36 h-10 w-14 -rotate-12 rounded-tr-[100%] rounded-bl-[100%] border border-[#77786d]"
        ),
        rx.el.div(
            class_name="absolute left-12 top-40 h-9 w-12 rotate-12 rounded-tl-[100%] rounded-br-[100%] border border-[#77786d]"
        ),
        aria_hidden=True,
        class_name="relative h-60 w-48 -rotate-12",
    )


def mini_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="h-10 w-9 rounded-t-sm border border-[#a39979] bg-[#e9dba8]"
        ),
        rx.el.div(
            class_name="h-20 w-9 rounded-t-sm border border-[#aa8175] bg-[#edbaa9]"
        ),
        rx.el.div(
            class_name="h-32 w-9 rounded-t-sm border border-[#819298] bg-[#becbd0]"
        ),
        aria_hidden=True,
        class_name="flex h-40 w-44 items-end justify-center gap-3 border-b border-[#8b897f] pb-0",
    )
