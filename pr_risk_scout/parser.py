import re

def parse_unified_diff(diff_text):
    changed, current_file, new_line = [], None, None
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            current_file = None if path == "/dev/null" else path.removeprefix("b/")
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            new_line = int(match.group(1)) if match else None
        elif line.startswith("+") and not line.startswith("+++"):
            if current_file and new_line is not None:
                changed.append({"file": current_file, "line": new_line, "content": line[1:]})
                new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue
        elif not line.startswith("\\") and new_line is not None:
            new_line += 1
    return changed
