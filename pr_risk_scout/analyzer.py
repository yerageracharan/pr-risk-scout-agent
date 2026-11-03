"""Explainable PR risk signals. Rules prompt review; they do not prove defects."""
from __future__ import annotations
from collections import Counter
import re
from .parser import parse_unified_diff

RULES = [
    {"id":"AUTH_PERMISSION_CHANGE","severity":"high","path":r"(^|/)(auth|security|permissions?|access)(/|_|\.|$)|session","text":r"\b(authoriz|authentication|permission|is_admin|access_token|csrf|rbac|acl)\b","why":"Authentication, session, or permission-related code changed.","question":"Do all affected users still receive only the access they are entitled to?"},
    {"id":"DATABASE_MIGRATION","severity":"high","path":r"(^|/)(migrations?|alembic|schema)(/|_|\.|$)|\.sql$","text":r"\b(drop table|drop column|truncate|alter table|foreign key|cascade|migration)\b","why":"Database structure or migration behaviour changed.","question":"Is this safe for existing data, rollback, and deployment order?"},
    {"id":"TLS_SECURITY_CHANGE","severity":"high","path":r"(ssl|tls|cert|certificate)","text":r"\b(ssl_context|tls|certificate|cert_reqs|ca_certs|verify\s*=\s*false|cert_none|check_hostname)\b","why":"TLS or certificate-verification behaviour changed.","question":"Does the new behaviour preserve certificate verification and the intended trust store?"},
    {"id":"SECRET_EXPOSURE","severity":"critical","path":r"(?!)","text":r"(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_/\-+=]{12,}['\"])","why":"A newly added line resembles a hard-coded credential.","question":"Is this a real credential? Remove it from history and rotate it if exposed.","added_only":True},
    {"id":"DANGEROUS_EXECUTION","severity":"high","path":r"(?!)","text":r"\b(eval|exec)\s*\(|\bos\.system\s*\(|shell\s*=\s*true","why":"Dynamic execution or shell invocation changed.","question":"Can untrusted input reach this path, and is the command safely parameterised?","added_only":True},
    {"id":"DEPENDENCY_CHANGE","severity":"medium","path":r"(^|/)(requirements([.-].*)?\.txt|poetry\.lock|uv\.lock|pdm\.lock|package(-lock)?\.json|cargo\.toml|go\.sum|go\.mod|pom\.xml|gemfile(\.lock)?)$","text":r"\b(dependencies|dependency|requirements|lockfile)\b|uses:\s*|actions/","why":"A package or CI action dependency changed.","question":"Do the version, transitive dependencies, provenance, and release notes make sense?"},
    {"id":"CI_WORKFLOW_CHANGE","severity":"medium","path":r"(^|/)(\.github/workflows|\.circleci|\.buildkite|azure-pipelines|\.gitlab-ci)","text":r"(uses:|actions/|matrix:|permissions:|runs-on:)","why":"Build or automation workflow behaviour changed.","question":"Does this preserve least-privilege permissions, pinned actions, and the intended test matrix?"},
    {"id":"RUNTIME_COMPATIBILITY","severity":"medium","path":r"(?!)","text":r"(requires-python|python[_-]version\s*[:=]|python\s*:\s*['\"]?3\.\d|py3\.\d|drop support for python|Programming Language :: Python :: 3)","why":"Supported runtime or interpreter test matrix changed.","question":"Are support policy, package metadata, docs, CI matrix, and compatibility tests aligned?"},
    {"id":"CACHE_CORRECTNESS","severity":"medium","path":r"(cache|memoiz)","text":r"\b(cache|memoiz|cached|template|lru_cache|cache_key)\b","why":"Caching or reuse of computed objects changed.","question":"Can cached values become stale, be mutated, or leak state between instances?"},
    {"id":"SCHEMA_GENERATION","severity":"medium","path":r"(schema|_fields|model_construction|typing_extra)","text":r"\b(schema|annotation|field_info|union|serializer|validator|type_adapter)\b","why":"Schema, annotation, or model-construction behaviour changed.","question":"Do unions, forward references, defaults, and custom hooks still behave correctly?"},
    {"id":"TIMING_BEHAVIOR","severity":"medium","path":r"(timing|runner|subtests)","text":r"\b(perf_counter|monotonic|duration|time\.time|instant|start|stop)\b","why":"Timing measurement or duration representation changed.","question":"Are clock mocking, monotonic elapsed time, zero values, and plugin compatibility handled?"},
    {"id":"TYPE_CHECKING_CHANGE","severity":"medium","path":r"(diagnostic|semantic|ty/|static_class)","text":r"\b(final|override|decorator)\b|is_function_def|static_class_literal","why":"Static type-checking or decorator-related analysis changed.","question":"Do inheritance, decorators, aliases, and autofix boundaries remain correct?"},
    {"id":"PARSER_SYNTAX_CHANGE","severity":"medium","path":r"(parser|syntax|semantic_errors|ast)","text":r"\b(__debug__|augassign|syntax|ast|semantic_errors|target-version)\b","why":"Parsing or syntax-diagnostic behaviour changed.","question":"Are supported language versions and syntactic contexts covered by fixtures?"},
    {"id":"TEST_SURFACE_CHANGE","severity":"low","path":r"(^|/)(tests?|testing)(/|_)|(^|/)(test_[^/]+|[^/]+_test\.py)|\.snap$","text":r"\b(test|pytest|fixture|snapshot|assert)\b","why":"A test, fixture, or expected-output surface changed.","question":"Does the test exercise the intended regression rather than just restating implementation?"},
    {"id":"PUBLIC_API_CHANGE","severity":"medium","path":r"(openapi|swagger|(^|/)api(/|_)|routes?|endpoints?)","text":r"\b(endpoint|response_model|request_model|openapi|swagger|public_api)\b","why":"A public interface or endpoint contract may have changed.","question":"Could an existing client rely on the old name, type, status code, or response shape?"},
    {"id":"ERROR_HANDLING_CHANGE","severity":"medium","path":r"(?!)","text":r"\b(try:|except\b|raise\b|BaseExceptionGroup|ExceptionGroup|fallback)\b","why":"Error propagation or fallback behaviour changed.","question":"Are expected errors preserved, unexpected errors visible, and cleanup paths safe?"},
    {"id":"SERIALIZATION_CHANGE","severity":"medium","path":r"(?!)","text":r"\b(pickle|yaml\.load|json\.loads|deserialize|serializer|encoding)\b","why":"Serialization or deserialization behaviour changed.","question":"Can untrusted or old data be decoded safely, and is backward compatibility preserved?"},
]

