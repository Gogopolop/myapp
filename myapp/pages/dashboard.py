import reflex as rx

from ..state.repo_analysis_state import RepoAnalysisState

# ═══════════════════════════════════════════════════════════
#  ЦВЕТА
# ═══════════════════════════════════════════════════════════
BG_COLOR       = "#faf9f6"
CARD_BG        = "#FFFFFF"
TEXT_MAIN      = "#1A1A1A"
TEXT_MUTED     = "#8B8B8B"
ACCENT_ORANGE  = "#E76F51"
SOFT_ORANGE_BG = "#FBE9E3"
BORDER_COLOR   = "#EFEAE3"
GREEN          = "#4CAF7D"
YELLOW         = "#E5B84B"
LIGHT_GRAY     = "#E8E5E0"
GRAY_BG        = "#F2F2F0"
GRAY_BORDER    = "#DCDCD8"

VERDICT_GOOD_TEXT = "#4D7A5A"
VERDICT_GOOD_BG   = "#EAF6EE"
VERDICT_MID_TEXT  = "#9A7A2A"
VERDICT_MID_BG    = "#FBF1D9"
VERDICT_BAD_TEXT  = "#C14F2D"
VERDICT_BAD_BG    = "#FCEAE4"

MAX_CONTENT = "1200px"
PAD_PAGE = ["16px", "24px", "48px"]
PAD_CARD = ["16px", "20px", "28px"]

TWO_COLS = "calc(50% - 16px)"

CHART_AREA_H = 180
BAR_MAX_W    = 40


# ═══════════════════════════════════════════════════════════
#  ВЕРДИКТ + ЦВЕТ ПО БАЛЛУ
# ═══════════════════════════════════════════════════════════
def verdict_badge(score) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                width="10px", height="10px",
                border_radius="9999px",
                background_color=rx.cond(
                    score >= 60, GREEN,
                    rx.cond(score >= 30, YELLOW, ACCENT_ORANGE)),
                flex_shrink="0",
            ),
            rx.text(
                rx.cond(score >= 60, "Отличный репозиторий",
                        rx.cond(score >= 30, "Хороший репозиторий",
                                "Плохой репозиторий")),
                font_size="12px",
                font_weight="600",
                color=rx.cond(
                    score >= 60, VERDICT_GOOD_TEXT,
                    rx.cond(score >= 30, VERDICT_MID_TEXT,
                            VERDICT_BAD_TEXT)),
                margin_left="8px",
            ),
            spacing="0", align="center",
        ),
        background_color=rx.cond(
            score >= 60, VERDICT_GOOD_BG,
            rx.cond(score >= 30, VERDICT_MID_BG,
                    VERDICT_BAD_BG)),
        padding="8px 14px", border_radius="9999px",
    )


def score_color(score):
    return rx.cond(
        score >= 60, GREEN,
        rx.cond(score >= 30, YELLOW, ACCENT_ORANGE))


# ═══════════════════════════════════════════════════════════
#  КНОПКА ОТЧЁТА
# ═══════════════════════════════════════════════════════════
def report_button(label: str = "Скачать отчёт (Markdown)"):    return rx.button(
        rx.hstack(
            rx.icon("file-down", size=14),
            rx.text(label, font_size="12px", font_weight="500",
                    margin_left="6px"),
            spacing="0", align="center",
        ),
        background_color="transparent",
        color=ACCENT_ORANGE,
        border=f"1px solid {ACCENT_ORANGE}",
        border_radius="8px",
        padding="6px 12px",
        cursor="pointer",
        _hover={"background_color": SOFT_ORANGE_BG},
        on_click=RepoAnalysisState.download_report,
    )


# ═══════════════════════════════════════════════════════════
#  ГИСТОГРАММА
# ═══════════════════════════════════════════════════════════
def _grid_line(pct: int) -> rx.Component:
    return rx.box(
        rx.text(f"{pct}%", font_size="10px", color=TEXT_MUTED,
                width="30px", text_align="right", margin_right="8px"),
        rx.box(
            width="100%",
            height="1px",
            background_color=BORDER_COLOR,
            border_top=f"1px dashed {LIGHT_GRAY}",
        ),
        display="flex", align_items="center",
        width="100%",
    )


