# Benchmark method and caveats

## What this benchmark is

The case study uses nine merged public pull requests across Flask, Requests, Pydantic, pytest, and Ruff. They exercise review areas including CI action versions, Python support, TLS setup, schema caching, model schema generation, timing internals, type analysis, and parser syntax.

Each case is pinned to its head commit. The runner checks the current PR head before downloading a diff. If it has changed, the run stops rather than silently testing different source.

## What the labels mean

Expected categories are human-assigned review-focus labels. They answer: "What area should a reviewer pay attention to in this PR?" They do not mean a defect exists or that maintainers made a mistake.

## Metrics

- Focus-label coverage: the share of selected focus labels surfaced by the configured rules.
- Case hit rate: the share of PRs where at least one expected focus area was surfaced.
- Additional signals: rules triggered outside the expected focus labels. They need review; they are not automatically false positives.

We do not report precision, recall, F1, or accuracy because this small sample does not have exhaustive, independently adjudicated, line-level ground truth.

## Reproduction

~~~bash
pip install -r requirements.txt
python -m benchmarks.run_real_benchmark
~~~

Set GITHUB_TOKEN only when needed to avoid public API rate limits. The benchmark is read-only.

## Limitations

Nine PRs are too few to generalise to all languages, repository sizes, teams, or change types. The sample is Python/open-source biased. It is an engineering case study and a starting point, not scientific validation.