def analyze_diff(diff_text: str, source: str = "local diff", file_path: str | None = None) -> dict:
    changed = parse_unified_diff(diff_text, file_path=file_path)
    findings, seen = [], set()
    for record in changed:
        path = record["file"].lower()
        content = record["content"].strip()
        for rule in RULES:
            if rule.get("added_only") and record["change"] != "added":
                continue
            path_match = bool(re.search(rule["path"], path, flags=re.I))
            content_match = bool(re.search(rule["text"], content, flags=re.I))
            if not (path_match or content_match):
                continue
            if rule["id"] in {"SECRET_EXPOSURE","DANGEROUS_EXECUTION","ERROR_HANDLING_CHANGE","SERIALIZATION_CHANGE","RUNTIME_COMPATIBILITY"} and not content_match:
                continue
            if rule["id"] == "SECRET_EXPOSURE" and not content_match:
                continue
            key = (rule["id"], record["file"])
            if key in seen:
                continue
            seen.add(key)
            findings.append({
                "rule_id":rule["id"],"severity":rule["severity"],"file":record["file"],
                "line":record["line"],"change":record["change"],"evidence":content[:260],
                "why_it_matters":rule["why"],"review_question":rule["question"],
            })
    counts = Counter(item["severity"] for item in findings)
    by_rule = Counter(item["rule_id"] for item in findings)
    return {
        "project":"PR Risk Scout Agent","source":source,"mode":"read-only heuristic analysis",
        "summary":{"changed_lines_inspected":len(changed),"files_with_changes":len({x["file"] for x in changed}),
                   "review_signals":len(findings),"critical":counts["critical"],"high":counts["high"],
                   "medium":counts["medium"],"low":counts["low"]},
        "rule_counts":dict(sorted(by_rule.items())),"findings":findings,
        "disclaimer":"Signals are heuristic prompts for human review, not proof of defects, vulnerabilities, or production impact. A clean report does not prove safety."
    }

def render_markdown(report: dict) -> str:
    s=report["summary"]
    lines=["# PR Risk Scout Report","",f"Source: {report['source']}  ",f"Mode: {report['mode']}","","## Summary","",
           f"- Files with changes: {s['files_with_changes']}",f"- Changed lines inspected: {s['changed_lines_inspected']}",
           f"- Review signals: {s['review_signals']}",f"- Critical: {s['critical']} | High: {s['high']} | Medium: {s['medium']} | Low: {s['low']}","","## Findings",""]
    if not report["findings"]:
        lines.append("No configured review signals were detected. This does not prove the PR is safe.")
    for item in report["findings"]:
        lines += [f"### [{item['severity'].upper()}] {item['rule_id']}",
                  f"- Location: {item['file']}:{item['line']} ({item['change']})",
                  f"- Evidence: {item['evidence']}",f"- Why it matters: {item['why_it_matters']}",
                  f"- Review question: {item['review_question']}",""]
    lines += ["---",f"> {report['disclaimer']}",""]
    return "\n".join(lines)
