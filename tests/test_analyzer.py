from pr_risk_scout.analyzer import analyze_diff

SAMPLE = """diff --git a/app/auth.py b/app/auth.py
--- a/app/auth.py
+++ b/app/auth.py
@@ -1,1 +1,2 @@
 def can_view(user):
+    return True
diff --git a/migrations/001.sql b/migrations/001.sql
--- /dev/null
+++ b/migrations/001.sql
@@ -0,0 +1 @@
+ALTER TABLE users DROP COLUMN old_name
diff --git a/requirements.txt b/requirements.txt
--- a/requirements.txt
+++ b/requirements.txt
@@ -1,1 +1,1 @@
+requests==2.31
"""

def test_detects_auth_migration_dependency():
    rule_ids = {finding["rule_id"] for finding in analyze_diff(SAMPLE)["findings"]}
    assert {"AUTH_PERMISSION_CHANGE", "DATABASE_MIGRATION", "DEPENDENCY_CHANGE"} <= rule_ids

def test_read_only_disclaimer():
    assert "not proof" in analyze_diff(SAMPLE)["disclaimer"]
