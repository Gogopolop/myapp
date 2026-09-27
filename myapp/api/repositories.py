from typing import TypedDict


class RepositoryFile(TypedDict):
    name: str
    note: str
    date: str
    folder: bool


class HealthReason(TypedDict):
    title: str
    description: str
    positive: bool


class Repository(TypedDict):
    name: str
    url: str
    stars: str
    score: int
    healthy: bool
    status: str
    summary: str
    commit: str
    updated: str
    branch: str
    files: list[RepositoryFile]
    reasons: list[HealthReason]


# Integration boundary: a future provider should return list[Repository].
# Replace REPOSITORIES in data/content.py with validated provider results in a
# state event when integration is requested. Keep credentials on the server.
# score: integer 0–10; url: HTTPS; files/reasons: complete typed records.
# Empty, loading and error states belong to that future integration layer.
# This module intentionally performs no I/O and implements no mock transport.
