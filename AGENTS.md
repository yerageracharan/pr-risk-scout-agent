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

## Change ownership and proof

- Keep one authoritative owner for each domain rule and each persisted state. UI, CLI, MCP, and provider adapters translate inputs and outputs; they must not reimplement business policy or become competing sources of truth.
- Before changing a contract, trace the input through its owner to every consumer. Update callers, schemas, examples, docs, and regression tests together. Remove superseded paths unless a documented public-compatibility requirement keeps them.
- Keep optional external model/provider integrations behind adapters. Use injected or mocked adapters for deterministic unit tests; label live network/provider checks separately and never describe a mock as live verification.
- Validate untrusted user, model, file, and network data at the boundary. Preserve the product's evidence/provenance rules and reject malformed inputs rather than silently inventing defaults.
- Verify the supported user entry point and at least one relevant failure path. Report exact commands and results; CI on a different commit SHA is not proof for the current change.
- Keep the root README as the user entry point, `docs/README.md` as the documentation map, and focused guides as the owners of detailed contracts. Update links when files move. Do not hand-edit generated output when a source or generator owns it.


## Repository automation rules

- Treat files under `.github/workflows/` as production code. When changing a workflow, inspect the triggered run for the exact commit SHA; a prior green run is not proof for a newer commit.
- Pin third-party GitHub Actions to full 40-character commit SHAs and keep the upstream release tag in a trailing comment. Do not replace a pinned SHA with a floating major-version tag.
- Use the least-privilege `permissions` block. Default to read-only; grant write access only to the specific job that must publish or commit generated output.
- Give every job a finite `timeout-minutes`. Add a clear `concurrency` group for expensive or supersedable work; cancel stale pull-request runs, but do not cancel workflows whose purpose is to publish a completed artifact or evidence.
- Keep workflow logs and uploaded artifacts free of secrets and personal data. Set retention to the shortest period that still serves the evaluation or debugging purpose.
- Rely on the existing Dependabot configuration for action updates, then review release notes and run the affected workflow before considering the update complete.