def _chart_grid() -> rx.Component:
    return rx.box(
        rx.box(
            _grid_line(100),
            _grid_line(80),
            _grid_line(60),
            _grid_line(40),
            _grid_line(20),
            _grid_line(0),
            display="flex", flex_direction="column",
            justify_content="space-between",
            height=f"{CHART_AREA_H}px",
            width="100%",
        ),
        position="absolute",
        top="0", left="0", right="0",
        pointer_events="none",
        z_index="0",
    )


def chart_bar(row) -> rx.Component:
    value = row["value"].to(int)
    label = row["label"]
    return rx.vstack(
        rx.box(
            rx.box(
                width=f"{BAR_MAX_W}px",
                height=f"{value * (CHART_AREA_H / 100)}px",
                background_color=ACCENT_ORANGE,
                border_radius="0",
                z_index="1",
            ),
            height=f"{CHART_AREA_H}px",
            width=f"{BAR_MAX_W}px",
            display="flex",
            align_items="flex-end",
            justify_content="center",
            position="relative",
            z_index="1",
        ),
        rx.text(f"{value}%", font_size="11px", color=TEXT_MAIN,
                font_weight="600", margin_top="6px"),
        rx.text(label, font_size="10px", color=TEXT_MUTED,
                text_align="center", white_space="nowrap"),
        spacing="0", align="center", justify="end",
    )


def category_bar(row) -> rx.Component:
    value = row["value"].to(int)
    color = rx.cond(value >= 60, GREEN, rx.cond(value >= 30, YELLOW, ACCENT_ORANGE))
    display_value = rx.cond(row["has_data"], f"{value}%", "нет данных")
    return rx.flex(
        rx.text(row["label"], font_size="13px", color=TEXT_MAIN, font_weight="500",
                width=["100%", "140px", "160px"]),
        rx.box(
            rx.box(width=f"{value}%", height="8px",
                   background_color=color, border_radius="9999px"),
            width="100%", height="8px",
            background_color=LIGHT_GRAY, border_radius="9999px", flex="1",
        ),
        rx.text(display_value, font_size="13px", color=TEXT_MAIN,
                font_weight="600", width="70px", text_align="right"),
        direction=rx.breakpoints(initial="column", md="row"),
        gap="2", width="100%",
        align=rx.breakpoints(initial="start", md="center"),
        margin_bottom="14px",
    )

# ═══════════════════════════════════════════════════════════
#  ТОЧКИ
# ═══════════════════════════════════════════════════════════
def strong_point(text) -> rx.Component:
    return rx.hstack(
        rx.box(width="6px", height="6px", border_radius="9999px",
               background_color=GREEN, margin_top="7px", flex_shrink="0"),
        rx.text(text, font_size="13px", color=TEXT_MAIN, margin_left="10px"),
        spacing="0", align="start",
    )


def problem_point(text) -> rx.Component:
    return rx.hstack(
        rx.box(width="6px", height="6px", border_radius="9999px",
               background_color=ACCENT_ORANGE, margin_top="7px",
               flex_shrink="0"),
        rx.text(text, font_size="13px", color=TEXT_MAIN, margin_left="10px"),
        spacing="0", align="start",
    )


# ═══════════════════════════════════════════════════════════
#  ГАРМОШКА РЕКОМЕНДАЦИЙ
# ═══════════════════════════════════════════════════════════
def _priority_badge_text(priority) -> rx.Component:
    return rx.text(
        rx.match(priority,
                 ("high", "Критично"),
                 ("medium", "Внимание"),
                 "Информация"),
        font_size="10px", font_weight="600",
        color=rx.match(priority,
                       ("high", "#C14F2D"),
                       ("medium", "#9A7A2A"),
                       "#4D7A5A"),
    )


def _rec_header(rec) -> rx.Component:
    return rx.flex(
        rx.box(
            width="10px", height="10px",
            border_radius="9999px",
            flex_shrink="0",
            background_color=rx.match(rec["priority"],
                                      ("high", ACCENT_ORANGE),
                                      ("medium", YELLOW),
                                      GREEN),
        ),
        rx.text(rec["problem"], font_weight="600", font_size="14px",
                color=TEXT_MAIN, flex="1", text_align="left",
                margin_left="10px"),
        rx.box(
            _priority_badge_text(rec["priority"]),
            background_color=rx.match(rec["priority"],
                                      ("high", "#FCEAE4"),
                                      ("medium", "#FBF1D9"),
                                      "#E8F0EA"),
            padding="4px 10px",
            border_radius="9999px",
            margin_left="10px",
            white_space="nowrap",
        ),
        width="100%", align="center",
    )


