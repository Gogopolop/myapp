import reflex as rx

from db.repository_store import get_top_repositories, get_analysis_by_repo

CATEGORY_LABELS = {
    "security": "Security",
    "activity": "Activity",
    "documentation": "Documentation",
    "ci": "CI/CD",
    "issues": "Issues",
    "code_health": "Code Health",
}


class RatingState(rx.State):
    top_repos: list[dict] = []
    compare_repo: str = ""
    compare_analysis: dict = {}

    def load_top_repos(self):
        self.top_repos = get_top_repositories(limit=10)

    def select_compare(self, repo: str):
        self.compare_repo = repo
        self.compare_analysis = get_analysis_by_repo(repo) or {}

    @rx.var
    def has_compare(self) -> bool:
        return bool(self.compare_analysis)

    @rx.var
    def compare_score(self) -> int:
        value = self.compare_analysis.get("score")
        return int(value) if value is not None else 0

    @rx.var
    def compare_category_rows(self) -> list[dict]:
        categories = self.compare_analysis.get("categories", {}) or {}
        rows = []
        for key, label in CATEGORY_LABELS.items():
            value = categories.get(key)
            rows.append({
                "label": label,
                "value": int(value) if value is not None else 0,
                "has_data": value is not None,
            })
        return rows