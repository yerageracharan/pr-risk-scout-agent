# PR Risk Scout Agent

A read-only GitHub pull-request review assistant. It scans a PR diff and flags changes worth a closer human review.

**It never approves, rejects, comments on, or merges pull requests.** Findings are heuristic signals, not proof of defects.

## Quick start (Python 3.10+)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt pytest
python -m pr_risk_scout --diff examples/sample.diff --format both --out reports/sample
```

## Scan a public or private GitHub PR

Create a GitHub token with read-only access to repository contents and pull requests, then:

```powershell
$env:GITHUB_TOKEN="YOUR_TOKEN"
python -m pr_risk_scout --repo owner/repository --pr 123 --format both --out reports/pr-123
```

The tool uses GitHub GET requests only. Public repositories can be scanned without a token, subject to rate limits.

## What it flags

- Authentication and permission-related changes
- Database migrations and schema changes
- API/interface changes
- Dependency manifests and lockfiles
- Test-related changes

Each finding includes severity, file, changed line, matched signal, evidence, why it matters, and a reviewer question.

## Run the tests

```powershell
python -m pytest -q
```

GitHub Actions runs the test suite on Python 3.10, 3.11, and 3.12.

## Limitations

Pattern matching can produce false positives and miss issues. It does not execute code, understand runtime context, or prove a PR is safe. Always review findings manually.

## Roadmap

- Language-aware rules and configurable policies
- SARIF output
- GitHub Actions integration
- Evaluation against labelled PR examples

MIT licensed.