def _rec_content(rec) -> rx.Component:
    return rx.vstack(
        rx.text(rec["fact"], font_size="12px", color=TEXT_MUTED,
                margin_bottom="10px"),
        rx.hstack(
            rx.box(width="6px", height="6px", border_radius="9999px",
                   background_color=ACCENT_ORANGE, flex_shrink="0", margin_top="6px"),
            rx.text("Что сделать: ", font_size="11px", color=TEXT_MUTED,
                    font_weight="600", margin_left="10px"),
            rx.text(rec["action"], font_size="13px", color=TEXT_MAIN, margin_left="2px"),
            spacing="0", align="start", wrap="wrap",
        ),
        rx.hstack(
            rx.box(width="6px", height="6px", border_radius="9999px",
                   background_color=GREEN, flex_shrink="0", margin_top="6px"),
            rx.text("Эффект: ", font_size="11px", color=TEXT_MUTED,
                    font_weight="600", margin_left="10px"),
            rx.text(rec["impact"], font_size="13px", color=GREEN,
                    font_weight="600", margin_left="2px"),
            spacing="0", align="start", wrap="wrap",
        ),
        spacing="3", align="start", width="100%",
    )


def recommendations_accordion(recommendations) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.text("Комментарии аналитика",
                            font_size=["14px", "15px", "16px"],
                            font_weight="700", color=TEXT_MAIN),
                    rx.text("Автоматический разбор слабых мест репозитория",
                            font_size="12px", color=TEXT_MUTED, margin_top="2px"),
                    spacing="0", align="start",
                ),
                rx.spacer(),
                report_button(),
                width="100%", align="center", justify="between", margin_bottom="16px",
            ),
            rx.accordion.root(
                rx.foreach(
                    recommendations,
                    lambda rec: rx.accordion.item(
                        header=_rec_header(rec),
                        content=_rec_content(rec),
                        value=rec["problem"],
                    ),
                ),
                collapsible=True, variant="ghost",
                width="100%", color_scheme="orange",
            ),
            spacing="0", width="100%", align="start",
        ),
        width="100%", padding=PAD_CARD,
        background_color=CARD_BG,
        border=f"1px solid {BORDER_COLOR}",
        border_radius="14px", margin_bottom="20px",
    )


# ═══════════════════════════════════════════════════════════
#  ГАРМОШКА «КАК СЧИТАЕТСЯ АНАЛИТИКА» — без изменений
# ═══════════════════════════════════════════════════════════
def how_it_works_accordion() -> rx.Component:
    return rx.box(
        rx.accordion.root(
            rx.accordion.item(
                header=rx.vstack(
                    rx.text("Как считается аналитика", font_weight="600",
                            font_size="14px", color=TEXT_MAIN),
                    rx.text("Что влияет на итоговую оценку и откуда берутся проценты",
                            font_size="12px", color=TEXT_MUTED, margin_top="2px"),
                    spacing="0", align="start", width="100%",
                ),
                content=rx.vstack(
                    rx.text("Формула итоговой оценки", font_size="13px",
                            font_weight="700", color=TEXT_MAIN, margin_bottom="6px"),
                    rx.text(
                        "Итоговый балл — это взвешенная сумма шести категорий. "
                        "Каждая категория имеет свой вес: чем важнее, тем больше "
                        "влияет на итог.",
                        font_size="13px", color=TEXT_MAIN, line_height="1.6",
                        margin_bottom="10px",
                    ),
                    rx.box(
                        rx.text(
                            "score = 0.20·security + 0.15·activity + "
                            "0.15·documentation + 0.15·ci + "
                            "0.15·issues + 0.20·code_health",
                            font_size="12px", color=TEXT_MAIN,
                            white_space="pre-wrap", line_height="1.6",
                            font_family="monospace",
                        ),
                        background_color="#FFFFFF", padding="12px 14px",
                        border_radius="8px", width="100%", margin_bottom="10px",
                    ),
                    rx.text(
                        "Если данных по какой-то категории нет — она не "
                        "учитывается, вес пересчитывается автоматически.",
                        font_size="12px", color=TEXT_MUTED, line_height="1.6",
                        margin_bottom="18px",
                    ),
                    spacing="0", align="start", width="100%",
                ),
                value="how",
            ),
            collapsible=True, variant="ghost",
            width="100%", color_scheme="gray",
        ),
        width="100%", padding=["12px", "14px", "16px"],
        background_color=GRAY_BG,
        border=f"1px solid {GRAY_BORDER}",
        border_radius="14px", margin_bottom="20px",
    )


