# Build walkthrough for beginners

## Step 1 — Understand the problem

A pull request is a proposal to change a codebase. GitHub shows it as added and removed lines. Reviewers must understand not only whether the program still runs, but whether the change affects permissions, stored data, interfaces, dependencies, or tests.

PR Risk Scout is an extra pair of eyes. It does not make the decision.

## Step 2 — Understand the input

A unified diff is plain text. Lines beginning with + were added. Lines beginning with - were removed. Lines beginning with a space are context. A hunk header records where old and new line ranges begin.

Why keep deletions? Removing a permission check or a test may matter just as much as adding a new line.

## Step 3 — Parse before analysing

The parser turns patch text into small records. Each record contains a file name, a line number, the change direction, and the changed text. The analyser should use the parser's line number instead of guessing.

## Step 4 — Make rules explainable

Each rule has a name, severity, pattern, reason, and question for the reviewer. For example, a change to TLS verification should trigger a TLS review signal. The report should point to the changed line and ask whether certificate verification remains correct.

## Step 5 — Make output useful

A report that says "this PR is risky" is not useful. A report that identifies a line, a pattern, a reason, and a reviewer question is actionable.

## Step 6 — Test rules

Every rule needs a positive example and a boundary example. Parser tests should prove additions and deletions receive correct locations. A secret detector should not call a removed credential a newly introduced exposure. Tests should also protect the read-only promise.

## Step 7 — Try real pull requests

Synthetic examples are useful because expected behaviour is obvious. Real PRs are messy. They combine documentation, code, tests, and configuration. The benchmark demonstrates how rules behave on actual public patches.

## Step 8 — Read the caveats

A heuristic may miss a risk or flag a harmless change. A rule match is not proof that a bug exists. A scan with no findings is not a clean bill of health. Human review remains necessary.
