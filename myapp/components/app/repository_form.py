import reflex as rx
from myapp.state.repo_analysis_state import RepoAnalysisState

TITLE = "Почувствуйте пульс"
TITLE_ACCENT = "вашего репозитория."
DESCRIPTION = "Добавьте ссылку на репозиторий и PAT-токен, чтобы начать анализ."
INPUT_LABEL = "Ссылка на репозиторий"
PLACEHOLDER = "Вставьте URL репозитория"
PAT_LABEL = "PAT-токен SourceCraft"
PAT_PLACEHOLDER = "Вставьте PAT-токен"
BUTTON_LABEL = "Анализировать"


def repository_form() -> rx.Component:
    return rx.el.section(
        rx.el.h2(
            TITLE,
            rx.el.br(),
            rx.el.span(TITLE_ACCENT, class_name="text-[#F06B45]"),
            id="analysis-title",
            class_name="text-[34px] font-semibold leading-[1.13] tracking-[-0.045em] text-[#17161C] sm:text-[48px] lg:text-[54px]",
        ),
        rx.el.p(
            DESCRIPTION,
            class_name="mt-5 text-sm leading-relaxed text-[#77736B] sm:text-base",
        ),
        rx.el.form(
            rx.el.label(INPUT_LABEL, html_for="repository-url", class_name="sr-only"),
            rx.el.div(
                rx.icon("link", class_name="ml-3 h-5 w-5 shrink-0 text-[#8D8981] sm:ml-4"),
                rx.el.input(
                    id="repository-url",
                    name="repository_url",
                    type="url",
                    placeholder=PLACEHOLDER,
                    value=RepoAnalysisState.repo_url,
                    on_change=RepoAnalysisState.set_repo_url,
                    auto_complete="url",
                    spell_check=False,
                    class_name="min-w-0 flex-1 bg-[#faf9f6] px-3 py-4 text-base text-[#17161C] outline-none placeholder:text-[#99958D] sm:py-5",
                ),
                class_name="flex min-w-0 flex-1 items-center rounded-xl focus-within:ring-2 focus-within:ring-[#F06B45]/50",
            ),
            rx.el.label(PAT_LABEL, html_for="pat-token", class_name="sr-only"),
            rx.el.div(
                rx.icon("key", class_name="ml-3 h-5 w-5 shrink-0 text-[#8D8981] sm:ml-4"),
                rx.el.input(
                    id="pat-token",
                    name="pat_token",
                    type="password",
                    placeholder=PAT_PLACEHOLDER,
                    value=RepoAnalysisState.pat,
                    on_change=RepoAnalysisState.set_pat,
                    spell_check=False,
                    class_name="min-w-0 flex-1 bg-white px-3 py-4 text-base text-[#17161C] outline-none placeholder:text-[#99958D] sm:py-5",
                ),
                class_name="mt-2 flex min-w-0 flex-1 items-center rounded-xl border border-[#E7E2D9] focus-within:ring-2 focus-within:ring-[#F06B45]/50 sm:mt-0",
            ),
            rx.el.button(
                rx.cond(RepoAnalysisState.is_loading, "Анализируем…", BUTTON_LABEL),
                rx.icon("arrow-up-right", class_name="h-5 w-5"),
                type="button",
                on_click=RepoAnalysisState.analyze,
                disabled=RepoAnalysisState.is_loading,
                class_name="flex shrink-0 items-center justify-center gap-5 rounded-xl bg-[#F06B45] px-7 py-4 text-sm font-semibold text-[#faf9f6] transition-colors hover:bg-[#DE5D38] disabled:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#F06B45] sm:py-5",
            ),
            on_submit=rx.prevent_default,
            class_name="mt-8 flex w-full flex-col gap-2 rounded-[20px] border border-[#E7E2D9] bg-[#faf9f6] p-2.5 text-left sm:flex-row",
        ),
        rx.cond(
            RepoAnalysisState.error != "",
            rx.el.p(RepoAnalysisState.error, class_name="mt-4 text-xs leading-relaxed text-red-500"),
        ),
        rx.cond(
            RepoAnalysisState.success_message != "",
            rx.el.p(RepoAnalysisState.success_message, class_name="mt-4 text-xs leading-relaxed text-green-600"),
        ),
        aria_labelledby="analysis-title",
        class_name="w-full pb-16 pt-14 text-center sm:pb-20 sm:pt-16",
    )