# ═══════════════════════════════════════════════════════════
#  НАВБАР
# ═══════════════════════════════════════════════════════════
def navbar():
    return rx.box(
        rx.flex(
            rx.hstack(
                rx.box(width="12px", height="12px", border_radius="9999px",
                       background_color=ACCENT_ORANGE, flex_shrink="0"),
                rx.text("SourceCraft", font_weight="700", font_size="18px",
                        color=TEXT_MAIN, margin_left="10px"),
                rx.text("RepoPuls", font_size="14px", color=TEXT_MUTED,
                        margin_left="8px"),
                spacing="0", align="center",
            ),
            rx.spacer(),
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon("trophy", size=14),
                        rx.text("Рейтинг", font_size="13px", font_weight="500",
                                margin_left="6px"),
                        spacing="0", align="center",
                    ),
                    background_color="#1A1A1A", color="white",
                    border_radius="10px",
                    padding_x=["14px", "18px", "22px"],
                    padding_y=["8px", "8px", "10px"],
                ),
                href="/rating",
                _hover={"text_decoration": "none"},
            ),
            width="100%", max_width=MAX_CONTENT, margin="0 auto",
            align="center", justify="between",
        ),
        width="100%", padding=["14px 16px", "16px 32px", "20px 48px"],
        border_bottom=f"1px solid {BORDER_COLOR}",
        background_color=BG_COLOR,
    )
# ═══════════════════════════════════════════════════════════
#  ПУСТОЕ СОСТОЯНИЕ (анализ ещё не запускали)
# ═══════════════════════════════════════════════════════════
def _empty_state() -> rx.Component:
    return rx.vstack(
        rx.text("Здесь появится аналитика по репозиторию",
                font_size="18px", font_weight="600", color=TEXT_MAIN),
        rx.text("Сначала запустите анализ на главной странице.",
                font_size="14px", color=TEXT_MUTED, margin_top="6px"),
        rx.link(
            rx.button("На главную", background_color=ACCENT_ORANGE, color="white",
                      border_radius="10px", padding="10px 20px", margin_top="20px"),
            href="/app",
        ),
        align="center", justify="center",
        padding="80px 20px",
        width="100%",
    )


