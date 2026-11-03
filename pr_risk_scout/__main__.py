import argparse, json, os
from pathlib import Path
from .analyzer import analyze_diff, render_markdown
from .github_client import fetch_pull_request_diff

def main():
    p = argparse.ArgumentParser(description="Read-only GitHub PR risk scout")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--diff")
    src.add_argument("--repo", help="owner/name")
    p.add_argument("--pr", type=int)
    p.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    p.add_argument("--out", default="reports/pr-risk-report")
    a = p.parse_args()
    if a.repo:
        if not a.pr:
            p.error("--pr is required with --repo")
        diff = fetch_pull_request_diff(a.repo, a.pr, os.getenv("GITHUB_TOKEN"))
        source = f"https://github.com/{a.repo}/pull/{a.pr}"
    else:
        diff = Path(a.diff).read_text(encoding="utf-8", errors="replace")
        source = a.diff
    report = analyze_diff(diff, source)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.format in ("json", "both"):
        out.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print("Wrote", out.with_suffix(".json"))
    if a.format in ("markdown", "both"):
        out.with_suffix(".md").write_text(render_markdown(report), encoding="utf-8")
        print("Wrote", out.with_suffix(".md"))
    print(f"Found {len(report['findings'])} review signals.")

if __name__ == "__main__":
    main()
