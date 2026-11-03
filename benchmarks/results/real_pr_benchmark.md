# Real-public-PR case study

<small>Benchmark run: 4 November 2026 · 9 merged pull requests · 5 public repositories</small>

## Result

| Measure | Result |
|---|---:|
| Pull requests analysed | 9 |
| Expected review-focus labels | 18 |
| Labels surfaced | 18 |
| Focus-label coverage | **100% (18/18)** |
| Cases with at least one expected signal | **9/9 (100%)** |
| Missed expected focus labels | 0 |

**Interpretation matters:** this is a small, manually labelled focus-area coverage exercise. It is not accuracy, precision, recall, F1, or proof that the tool finds all defects. The nine cases were selected to exercise known areas and labels were assigned after inspecting their public titles, metadata, and patches.

## Case-by-case results

| Public repository / PR | Expected focus areas | Matched | Other signals |
|---|---|---|---|
| [pallets/flask #6168](https://github.com/pallets/flask/pull/6168) | CI_WORKFLOW_CHANGE, RUNTIME_COMPATIBILITY, TEST_SURFACE_CHANGE | 3/3 | ERROR_HANDLING_CHANGE |
| [psf/requests #7636](https://github.com/psf/requests/pull/7636) | CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE | 2/2 | None |
| [psf/requests #6767](https://github.com/psf/requests/pull/6767) | TLS_SECURITY_CHANGE | 1/1 | ERROR_HANDLING_CHANGE |
| [pydantic/pydantic #13544](https://github.com/pydantic/pydantic/pull/13544) | CACHE_CORRECTNESS, SCHEMA_GENERATION, TEST_SURFACE_CHANGE | 3/3 | ERROR_HANDLING_CHANGE, SERIALIZATION_CHANGE, TIMING_BEHAVIOR, TYPE_CHECKING_CHANGE |
| [pydantic/pydantic #14138](https://github.com/pydantic/pydantic/pull/14138) | SCHEMA_GENERATION, TEST_SURFACE_CHANGE | 2/2 | ERROR_HANDLING_CHANGE, SERIALIZATION_CHANGE |
| [pytest-dev/pytest #15309](https://github.com/pytest-dev/pytest/pull/15309) | CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE | 2/2 | None |
| [pytest-dev/pytest #15298](https://github.com/pytest-dev/pytest/pull/15298) | TIMING_BEHAVIOR, TEST_SURFACE_CHANGE | 2/2 | None |
| [astral-sh/ruff #29961](https://github.com/astral-sh/ruff/pull/29961) | TYPE_CHECKING_CHANGE | 1/1 | TEST_SURFACE_CHANGE |
| [astral-sh/ruff #27908](https://github.com/astral-sh/ruff/pull/27908) | PARSER_SYNTAX_CHANGE, TEST_SURFACE_CHANGE | 2/2 | TYPE_CHECKING_CHANGE |

## What was actually tested

### pallets/flask #6168 — drop support for Python 3.10

- Source: [https://github.com/pallets/flask/pull/6168](https://github.com/pallets/flask/pull/6168)
- Changed files: 12
- Changed lines parsed: 71
- Pinned head: `7689f98403e2c0b0bc8d1031e60f8cff2620e86a`
- Expected review focus: CI_WORKFLOW_CHANGE, RUNTIME_COMPATIBILITY, TEST_SURFACE_CHANGE
- Signals matched: CI_WORKFLOW_CHANGE, RUNTIME_COMPATIBILITY, TEST_SURFACE_CHANGE
- Additional signals to inspect: ERROR_HANDLING_CHANGE


### psf/requests #7636 — Bump the actions group with 4 updates

- Source: [https://github.com/psf/requests/pull/7636](https://github.com/psf/requests/pull/7636)
- Changed files: 2
- Changed lines parsed: 8
- Pinned head: `a7d2a5d259b74e97812c2db04acb34adf41ba22e`
- Expected review focus: CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE
- Signals matched: CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE
- Additional signals to inspect: None


### psf/requests #6767 — Revert caching a default SSLContext

- Source: [https://github.com/psf/requests/pull/6767](https://github.com/psf/requests/pull/6767)
- Changed files: 1
- Changed lines parsed: 55
- Pinned head: `11d68c17bcd66bd3e2c5137b0a7aad7f59967102`
- Expected review focus: TLS_SECURITY_CHANGE
- Signals matched: TLS_SECURITY_CHANGE
- Additional signals to inspect: ERROR_HANDLING_CHANGE


### pydantic/pydantic #13544 — Add fast paths for fields defined by a pure annotation and a simple default

- Source: [https://github.com/pydantic/pydantic/pull/13544](https://github.com/pydantic/pydantic/pull/13544)
- Changed files: 10
- Changed lines parsed: 1623
- Pinned head: `1f9b994fd700d9c8f3df18d181efa269c1b2a65a`
- Expected review focus: CACHE_CORRECTNESS, SCHEMA_GENERATION, TEST_SURFACE_CHANGE
- Signals matched: CACHE_CORRECTNESS, SCHEMA_GENERATION, TEST_SURFACE_CHANGE
- Additional signals to inspect: ERROR_HANDLING_CHANGE, SERIALIZATION_CHANGE, TIMING_BEHAVIOR, TYPE_CHECKING_CHANGE


### pydantic/pydantic #14138 — Construct builtin scalar union schemas directly

- Source: [https://github.com/pydantic/pydantic/pull/14138](https://github.com/pydantic/pydantic/pull/14138)
- Changed files: 2
- Changed lines parsed: 194
- Pinned head: `bb9a26c665a2acbfc120c2a0d1f22a8d88ec1fba`
- Expected review focus: SCHEMA_GENERATION, TEST_SURFACE_CHANGE
- Signals matched: SCHEMA_GENERATION, TEST_SURFACE_CHANGE
- Additional signals to inspect: ERROR_HANDLING_CHANGE, SERIALIZATION_CHANGE


### pytest-dev/pytest #15309 — Bump the github-actions group with 3 updates

- Source: [https://github.com/pytest-dev/pytest/pull/15309](https://github.com/pytest-dev/pytest/pull/15309)
- Changed files: 2
- Changed lines parsed: 8
- Pinned head: `2dba1ac121b91f974ac37b1f06eee68694259fd7`
- Expected review focus: CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE
- Signals matched: CI_WORKFLOW_CHANGE, DEPENDENCY_CHANGE
- Additional signals to inspect: None


### pytest-dev/pytest #15298 — Store a timing.Duration in CallInfo

- Source: [https://github.com/pytest-dev/pytest/pull/15298](https://github.com/pytest-dev/pytest/pull/15298)
- Changed files: 7
- Changed lines parsed: 168
- Pinned head: `fd356839cbe402940c46ef50256b41b5ad0eb612`
- Expected review focus: TIMING_BEHAVIOR, TEST_SURFACE_CHANGE
- Signals matched: TIMING_BEHAVIOR, TEST_SURFACE_CHANGE
- Additional signals to inspect: None


### astral-sh/ruff #29961 — Handle decorators that replace overrides of final methods

- Source: [https://github.com/astral-sh/ruff/pull/29961](https://github.com/astral-sh/ruff/pull/29961)
- Changed files: 2
- Changed lines parsed: 60
- Pinned head: `a72b0c7412af81b5c86e2cdbbf6f47ca9079d0b7`
- Expected review focus: TYPE_CHECKING_CHANGE
- Signals matched: TYPE_CHECKING_CHANGE
- Additional signals to inspect: TEST_SURFACE_CHANGE


### astral-sh/ruff #27908 — Extend __debug__ write check to attribute targets

- Source: [https://github.com/astral-sh/ruff/pull/27908](https://github.com/astral-sh/ruff/pull/27908)
- Changed files: 5
- Changed lines parsed: 480
- Pinned head: `c7c7df43fe1fb7f58873ab21f3cd9e03a65250b3`
- Expected review focus: PARSER_SYNTAX_CHANGE, TEST_SURFACE_CHANGE
- Signals matched: PARSER_SYNTAX_CHANGE, TEST_SURFACE_CHANGE
- Additional signals to inspect: TYPE_CHECKING_CHANGE



## Reproduction

```bash
pip install -r requirements.txt
python -m benchmarks.run_real_benchmark
```

The runner fetches public PR metadata and diffs with HTTP GET requests only. It verifies that each PR still points to the pinned head SHA; if a PR changes, the run stops rather than silently benchmarking different code.

## Limitations

Nine examples are too few to generalise across all languages, repositories, teams, or change types. The labels are review-focus labels, not a gold-standard classification of vulnerabilities or bugs. Additional signals are not automatically false positives. A later evaluation should sample PRs randomly, label findings independently with multiple reviewers, measure agreement, and report precision/recall with confidence intervals.
