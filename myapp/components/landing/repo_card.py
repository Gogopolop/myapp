import reflex as rx
from myapp.api.repositories import Repository, RepositoryFile, HealthReason
from myapp.data.content import UI


def file_row(item: RepositoryFile) -> rx.Component:
    return rx.el.div(
        rx.icon(
            rx.cond(item["folder"], "folder", "file-text"),
            class_name="h-4 w-4 shrink-0 text-[#859098]",
        ),
        rx.el.span(
            item["name"].to(str),
            class_name="w-32 shrink-0 truncate text-[#41474c]",
        ),
        rx.el.span(
            item["note"].to(str),
            class_name="hidden flex-1 truncate text-[#969ba0] sm:block",
        ),
        rx.el.span(
            item["date"].to(str),
            class_name="ml-auto shrink-0 text-[10px] text-[#93989d]",
        ),
        class_name="flex items-center gap-2.5 border-b border-[#eeeff0] px-4 py-3 text-xs last:border-0 hover:bg-[#f5f6f7]",
        key=item["name"],
    )


def repo_card(repo: Repository) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "book-marked", class_name="h-4 w-4 shrink-0 text-[#717b83]"
                ),
                rx.el.a(
                    repo["name"].to(str),
                    href=repo["url"].to(str),
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name="min-w-0 truncate text-sm font-medium text-[#435e78] hover:underline",
                ),
                rx.el.span(
                    UI["public"],
                    class_name="rounded-full border border-[#d9dee1] px-2 py-0.5 text-[9px] text-[#77818a]",
                ),
                rx.el.span(
                    rx.icon("star", class_name="h-3.5 w-3.5"),
                    repo["stars"].to(str),
                    title=UI["star_label"],
                    class_name="ml-auto flex shrink-0 items-center gap-1.5 rounded-md border border-[#d9dee1] bg-white px-2 py-1 text-[10px] text-[#68717a]",
                ),
                class_name="flex items-center gap-2.5",
            ),
            rx.el.div(
                rx.icon("code", class_name="h-4 w-4"),
                UI["code"],
                class_name="mt-5 flex w-fit items-center gap-2 border-b-2 border-[#f38d72] pb-3 text-xs text-[#444b50]",
            ),
            class_name="border-b border-[#dce0e3] bg-[#f6f8fa] px-4 pt-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(repo["healthy"], "activity", "triangle-alert"),
                    class_name="h-5 w-5 shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        repo["status"].to(str), class_name="font-medium text-xs"
                    ),
                    rx.el.p(
                        repo["summary"].to(str),
                        class_name="mt-1 text-[10px] opacity-75",
                    ),
                ),
                rx.el.span(
                    f"{repo['score']}{UI['score_suffix']}",
                    class_name="ml-auto text-lg font-semibold",
                ),
                class_name=rx.cond(
                    repo["healthy"],
                    "flex items-center gap-3 rounded-md border border-[#cdded2] bg-[#eff6f0] p-3 text-[#52745a]",
                    "flex items-center gap-3 rounded-md border border-[#ead7c5] bg-[#fcf3e9] p-3 text-[#9d7448]",
                ),
            ),
            rx.el.div(
                rx.el.span(
                    rx.icon("git-branch", class_name="h-3.5 w-3.5"),
                    repo["branch"].to(str),
                    class_name="flex items-center gap-2 rounded-md border border-[#d9dee1] bg-[#f6f8fa] px-3 py-1.5 text-xs text-[#596269]",
                ),
                rx.el.a(
                    UI["github"],
                    rx.icon("arrow-up-right", class_name="h-3 w-3"),
                    href=repo["url"].to(str),
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name="flex items-center gap-1 text-[10px] text-[#777f86] hover:text-[#e9663f]",
                ),
                class_name="my-3 flex items-center justify-between gap-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "git-commit-horizontal",
                        class_name="h-4 w-4 text-[#80949f]",
                    ),
                    rx.el.span(repo["commit"].to(str), class_name="truncate"),
                    class_name="flex items-center gap-2 border-b border-[#dce0e3] bg-[#f2f6fa] px-4 py-3 text-[11px] text-[#6b7885]",
                ),
                rx.el.div(
                    rx.foreach(
                        repo["files"].to(list[RepositoryFile]), file_row
                    ),
                    tab_index=0,
                    role="region",
                    aria_label=UI["files"],
                    class_name="h-[224px] overflow-y-auto overscroll-contain bg-white focus-visible:outline-2 focus-visible:outline-orange-400",
                ),
                class_name="overflow-hidden rounded-md border border-[#dce0e3]",
            ),
            class_name="p-4",
        ),
        class_name="min-w-0 w-full overflow-hidden rounded-xl border border-[#d5d9dc] bg-white",
    )


def reason(item: HealthReason) -> rx.Component:
    return rx.el.div(
        rx.icon(
            rx.cond(item["positive"], "check", "minus"),
            class_name=rx.cond(
                item["positive"],
                "mt-1 h-4 w-4 shrink-0 text-[#71836a]",
                "mt-1 h-4 w-4 shrink-0 text-[#b88a67]",
            ),
        ),
        rx.el.div(
            rx.el.h4(
                item["title"].to(str),
                class_name="text-sm font-medium text-[#383831]",
            ),
            rx.el.p(
                item["description"].to(str),
                class_name="mt-1.5 text-[13px] leading-[1.7] text-[#878276]",
            ),
        ),
        class_name="flex items-start gap-3",
        key=item["title"],
    )


def repository_example(repo: Repository) -> rx.Component:
    return rx.el.article(
        repo_card(repo),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    repo["score"].to(int),
                    class_name=rx.cond(
                        repo["healthy"],
                        "text-[60px] leading-none tracking-[-3px] font-medium text-[#6d7e5f]",
                        "text-[60px] leading-none tracking-[-3px] font-medium text-[#bd8a62]",
                    ),
                ),
                rx.el.span(
                    UI["score_suffix"],
                    class_name="mb-1 text-2xl text-[#aaa396]",
                ),
                rx.el.span(
                    UI["score_label"],
                    class_name="ml-4 mb-2 text-xs text-[#9a9488]",
                ),
                class_name="mb-5 flex items-end",
            ),
            rx.el.h3(
                rx.cond(repo["healthy"], UI["good_label"], UI["bad_label"]),
                class_name="text-[23px] font-medium tracking-[-0.6px] text-[#37382f]",
            ),
            rx.el.p(
                rx.cond(repo["healthy"], UI["good_intro"], UI["bad_intro"]),
                class_name="mt-3 mb-7 text-sm leading-6 text-[#8c8578]",
            ),
            rx.el.div(
                rx.foreach(repo["reasons"].to(list[HealthReason]), reason),
                class_name="flex flex-col gap-6",
            ),
            class_name="lg:pl-4",
        ),
        class_name="grid items-center gap-8 md:grid-cols-[1.25fr_1fr] lg:gap-16",
        key=repo["name"],
    )
