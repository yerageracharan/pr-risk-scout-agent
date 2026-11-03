from collections import Counter
from .parser import parse_unified_diff

RULES = [
    ("AUTH_PERMISSION_CHANGE", "high",
     ("auth", "permission", "authorize", "authentication", "is_admin", "role", "access_control"),
     "Authentication or permission-related code changed.",
     "Does this preserve intended access checks for every affected role?"),
    ("DATABASE_MIGRATION", "high",
     ("migration", "alter table", "drop table", "drop column", "schema", "alembic", "django.db.migrations"),
     "Database schema or migration-related code changed.",
     "Is this safe for existing data and deployment order?"),
    ("PUBLIC_API_CHANGE", "medium",
     ("api/", "/api", "endpoint", "route", "openapi", "swagger", "router"),
     "API or interface-related code changed.",
     "Could existing clients depend on the previous contract?"),
    ("DEPENDENCY_CHANGE", "medium",
     ("requirements.txt", "pyproject.toml", "poetry.lock", "uv.lock", "package-lock.json", "package.json", "pom.xml", "cargo.toml"),
     "A dependency manifest or lockfile changed.",
     "Are compatibility and release notes understood?"),
    ("TEST_CHANGE", "medium",
     ("test", "spec", "pytest", "unittest"),
     "Test-related code changed.",
     "Do tests still cover changed behaviour and failure cases?"),
]

def analyze_diff(diff_text, source="local diff"):
    changed = parse_unified_diff(diff_text)
    findings, seen = [], set()
    for item in changed:
        haystack = (item["file"] + " " + item["content"]).lower()
        for rule_id, severity, terms, reason, question in RULES:
            match = next((term for term in terms if term in haystack), None)
            key = (rule_id, item["file"], item["line"])
            if match and key not in seen:
                seen.add(key)
                findings.append({
                    "rule_id": rule_id,
                    "severity": severity,
                    "file": item["file"],
                    "line": item["line"],
                    "evidence": item["content"].strip()[:240],
                    "matched_signal": match,
                    "why_it_matters": reason,
                    "review_question": question,
                })
    counts = Counter(f["severity"] for f in findings)
    return {
        "project": "PR Risk Scout Agent",
        "source": source,
        "mode": "read-only heuristic analysis",
        "summary": {
            "changed_lines_inspected": len(changed),
            "review_signals": len(findings),
            "high": counts["high"],
            "medium": counts["medium"],
        },
        "findings": findings,
        "disclaimer": "Signals are heuristic prompts for human review, not proof of defects or vulnerabilities.",
    }

def render_markdown(report):
    summary = report["summary"]
    lines = [
        "# PR Risk Scout Report", "",
        f"**Source:** {report['source']}  ",
        f"**Mode:** {report['mode']}", "",
        "## Summary", "",
        f"- Changed lines inspected: {summary['changed_lines_inspected']}",
        f"- Review signals: {summary['review_signals']}",
        f"- High: {summary['high']} | Medium: {summary['medium']}", "",
        "## Findings", "",
    ]
    if not report["findings"]:
        lines.append("No configured signals detected. This does not prove the PR is safe.")
    for finding in report["findings"]:
        lines += [
            f"### [{finding['severity'].upper()}] {finding['rule_id']}",
            f"- **Location:** `{finding['file']}:{finding['line']}`",
            f"- **Evidence:** `{finding['evidence']}`",
            f"- **Why it matters:** {finding['why_it_matters']}",
            f"- **Review question:** {finding['review_question']}", "",
        ]
    lines += ["---", f"> {report['disclaimer']}", ""]
    return "\n".join(lines)
