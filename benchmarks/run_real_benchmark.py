"""Run a pinned case study over real public GitHub PR diffs."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests
from pr_risk_scout.analyzer import analyze_diff

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "real_pr_cases.json"
OUTPUT_PATH = ROOT / "benchmarks" / "results" / "real_pr_benchmark.json"

def headers(token, accept):
    value = {"Accept":accept,"X-GitHub-Api-Version":"2022-11-28","User-Agent":"pr-risk-scout-agent-benchmark"}
    if token:
        value["Authorization"] = f"Bearer {token}"
    return value

def main():
    manifest=json.loads(CASES_PATH.read_text(encoding="utf-8"))
    token=os.getenv("GITHUB_TOKEN")
    results=[]
    expected_total=matched_total=case_hits=0
    for case in manifest["cases"]:
        root=f"https://api.github.com/repos/{case['repo']}/pulls/{case['number']}"
        meta=requests.get(root,headers=headers(token,"application/vnd.github+json"),timeout=45)
        meta.raise_for_status()
        current_head=meta.json()["head"]["sha"]
        if current_head != case["head_sha"]:
            raise RuntimeError(f"PR head changed for {case['url']}: expected {case['head_sha']}, got {current_head}")
        response=requests.get(root,headers=headers(token,"application/vnd.github.v3.diff"),timeout=45)
        response.raise_for_status()
        report=analyze_diff(response.text,source=case["url"])
        detected=set(report["rule_counts"])
        expected=set(case["expected_categories"])
        matched=sorted(detected & expected)
        missed=sorted(expected - detected)
        extra=sorted(detected - expected)
        expected_total += len(expected)
        matched_total += len(matched)
        case_hits += bool(matched)
        results.append({
            "repo":case["repo"],"number":case["number"],"title":case["title"],"url":case["url"],
            "head_sha":current_head,"expected_categories":sorted(expected),"detected_categories":sorted(detected),
            "matched_categories":matched,"missed_categories":missed,"additional_signals":extra,
            "files_changed_expected_from_github":case["changed_files"],
            "changed_lines_inspected":report["summary"]["changed_lines_inspected"],
            "review_signals":report["summary"]["review_signals"]
        })
    result={
        "title":manifest["title"],"method":manifest["method"],
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),"case_count":len(results),
        "expected_focus_labels":expected_total,"matched_focus_labels":matched_total,
        "focus_label_coverage":round(matched_total/expected_total,4) if expected_total else 0,
        "cases_with_any_expected_signal":case_hits,
        "case_hit_rate":round(case_hits/len(results),4) if results else 0,
        "results":results,
        "interpretation":"Focus-label coverage measures whether configured rules surfaced manually labelled review areas in this small sample. Additional signals are not automatically false positives. This is not precision, recall, F1, security certification, or a representative estimate of production performance."
    }
    OUTPUT_PATH.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
