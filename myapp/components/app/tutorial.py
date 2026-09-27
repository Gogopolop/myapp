import reflex as rx

EYEBROW = "ЗНАКОМСТВО С REPOPULS"
TITLE = "Начните с короткого знакомства"
DESCRIPTION = "Посмотрите, как анализировать репозиторий и читать результаты."
VIDEO_PATH = ("/Guide2009.mp4")
VIDEO_LABEL = "Обучающее видео: работа с SourceCraft RepoPuls"
VIDEO_FALLBACK = "Ваш браузер не поддерживает HTML5-видео."
DOWNLOAD_LABEL = "Открыть обучающее видео"


def tutorial() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon("circle-play", class_name="h-4 w-4 text-[#F06B45]"),
                rx.el.p(
                    EYEBROW,
                    class_name="text-[11px] font-semibold tracking-[0.16em] text-[#77736B]",
                ),
                class_name="mb-4 flex items-center justify-center gap-2",
            ),
            rx.el.h1(
                TITLE,
                id="tutorial-title",
                class_name="text-[27px] font-semibold leading-tight tracking-[-0.035em] text-[#17161C] sm:text-[36px]",
            ),
            rx.el.p(
                DESCRIPTION,
                class_name="mt-3 text-sm leading-relaxed text-[#77736B] sm:text-base",
            ),
            class_name="mb-8 text-center sm:mb-10",
        ),
        rx.el.div(
            rx.el.video(
                rx.el.source(src=VIDEO_PATH, type="video/mp4"),
                VIDEO_FALLBACK,
                rx.el.a(DOWNLOAD_LABEL, href=VIDEO_PATH),
                controls=True,
                preload="metadata",
                plays_inline=True,
                aria_label=VIDEO_LABEL,
                class_name="aspect-video h-auto w-full rounded-[20px] bg-[#17161C] object-contain focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#F06B45] sm:rounded-[28px]",
            ),
            class_name="overflow-hidden rounded-[22px] border border-[#29282D] bg-[#17161C] p-2 sm:rounded-[32px] sm:p-3",
        ),
        aria_labelledby="tutorial-title",
        class_name="w-full",
    )
