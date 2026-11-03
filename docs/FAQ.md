# Frequently asked questions

### Is this an AI agent or a static analyser?
The current version is a deterministic, rule-based PR review assistant. It is part of an AI-agent learning challenge, but this MVP does not call an LLM. Starting with explicit rules makes the behaviour inspectable and testable.

### Does it find every security bug?
No. It flags selected review patterns. It is not a full static analyser, SAST platform, dependency scanner, or penetration test.

### Does it approve or merge PRs?
No. It is read-only.

### Why does it sometimes flag harmless changes?
A keyword or path may match even when the change is safe. Read the evidence and surrounding code.

### Why might it miss something?
The rule set is finite. It does not understand every language, data flow, runtime condition, or repository convention.

### Can it scan private repositories?
Yes, with a read-only GitHub token passed through the environment variable. Never place a token in source code or reports.

### Do benchmark results prove production accuracy?
No. The case study has nine PRs and manual review-focus labels. It is a useful engineering check, not a statistically representative evaluation.
