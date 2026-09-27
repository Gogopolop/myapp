"""Генерация читаемого Markdown-отчёта из результата analyze_repo()."""

PRIORITY_LABELS = {"high": "Критично", "medium": "Внимание", "low": "Информация"}
CATEGORY_LABELS = {
    "security": "Security",
    "activity": "Activity",
    "documentation": "Documentation",
    "ci": "CI/CD",
    "issues": "Issues",
    "code_health": "Code Health",
}


def build_markdown_report(analysis: dict) -> str:
    repo = analysis.get("repo", "unknown")
    score = analysis.get("score")
    categories = analysis.get("categories", {}) or {}
    recommendations = analysis.get("recommendations", []) or []

    score_display = f"{score}/100" if score is not None else "нет данных"

    lines = [
        f"# Отчёт по репозиторию: {repo}",
        "",
        f"**Итоговый балл:** {score_display}",
        "",
        "## Оценка по категориям",
        "",
        "| Категория | Балл |",
        "|---|---|",
    ]
    for key, value in categories.items():
        label = CATEGORY_LABELS.get(key, key)
        display = f"{value}%" if value is not None else "нет данных"
        lines.append(f"| {label} | {display} |")

    lines += ["", "## Рекомендации", ""]

    if not recommendations:
        lines.append("Рекомендаций нет.")
    else:
        for r in recommendations:
            priority = PRIORITY_LABELS.get(r.get("priority"), "Информация")
            lines += [
                f"### {r.get('problem', '')} ({priority})",
                "",
                f"- **Факт:** {r.get('fact', '')}",
                f"- **Что сделать:** {r.get('action', '')}",
                f"- **Эффект:** {r.get('impact', '')}",
                "",
            ]

    return "\n".join(lines)