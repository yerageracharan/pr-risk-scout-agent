"""Unified-diff parser that preserves additions and deletions safely."""
from __future__ import annotations

import re
from pathlib import PurePosixPath

HUNK_RE = re.compile(
    r"^@@ -(?P<old>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new>\d+)(?:,(?P<new_count>\d+))? @@"
)


def normalise_path(path: str) -> str:
    """Normalise a Git diff path and reject absolute/traversal paths."""
    if not isinstance(path, str):
        raise TypeError("diff path must be a string")
    path = path.strip()
    if not path or "\x00" in path or "\\" in path:
        raise ValueError("diff path is empty or contains an invalid character")
    if path.startswith(("/", "~")):
        raise ValueError("absolute diff paths are not allowed")
    if path.startswith(("a/", "b/")):
        path = path[2:]
    parsed = PurePosixPath(path)
    if not parsed.parts or any(part in {".", ".."} for part in parsed.parts):
        raise ValueError("diff path contains an unsafe path component")
    if parsed.is_absolute():
        raise ValueError("absolute diff paths are not allowed")
    return str(parsed)


def parse_unified_diff(diff_text: str, file_path: str | None = None) -> list[dict]:
    """Return changed lines; enforce hunk counts and safe relative paths."""
    if not isinstance(diff_text, str):
        raise TypeError("diff_text must be a string")
    if len(diff_text) > 10 * 1024 * 1024:
        raise ValueError("diff exceeds the 10 MB parser limit")

    records: list[dict] = []
    current_file = normalise_path(file_path) if file_path else None
    old_line: int | None = None
    new_line: int | None = None
    old_remaining = new_remaining = 0

    def finish_hunk() -> None:
        if old_line is not None and (old_remaining or new_remaining):
            raise ValueError(
                "diff hunk ended before its declared old/new line counts were consumed"
            )

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git "):
            finish_hunk()
            old_line = new_line = None
            current_file = None
            continue
        if raw.startswith("--- "):
            finish_hunk()
            path = raw[4:].split("\t", 1)[0].strip()
            if path != "/dev/null":
                current_file = normalise_path(path)
            continue
        if raw.startswith("+++ "):
            path = raw[4:].split("\t", 1)[0].strip()
            if path != "/dev/null":
                current_file = normalise_path(path)
            continue

        match = HUNK_RE.match(raw)
        if match:
            finish_hunk()
            if current_file is None:
                raise ValueError("diff hunk has no file path")
            old_line = int(match.group("old"))
            new_line = int(match.group("new"))
            old_remaining = int(match.group("old_count") or 1)
            new_remaining = int(match.group("new_count") or 1)
            continue

        if old_line is None or new_line is None or current_file is None:
            continue
        if raw.startswith("\\"):
            continue
        if raw.startswith("+"):
            if new_remaining < 1:
                raise ValueError("diff hunk contains more added lines than declared")
            records.append({"file": current_file, "change": "added", "line": new_line, "content": raw[1:]})
            new_line += 1
            new_remaining -= 1
        elif raw.startswith("-"):
            if old_remaining < 1:
                raise ValueError("diff hunk contains more removed lines than declared")
            records.append({"file": current_file, "change": "removed", "line": old_line, "content": raw[1:]})
            old_line += 1
            old_remaining -= 1
        elif raw.startswith(" "):
            if old_remaining < 1 or new_remaining < 1:
                raise ValueError("diff hunk contains more context lines than declared")
            old_line += 1
            new_line += 1
            old_remaining -= 1
            new_remaining -= 1
        else:
            # Metadata may appear between file headers and hunks; content in a
            # hunk must be context/add/remove or the no-newline marker.
            if old_remaining or new_remaining:
                raise ValueError("diff hunk contains an invalid line prefix")

    finish_hunk()
    return records
