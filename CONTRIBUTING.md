# Contributing

Thanks for improving PR Risk Scout. The goal is an explainable second set of eyes on pull-request diffs—not an automated reviewer that makes merge decisions.

## Before changing code

- Search existing issues and commits for overlapping work.
- Open an issue before adding a new risk rule, changing severity semantics, or expanding benchmark scope. Include the threat/review scenario, expected behavior, alternatives, and validation plan.
- For bugs, provide a small unified-diff fixture, expected finding, actual result, and exact test command.
- Keep rule changes, parser changes, benchmark-data changes, and documentation changes focused.

## Development setup

Python 3.10 or newer.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pytest
```

## Validation

```bash
python -m pytest -q
python -m compileall -q pr_risk_scout benchmarks
python -m pr_risk_scout --help
```

For parser changes, cover file headers, /dev/null paths, additions/deletions, context lines, hunk counts, malformed headers, multiple files, and oversized input. For rule changes, add positive and negative examples and keep stable rule IDs.

## Engineering expectations

- Findings must include a reason, review question, file, line, and evidence where available.
- Severity is a prioritization hint, not a security verdict.
- Never include live credentials in tests, examples, logs, or screenshots.
- Keep GitHub access read-only and do not add merge/approval automation.
- Update benchmark methodology and docs when the rule set or expected categories change.

## Pull requests

Use the repository PR template. Include problem, user impact, focused tests and results, and known false positives/negatives. Link an issue for non-trivial changes.

## Security

Use [SECURITY.md](SECURITY.md) for private vulnerability disclosure. Avoid publishing working credentials or exploit details in public issues.
