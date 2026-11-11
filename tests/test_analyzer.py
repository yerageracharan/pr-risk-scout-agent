from pr_risk_scout.analyzer import analyze_diff, render_markdown
from pr_risk_scout.parser import parse_unified_diff

def patch(path, body):
    return f"--- a/{path}\n+++ b/{path}\n@@ -1,1 +1,2 @@\n keep_line = True\n{body}\n"

def test_parser_preserves_added_and_removed_lines():
    diff = """--- a/app/auth.py
+++ b/app/auth.py
@@ -10,1 +10,1 @@
-old_check = user.is_admin
+new_check = user.has_access
"""
    rows = parse_unified_diff(diff)
    assert [(r["change"], r["line"]) for r in rows] == [("removed", 10), ("added", 10)]

def test_detects_auth_permission_change():
    assert "AUTH_PERMISSION_CHANGE" in analyze_diff(patch("app/auth.py", "+    if user.has_access:"))["rule_counts"]

def test_detects_database_migration():
    assert "DATABASE_MIGRATION" in analyze_diff(patch("migrations/004.sql", "+ALTER TABLE users DROP COLUMN legacy_id;"))["rule_counts"]

def test_detects_tls_change():
    assert "TLS_SECURITY_CHANGE" in analyze_diff(patch("src/ssl_adapter.py", "+conn.cert_reqs = CERT_NONE"))["rule_counts"]

def test_detects_dependency_manifest():
    assert "DEPENDENCY_CHANGE" in analyze_diff(patch("requirements.txt", "+requests==2.32.0"))["rule_counts"]

def test_detects_github_actions_update():
    report = analyze_diff(patch(".github/workflows/test.yml", "+      uses: actions/setup-python@v5"))
    assert {"CI_WORKFLOW_CHANGE", "DEPENDENCY_CHANGE"} <= set(report["rule_counts"])

def test_detects_python_runtime_policy():
    assert "RUNTIME_COMPATIBILITY" in analyze_diff(patch("pyproject.toml", '+requires-python = ">=3.12"'))["rule_counts"]

def test_detects_cache_correctness_signal():
    assert "CACHE_CORRECTNESS" in analyze_diff(patch("src/_schema_cache.py", "+field_cache[key] = template.copy()"))["rule_counts"]

def test_detects_schema_generation_signal():
    assert "SCHEMA_GENERATION" in analyze_diff(patch("src/schema.py", "+def build_union_schema(annotation):"))["rule_counts"]

def test_detects_timing_signal():
    assert "TIMING_BEHAVIOR" in analyze_diff(patch("src/timing.py", "+elapsed = time.perf_counter() - start"))["rule_counts"]

def test_detects_type_checker_signal():
    assert "TYPE_CHECKING_CHANGE" in analyze_diff(patch("src/diagnostic.py", "+if method_is_final and is_override:"))["rule_counts"]

def test_detects_parser_syntax_signal():
    assert "PARSER_SYNTAX_CHANGE" in analyze_diff(patch("src/parser/semantic_errors.py", '+if attr == "__debug__":'))["rule_counts"]

def test_detects_test_surface():
    assert "TEST_SURFACE_CHANGE" in analyze_diff(patch("tests/test_auth.py", "+def test_denies_guest_access():"))["rule_counts"]

def test_detects_secret_only_on_added_line():
    report = analyze_diff(patch("config.py", '+API_KEY = "ghp_abcdefghijklmnopqrstuvwxyz123456"'))
    assert "SECRET_EXPOSURE" in report["rule_counts"]

def test_does_not_flag_removed_secret_as_new_exposure():
    diff = """--- a/config.py
+++ b/config.py
@@ -1,1 +1,1 @@
-API_KEY = "ghp_abcdefghijklmnopqrstuvwxyz123456"
+API_KEY = os.environ["API_KEY"]
"""
    assert "SECRET_EXPOSURE" not in analyze_diff(diff)["rule_counts"]

def test_detects_dangerous_execution():
    assert "DANGEROUS_EXECUTION" in analyze_diff(patch("app/run.py", "+eval(user_input)"))["rule_counts"]

def test_report_contains_traceable_evidence():
    report = analyze_diff(patch("app/auth.py", "+    if user.has_access:"))
    finding = report["findings"][0]
    assert (finding["file"], finding["line"], finding["evidence"]) == ("app/auth.py", 2, "if user.has_access:")

def test_markdown_report_is_human_readable():
    markdown = render_markdown(analyze_diff(patch("app/auth.py", "+    if user.has_access:")))
    assert "Review question" in markdown and "does not prove safety" in markdown

def test_empty_diff_is_not_declared_safe():
    report = analyze_diff("")
    assert report["summary"]["review_signals"] == 0
    assert "does not prove safety" in report["disclaimer"]

def test_detects_error_handling_change():
    assert "ERROR_HANDLING_CHANGE" in analyze_diff(patch("src/errors.py", "+raise ExceptionGroup(message, errors)"))["rule_counts"]

def test_detects_serialization_change():
    assert "SERIALIZATION_CHANGE" in analyze_diff(patch("src/loader.py", "+data = pickle.loads(payload)"))["rule_counts"]
