from analytics.metrics import (
    calc_activity,
    calc_documentation,
    calc_ci,
    calc_security,
    calc_issues,
)

WEIGHTS = {
    "security": 0.20,
    "activity": 0.15,
    "documentation": 0.15,
    "ci": 0.15,
    "issues": 0.15,
    "code_health": 0.20,
}


def calc_score(data: dict) -> dict:
    categories = {
        "security": calc_security(data.get("appsec_findings", [])),
        "activity": calc_activity(data),
        "documentation": calc_documentation(data.get("files", [])),
        "ci": calc_ci(data.get("ci_runs", [])),
        "issues": calc_issues(data.get("issues", [])),
        "code_health": data.get("code_health_score"),
    }

    has_any_data = any(v is not None for v in categories.values())
    if not has_any_data:
        return {"score": None, "categories": categories}

    total_weight = 0.0
    weighted_sum = 0.0
    for name, value in categories.items():
        if value is None:
            continue
        total_weight += WEIGHTS[name]
        weighted_sum += value * WEIGHTS[name]

    score = round(weighted_sum / total_weight, 2) if total_weight else None
    return {"score": score, "categories": categories}