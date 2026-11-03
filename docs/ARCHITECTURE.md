# Architecture, in plain English

PR Risk Scout reads the patch attached to a pull request. A patch is Git's description of the lines that were added and removed. The parser keeps the file name, change direction, line number, and changed text. The rule engine checks those changed lines against a set of small, understandable patterns.

When a rule matches, the program creates a finding. A finding tells the reviewer what matched, where it matched, why the area may matter, and what question to investigate.

## Components

1. GitHub client — retrieves a pull-request diff with an HTTP GET request.
2. Diff parser — converts patch text into structured changed-line records.
3. Rule engine — evaluates file paths and changed-line content.
4. Finding formatter — creates Markdown and JSON.
5. Benchmark runner — compares findings with manually labelled focus areas in real public PRs.

## Why path and text are both used

The word "cache" can appear in documentation, tests, or the implementation. The file path gives context. The changed line gives evidence. Both are useful, but this is still a heuristic: it does not build a complete model of the program.

## Why an LLM is not in the critical path

The first version uses deterministic rules. That makes it easier to reproduce why a flag appeared and write a test for it. A future language-model explanation layer could summarise findings, but it must cite supplied evidence and must not invent code facts.

## Security boundary

The GitHub client uses GET requests only. It does not approve, merge, assign, label, comment, or push code. Use a read-only token and keep it in an environment variable. Never commit tokens.