# ═══════════════════════════════════════════════════════════
#  СТРАНИЦА
# ═══════════════════════════════════════════════════════════
def dashboard_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.cond(
            RepoAnalysisState.has_analysis,
            rx.vstack(
                rx.link(
                    rx.button(
                        rx.hstack(rx.text("←", font_size="16px"),
                                  rx.text("Назад", font_size="14px", font_weight="600"),
                                  spacing="2", align="center"),
                        background_color=ACCENT_ORANGE, color="white",
                        border_radius="10px",
                        padding_x=["14px", "18px", "20px"],
                        padding_y=["8px", "10px", "10px"],
                    ),
                    href="/app", _hover={"text_decoration": "none"},
                    align_self="start", margin_bottom="20px",
                ),

                rx.box(
                    rx.vstack(
                        rx.text(RepoAnalysisState.repo_name,
                                font_size=["18px", "20px", "22px"],
                                font_weight="700", color=TEXT_MAIN),
                        rx.text(RepoAnalysisState.repo_url,
                                font_size="13px", color=TEXT_MUTED),
                        spacing="1", align="start",
                    ),
                    width="100%", padding=PAD_CARD,
                    background_color=SOFT_ORANGE_BG,
                    border_radius="14px", margin_bottom="20px",
                ),

                rx.box(
                    rx.flex(
                        rx.hstack(
                            rx.text(RepoAnalysisState.score.to_string(),
                                    font_size=["40px", "48px", "52px"],
                                    font_weight="800", color=TEXT_MAIN),
                            rx.text("/100", font_size="18px", color=TEXT_MUTED),
                            spacing="1", align="end",
                        ),
                        rx.box(
                            rx.box(
                                width=f"{RepoAnalysisState.score}%", height="8px",
                                background_color=score_color(RepoAnalysisState.score),
                                border_radius="9999px",
                            ),
                            width="100%", height="8px",
                            background_color=LIGHT_GRAY, border_radius="9999px",
                            flex="1", margin=["12px 0", "0 20px", "0 24px"],
                        ),
                        verdict_badge(RepoAnalysisState.score),
                        direction=rx.breakpoints(initial="column", md="row"),
                        gap="3", width="100%",
                        align=rx.breakpoints(initial="start", md="center"),
                    ),
                    width="100%", padding=PAD_CARD,
                    background_color=CARD_BG,
                    border=f"1px solid {BORDER_COLOR}",
                    border_radius="14px", margin_bottom="20px",
                ),

                rx.box(
                    rx.vstack(
                        rx.text("Оценка по категориям",
                                font_size=["14px", "15px", "16px"],
                                font_weight="700", color=TEXT_MAIN, margin_bottom="16px"),
                        rx.box(
                            _chart_grid(),
                            rx.flex(
                                rx.foreach(
                                    RepoAnalysisState.category_rows,
                                    chart_bar,
                                ),
                                width="100%", justify="between", align="end",
                                gap="2", overflow_x="auto",
                                position="relative", z_index="1",
                                style={"padding-left": "60px", "padding-right": "0"},
                            ),
                            position="relative", width="100%",
                        ),
                        spacing="0", width="100%",
                    ),
                    width="100%", padding=PAD_CARD,
                    background_color=CARD_BG,
                    border=f"1px solid {BORDER_COLOR}",
                    border_radius="14px", margin_bottom="20px",
                ),

                rx.box(
                    rx.vstack(
                        rx.text("По категориям", font_size=["14px", "15px", "16px"],
                                font_weight="700", color=TEXT_MAIN, margin_bottom="16px"),
                        rx.foreach(RepoAnalysisState.category_rows, category_bar),
                        spacing="0", width="100%",
                    ),
                    width="100%", padding=PAD_CARD,
                    background_color=CARD_BG,
                    border=f"1px solid {BORDER_COLOR}",
                    border_radius="14px", margin_bottom="20px",
                ),

                rx.flex(
                    rx.vstack(
                        rx.text("Сильные стороны", font_size="14px", font_weight="700",
                                color=TEXT_MAIN, margin_bottom="12px"),
                        rx.foreach(RepoAnalysisState.strengths, strong_point),
                        spacing="3", align="start", width=TWO_COLS, min_width="240px",
                        padding=PAD_CARD, background_color=CARD_BG,
                        border=f"1px solid {BORDER_COLOR}", border_radius="14px",
                    ),
                    rx.vstack(
                        rx.text("Проблемы", font_size="14px", font_weight="700",
                                color=TEXT_MAIN, margin_bottom="12px"),
                        rx.foreach(RepoAnalysisState.weaknesses, problem_point),
                        spacing="3", align="start", width=TWO_COLS, min_width="240px",
                        padding=PAD_CARD, background_color=CARD_BG,
                        border=f"1px solid {BORDER_COLOR}", border_radius="14px",
                        margin_left="32px",
                    ),
                    width="100%", wrap="wrap", margin_bottom="20px", align="start",
                ),

                recommendations_accordion(RepoAnalysisState.recommendations),
                how_it_works_accordion(),

                width="100%", max_width=MAX_CONTENT, padding=PAD_PAGE,
                spacing="0", margin="0 auto",
            ),
            _empty_state(),
        ),

        rx.box(
            rx.hstack(
                rx.text("SourceCraft RepoPuls — анализ открытых репозиториев",
                        font_size="12px", color=TEXT_MUTED),
                width="100%", max_width=MAX_CONTENT, margin="0 auto", justify="center",
            ),
            width="100%", padding=["24px 16px", "32px 32px", "40px 48px"],
            border_top=f"1px solid {BORDER_COLOR}",
        ),

        background_color=BG_COLOR, min_height="100vh", font_family="Inter, sans-serif",
    )


