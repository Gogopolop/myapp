import reflex as rx

from ..state.rating_state import RatingState
from ..state.repo_analysis_state import RepoAnalysisState
from .dashboard import category_bar, navbar

BG_COLOR = "#faf9f6"


def _medal_color(index):
    return rx.cond(
        index == 0, "#dfbd55",
        rx.cond(index == 1, "#a7b7c2",
                rx.cond(index == 2, "#e3a184", "#c9c5b8")),
    )


def _medal_bg(index):
    return rx.cond(
        index == 0, "#faf3d9",
        rx.cond(index == 1, "#eef1f3",
                rx.cond(index == 2, "#fbe9df", "#f2f0eb")),
    )


def _score_color(score):
    return rx.cond(
        score >= 70, "#5a7d52",
        rx.cond(score >= 40, "#c99a3f", "#c1573a"),
    )


def _repo_list_item(item, index) -> rx.Component:
    score = item["score"].to(int)
    return rx.el.div(
        rx.el.div(
            f"{(index + 1).to_string()}",
            class_name="flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-lg font-semibold",
            style={"color": _medal_color(index), "background_color": _medal_bg(index)},
        ),
        rx.el.div(
            rx.el.p(
                item["repo"].to(str),
                class_name="truncate text-base font-medium text-[#33352d]",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.span(
            score.to_string(),
            rx.el.span("/100", class_name="ml-0.5 text-xs font-normal text-[#aaa396]"),
            class_name="shrink-0 text-2xl font-semibold",
            style={"color": _score_color(score)},
        ),
        rx.el.button(
            "Сравнить",
            on_click=lambda: RatingState.select_compare(item["repo"]),
            class_name="ml-2 shrink-0 rounded-lg bg-[#242422] px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-[#fa6035]",
        ),
        class_name="flex items-center gap-4 border-b border-[#eeece5] px-5 py-5 last:border-0",
        key=item["repo"],
    )


def _leaderboard_card() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Рейтинг",
            class_name="text-[10px] font-medium tracking-[0.16em] text-[#a19785]",
        ),
        rx.el.h2(
            "Топ репозиториев",
            class_name="mt-2 mb-6 text-3xl font-medium tracking-[-0.8px] text-[#272722]",
        ),
        rx.el.div(
            rx.foreach(RatingState.top_repos, _repo_list_item),
            class_name="overflow-hidden rounded-2xl border border-[#e2dfd5] bg-white",
        ),
        class_name="w-full",
    )


def _analysis_column(title, score, category_rows) -> rx.Component:
    return rx.el.div(
        rx.el.p(title, class_name="mb-1 text-sm font-medium text-[#66645e]"),
        rx.el.div(
            rx.el.span(score.to_string(), class_name="text-5xl font-medium tracking-[-2px] text-[#f2613c]"),
            rx.el.span("/100", class_name="mb-1 text-lg text-[#aaa396]"),
            class_name="mb-5 flex items-end gap-1",
        ),
        rx.foreach(category_rows, category_bar),
        class_name="w-full md:w-[48%]",
    )


def _comparison_section() -> rx.Component:
    return rx.cond(
        RatingState.has_compare,
        rx.el.div(
            rx.el.p(
                "Сравнение",
                class_name="text-[10px] font-medium tracking-[0.16em] text-[#a19785]",
            ),
            rx.el.h2(
                "Ваш репозиторий vs выбранный",
                class_name="mt-2 mb-6 text-2xl font-medium tracking-[-0.6px] text-[#272722]",
            ),
            rx.cond(
                RepoAnalysisState.has_analysis,
                rx.el.div(
                    _analysis_column(
                        rx.cond(RepoAnalysisState.repo_name != "", RepoAnalysisState.repo_name, "Ваш репозиторий"),
                        RepoAnalysisState.score,
                        RepoAnalysisState.category_rows,
                    ),
                    _analysis_column(
                        RatingState.compare_repo,
                        RatingState.compare_score,
                        RatingState.compare_category_rows,
                    ),
                    class_name="flex flex-col gap-10 md:flex-row md:justify-between",
                ),
                rx.el.p(
                    "Сначала проанализируйте свой репозиторий на главной странице — "
                    "тогда здесь появится сравнение.",
                    class_name="text-sm text-[#8c8578]",
                ),
            ),
            class_name="mt-16 border-t border-[#e2dfd5] pt-12",
        ),
    )


def rating_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.link(
                rx.button(
                    rx.hstack(rx.text("←", font_size="16px"),
                              rx.text("Назад", font_size="14px", font_weight="600"),
                              spacing="2", align="center"),
                    background_color="#242422", color="white",
                    border_radius="10px",
                    padding_x=["14px", "18px", "20px"],
                    padding_y=["8px", "10px", "10px"],
                ),
                href="/app",
                _hover={"text_decoration": "none"},
                display="block",
                margin_bottom="20px",
            ),
            _leaderboard_card(),
            _comparison_section(),
            class_name="mx-auto w-full max-w-[820px] px-5 pt-14 pb-20 md:px-12",
        ),
        class_name="min-h-dvh w-full bg-[#faf9f6] font-['Inter',Arial,sans-serif]",
    )