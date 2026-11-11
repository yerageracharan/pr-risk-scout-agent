# Documentation map

The [project README](../README.md) is the canonical entry point for installing PR Risk Scout, analysing a unified diff, interpreting review signals, and understanding the limits of rule-based risk detection.

## Architecture and operating guides

- [Architecture](ARCHITECTURE.md) — diff parsing, risk rules, evidence records, scoring, and report generation.
- [Step-by-step guide](STEP_BY_STEP.md) — run the tool from a local diff to a review report.
- [Operating guide](OPERATING_GUIDE.md) — practical usage and interpretation.
- [FAQ](FAQ.md) — common questions and known behavior.
- [Threat model](THREAT_MODEL.md) — what the tool can detect, trust assumptions, and what it does not prove.

## Benchmarks and evaluation

- [Benchmark methodology](BENCHMARK_METHOD.md) — how pinned public pull requests are selected and how results should be interpreted.
- [Benchmark runner](../benchmarks/) — scripts and fixtures for the repeatable public-PR evaluation.
- [Automated tests](../tests/) — parser, classification rules, evidence traceability, and report regressions.

## Code ownership map

- `pr_risk_scout/parser.py` — unified-diff parsing, path normalisation, and line-number tracking.
- `pr_risk_scout/analyzer.py` — explainable risk rules and evidence-linked findings.
- `pr_risk_scout/` — report formatting, CLI, and application entry points.
- `benchmarks/` — reproducible fixtures and public-PR evaluation.

## Repository governance

- [Contribution workflow](../CONTRIBUTING.md)
- [AI coding-agent instructions](../AGENTS.md)
- [Security policy](../SECURITY.md)
- [Issue forms and PR template](../.github/)

A risk finding is a prompt for human review, not proof of a defect. A clean report does not prove that a pull request is safe.
