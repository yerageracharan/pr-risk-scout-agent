"""Unified-diff parser that preserves additions and deletions."""
from __future__ import annotations
import re
from pathlib import PurePosixPath

HUNK_RE = re.compile(r"@@ -(?P<old>\d+)(?:,(?P<old_count>\d+))? \+(?P<new>\d+)(?:,(?P<new_count>\d+))? @@")


def normalise_path(path: str) -> str:
    path = path.strip()
    if path.startswith(("a/", "b/")):
        path = path[2:]
    return str(PurePosixPath(path))


def parse_unified_diff(diff_text: str, file_path: str | None = None) -> list[dict]:
    """Return changed lines with file, change direction, line number, and text."""
    records: list[dict] = []
    current_file = normalise_path(file_path) if file_path else None
    old_line: int | None = None
    new_line: int | None = None

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git "):
            old_line = new_line = None
            continue
        if raw.startswith("--- "):
            path = raw[4:].strip()
            if path != "/dev/null":
                current_file = normalise_path(path)
            continue
        if raw.startswith("+++ "):
            path = raw[4:].strip()
            if path != "/dev/null":
                current_file = normalise_path(path)
            continue
        match = HUNK_RE.match(raw)
        if match:
            old_line = int(match.group("old"))
            new_line = int(match.group("new"))
            continue
        if old_line is None or new_line is None or current_file is None or raw.startswith("\\"):
            continue
        if raw.startswith("+"):
            records.append({"file": current_file, "change": "added", "line": new_line, "content": raw[1:]})
            new_line += 1
        elif raw.startswith("-"):
            records.append({"file": current_file, "change": "removed", "line": old_line, "content": raw[1:]})
            old_line += 1
        else:
            old_line += 1
            new_line += 1
    return records
