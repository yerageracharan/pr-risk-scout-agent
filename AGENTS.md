# Agent Instructions

These instructions apply across PR Risk Scout.

## Product invariants

- Risk findings are review signals, not proof of defects, vulnerabilities, or unsafe changes.
- Preserve exact file paths, changed-line numbers, and evidence text so every finding is traceable to the supplied diff.
- Do not approve, reject, comment on, label, assign, or merge pull requests; the tool is advisory and read-only.
- Secret patterns are possible exposures, not proof that a credential is live. Never echo or commit real secret values.
- Parse unified-diff hunk counts and file paths defensively; malformed or oversized diffs must fail clearly.

## Repository map

- `pr_risk_scout/parser.py`: unified-diff parsing and changed-line locations.
- `pr_risk_scout/analyzer.py`: deterministic risk rules, aggregation, and report generation.
- `benchmarks/`: pinned public-PR evaluation inputs and methodology.
- `tests/`: parser, rule, and report regression tests.
- `docs/`: architecture, threat model, operating guide, and benchmark method.

## Working rules

- Read the threat model and benchmark methodology before altering a rule or its severity.
- Add negative tests for false positives, not only positive detector examples.
- Keep path and line evidence exact; do not silently drop malformed hunks.
- Treat input diffs as untrusted data and enforce size/path boundaries.
- Do not turn a signal into a claim that a PR is insecure or defective.
- The benchmark must use pinned commits and documented expected review-focus categories.

## Validation

```bash
python -m pytest -q
python -m compileall -q pr_risk_scout benchmarks
python -m pr_risk_scout --help
```
