import pytest

from pr_risk_scout.parser import normalise_path, parse_unified_diff


def test_normalise_path_strips_git_prefix():
    assert normalise_path("a/src/app.py") == "src/app.py"
    assert normalise_path("b/src/app.py") == "src/app.py"


@pytest.mark.parametrize("path", ["/etc/passwd", "../secret.txt", "a/../../secret", "C:\\Windows\\file.txt", ""])
def test_normalise_path_rejects_unsafe_paths(path):
    with pytest.raises((TypeError, ValueError)):
        normalise_path(path)


def test_parse_diff_enforces_hunk_line_counts():
    diff = """--- a/app.py
+++ b/app.py
@@ -1,1 +1,2 @@
 keep = True
+added = True
"""
    records = parse_unified_diff(diff)
    assert [(row["change"], row["line"]) for row in records] == [("added", 2)]


@pytest.mark.parametrize("diff, message", [
    ("--- a/app.py\n+++ b/app.py\n@@ -1,2 +1,2 @@\n-old\n+new\n", "ended before"),
    ("--- a/app.py\n+++ b/app.py\n@@ -1,0 +1,0 @@\n+extra\n", "more added"),
])
def test_parse_diff_rejects_inconsistent_hunk_counts(diff, message):
    with pytest.raises(ValueError, match=message):
        parse_unified_diff(diff)


def test_parse_diff_rejects_unsafe_file_header():
    with pytest.raises(ValueError, match="unsafe path"):
        parse_unified_diff("--- a/../../outside.py\n+++ b/../../outside.py\n@@ -1 +1 @@\n-a\n+b\n")


def test_parse_diff_rejects_non_string_and_oversized_input():
    with pytest.raises(TypeError, match="diff_text"):
        parse_unified_diff(None)
    with pytest.raises(ValueError, match="10 MB"):
        parse_unified_diff("x" * (10 * 1024 * 1024 + 1))
