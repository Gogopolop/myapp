import json
from datetime import datetime
from pathlib import Path
from db.repository_store import save_analysis, track_repo

import reflex as rx

from ..api.sourcecraft_client import SourceCraftError, fetch_repository_snapshot
from analytics.transform import to_analyzer_input
from analytics.analyzer import analyze_repo
from db.repository_store import save_analysis
from analytics.report import build_markdown_report

EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"

CATEGORY_LABELS = {
    "security": "Security",
    "activity": "Activity",
    "documentation": "Documentation",
    "ci": "CI/CD",
    "issues": "Issues",
    "code_health": "Code Health",
}


class RepoAnalysisState(rx.State):
    pat: str = ""
    repo_url: str = ""

    is_loading: bool = False
    error: str = ""
    success_message: str = ""

    raw_data: dict = {}
    analysis: dict = {}

    def set_pat(self, value: str):
        self.pat = value

    def set_repo_url(self, value: str):
        self.repo_url = value

    @rx.event(background=True)
    async def analyze(self):
        async with self:
            self.error = ""
            self.success_message = ""
            if not self.pat.strip():
                self.error = "Укажите PAT-токен"
                return
            if not self.repo_url.strip():
                self.error = "Укажите ссылку на репозиторий"
                return
            self.is_loading = True

        try:
            data = await fetch_repository_snapshot(self.repo_url, self.pat)
            analyzer_input = to_analyzer_input(data, pat=self.pat)
            result = analyze_repo(analyzer_input)
        except SourceCraftError as exc:
            async with self:
                self.error = str(exc)
                self.is_loading = False
            return
        except Exception:
            async with self:
                self.error = "Не удалось получить данные репозитория"
                self.is_loading = False
            return

        org = data["repository"].get("organization", {}).get("slug", "org")
        repo = data["repository"].get("slug", "repo")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._save_json(data, f"{org}_{repo}_{timestamp}_raw.json")
        self._save_json(result, f"{org}_{repo}_{timestamp}_analysis.json")

        save_analysis(result)
        track_repo(self.repo_url, self.pat)

        async with self:
            self.raw_data = data
            self.analysis = result
            self.is_loading = False
            self.success_message = f"Готово: score = {result.get('score')}"

        yield rx.redirect("/dashboard")

    def _save_json(self, payload: dict, filename: str) -> Path:
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = EXPORTS_DIR / filename
        file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return file_path

    def download_report(self):
        if not self.analysis:
            return
        content = build_markdown_report(self.analysis)
        repo_name = self.analysis.get("repo", "report")
        return rx.download(data=content, filename=f"{repo_name}_report.md")

    # ─── вычисляемые данные для страницы ───

    @rx.var
    def has_analysis(self) -> bool:
        return bool(self.analysis)

    @rx.var
    def score(self) -> int:
        value = self.analysis.get("score")
        return int(value) if value is not None else 0

    @rx.var
    def repo_name(self) -> str:
        return self.analysis.get("repo", "")

    @rx.var
    def category_rows(self) -> list[dict]:
        categories = self.analysis.get("categories", {}) or {}
        rows = []
        for key, label in CATEGORY_LABELS.items():
            value = categories.get(key)
            rows.append({
                "label": label,
                "value": int(value) if value is not None else 0,
                "has_data": value is not None,
            })
        return rows

    @rx.var
    def recommendations(self) -> list[dict]:
        return self.analysis.get("recommendations", [])

    @rx.var
    def strengths(self) -> list[str]:
        categories = self.analysis.get("categories", {}) or {}
        return [CATEGORY_LABELS[k] for k, v in categories.items() if v is not None and v >= 60]

    @rx.var
    def weaknesses(self) -> list[str]:
        categories = self.analysis.get("categories", {}) or {}
        return [CATEGORY_LABELS[k] for k, v in categories.items() if v is not None and v < 60]

