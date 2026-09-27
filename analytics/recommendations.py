# генерирует рекомендации на основе оценок и данных

def generate_recommendations(categories: dict, data: dict) -> list:

    recs = []

    # Security
    sec = categories.get("security")
    if sec is None:
        recs.append({
            "priority": "low",
            "problem": "Нет данных по безопасности",
            "fact": "Информация об уязвимостях недоступна",
            "action": "Подключить проверку зависимостей на уязвимости",
            "impact": "Позволит учитывать Security в общем балле",
        })
    elif sec < 90:
        findings = data.get("appsec_findings", [])
        open_count = sum(1 for f in findings if f.get("status") == "open")
        recs.append({
            "priority": "high",
            "problem": "Обнаружены уязвимости в зависимостях",
            "fact": f"AppSec: {open_count} открытых уязвимостей",
            "action": "Обновить пакеты до безопасных версий",
            "impact": "+10 к Security",
        })

    # Activity
    act = categories.get("activity")
    if act is None:
        recs.append({
            "priority": "low",
            "problem": "Нет данных об активности",
            "fact": "Информация о коммитах недоступна",
            "action": "Подключить историю коммитов репозитория",
            "impact": "Позволит учитывать Activity в общем балле",
        })
    elif act < 60:
        commits_count = len(data.get("commits", []))
        recs.append({
            "priority": "high",
            "problem": "Низкая активность разработки",
            "fact": f"Всего {commits_count} коммитов",
            "action": "Увеличить частоту коммитов и вовлечь контрибьюторов",
            "impact": "+15 к Activity",
        })

    # Documentation
    doc = categories.get("documentation")
    if doc is not None and doc < 70:
        files = data.get("files", [])
        missing = []
        if not any(f.lower().startswith("readme") for f in files):
            missing.append("README")
        if not any(f.lower().startswith("license") for f in files):
            missing.append("LICENSE")
        if not any("contributing" in f.lower() for f in files):
            missing.append("CONTRIBUTING")
        recs.append({
            "priority": "medium",
            "problem": "Недостаточная документация",
            "fact": f"Отсутствуют: {', '.join(missing) or 'нет'}",
            "action": "Добавить README, LICENSE и CONTRIBUTING",
            "impact": "+10 к Documentation",
        })

    # CI/CD
    ci = categories.get("ci")
    if ci is not None and ci < 90:
        runs = data.get("ci_runs", [])
        failed = sum(1 for r in runs if r.get("status") == "failed")
        recs.append({
            "priority": "medium",
            "problem": "Нестабильный CI/CD",
            "fact": f"{failed} из {len(runs)} прогонов завершились неудачей",
            "action": "Починить падающие пайплайны",
            "impact": "+8 к CI/CD",
        })

    # Issues
    iss = categories.get("issues")
    if iss is not None and iss < 75:
        issues = data.get("issues", [])
        open_count = sum(1 for i in issues if i.get("state") == "open")
        recs.append({
            "priority": "medium",
            "problem": "Много открытых issues",
            "fact": f"{open_count} из {len(issues)} issues открыты",
            "action": "Закрыть устаревшие задачи",
            "impact": "+10 к Issues",
        })

    # Code Health
    code = categories.get("code_health")
    if code is not None and code < 80:
        recs.append({
            "priority": "low",
            "problem": "Накоплен технический долг",
            "fact": "Обнаружены TODO/FIXME в коде",
            "action": "Разобрать TODO/FIXME комментарии",
            "impact": "+5 к Code Health",
        })

    order = {"high": 0, "medium": 1, "low": 2}
    recs.sort(key=lambda r: order.get(r["priority"], 3))

    return recs