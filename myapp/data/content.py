from ..api.repositories import Repository, RepositoryFile  # ← станет
BRAND = "SourceCraft"
PRODUCT = "Repo Health"
PAGE_TITLE = "SourceCraft Repo Health — здоровье open-source проектов"
LINKS = {
    "home": "#top",
    "health": "#health",
    "login": "/auth/yandex/login",
}
UI = {
    "login": "Войти",
    "preview": "Просто посмотреть",
    "eyebrow": "OPEN SOURCE. ПОНЯТНЫМ ЯЗЫКОМ.",
    "hero_title": "Хороший код —",
    "hero_accent": "живой проект.",
    "hero_description": "Посмотрите на репозиторий за пределами кода.\nRepo Health поможет понять, живёт ли проект,\nразвивается ли сообщество и можно ли на него положиться.",
    "hero_note": "Меньше догадок. Больше сигналов.",
    "scroll": "Как это работает",
    "section_number": "01 / ЗДОРОВЬЕ РЕПОЗИТОРИЯ",
    "section_title": "Оценка жизнеспособности проекта",
    "section_description": "Звёзды — не вся история. Мы смотрим на активность, документацию\nи сообщество, чтобы за цифрой была понятная картина.",
    "demo": "Демонстрационные примеры · не результаты анализа GitHub",
    "good_label": "Есть на что положиться",
    "bad_label": "Стоит присмотреться",
    "good_intro": "Проект живёт и развивается. Здесь легко начать — и есть кому помочь.",
    "bad_intro": "Код открыт, но важные сигналы говорят о рисках. Изучите их перед использованием.",
    "score_suffix": "/10",
    "score_label": "здоровье проекта",
    "public": "Public",
    "code": "Код",
    "files": "Файлы репозитория",
    "github": "Открыть на GitHub",
    "star_label": "Звёзды",
    "footer": "У каждого проекта есть пульс.",
    "footer_sub": "Помогаем его услышать.",
    "footer_note": "SourceCraft Repo Health · Демонстрационная версия",
    "back": "Наверх",
    "skip": "Перейти к оценкам",
    "login_hint": "Перейти в SourceCraft (новая вкладка)",
}

FILE_SPECS = [
    (".github", "Настроены процессы разработки", True),
    ("docs", "Руководства и примеры", True),
    ("src", "Исходный код проекта", True),
    ("tests", "Автоматические тесты", True),
    ("examples", "Примеры использования", True),
    ("scripts", "Инструменты разработки", True),
    (".gitignore", "Исключения Git", False),
    ("LICENSE", "Условия использования", False),
    ("README.md", "Знакомство с проектом", False),
    ("CONTRIBUTING.md", "Как внести вклад", False),
    ("CHANGELOG.md", "История изменений", False),
    ("package.json", "Зависимости проекта", False),
]
GOOD_FILES: list[RepositoryFile] = [
    RepositoryFile(name=name, note=note, folder=folder, date="2 дня назад")
    for name, note, folder in FILE_SPECS
]
BAD_FILES: list[RepositoryFile] = [
    RepositoryFile(
        name=name,
        note="Первый коммит" if folder else "Обновление файла",
        folder=folder,
        date="3 года назад",
    )
    for name, note, folder in FILE_SPECS
    if name not in ("CONTRIBUTING.md", "CHANGELOG.md", "docs", "tests")
]
REPOSITORIES: list[Repository] = [
    {
        "name": "withastro / astro",
        "url": "https://github.com/withastro/astro",
        "stars": "48,2k",
        "score": 8,
        "healthy": True,
        "status": "Проект в хорошей форме",
        "summary": "Активная разработка и здоровое сообщество",
        "commit": "Обновлена документация и примеры",
        "updated": "2 дня назад",
        "branch": "main",
        "files": GOOD_FILES,
        "reasons": [
            {
                "title": "Разработка не останавливается",
                "description": "Регулярные коммиты и свежие релизы. Проект не стоит на месте.",
                "positive": True,
            },
            {
                "title": "Понятно, с чего начать",
                "description": "Есть README, документация и правила участия для новых контрибьюторов.",
                "positive": True,
            },
            {
                "title": "Сообщество на связи",
                "description": "На вопросы отвечают, pull request обсуждают и принимают.",
                "positive": True,
            },
        ],
    },
    {
        "name": "moment / moment",
        "url": "https://github.com/moment/moment",
        "stars": "48,1k",
        "score": 3,
        "healthy": False,
        "status": "Проекту не хватает активности",
        "summary": "Перед использованием стоит оценить риски",
        "commit": "Обновлён README.md",
        "updated": "3 года назад",
        "branch": "develop",
        "files": BAD_FILES,
        "reasons": [
            {
                "title": "Давно не было обновлений",
                "description": "Редкие коммиты могут означать, что исправления придётся ждать долго.",
                "positive": False,
            },
            {
                "title": "Не хватает ориентиров",
                "description": "Без подробной документации и правил участия сложнее разобраться в проекте.",
                "positive": False,
            },
            {
                "title": "Вопросы остаются открытыми",
                "description": "Низкая активность в обсуждениях — повод проверить доступность поддержки.",
                "positive": False,
            },
        ],
    },
]
