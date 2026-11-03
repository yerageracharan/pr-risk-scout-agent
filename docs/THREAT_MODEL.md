# Threat model

## What we are protecting

The tool reads source code and pull-request metadata. Main risks include credential exposure, over-broad tokens, false confidence from an empty report, and unsafe future features that write back to GitHub.

## Assets

- GitHub token, if configured.
- Repository source and PR metadata fetched for analysis.
- Local JSON and Markdown reports.
- Integrity of the human review decision.

## Trust boundaries

1. The user chooses a repository and pull request.
2. GitHub provides metadata and a diff.
3. The parser treats patch text as data, never executable code.
4. The rule engine produces suggestions.
5. A human reviewer makes the final decision.

## Controls in this version

- Read-only HTTP method: GET.
- No shell execution of patch content.
- No automatic comments, approvals, labels, merges, or branch updates.
- Secret-pattern checks apply to added lines.
- Findings include evidence for inspection.
- Tokens are read from GITHUB_TOKEN.
- Reports state that a clean scan does not prove safety.

## Known gaps

- Secret patterns cannot recognise every possible credential.
- A changed line can be dangerous only in combination with other code or runtime state.
- The tool does not model data flow, control flow, taint, dependency reachability, or deployment topology.
- A future LLM layer could hallucinate. It must cite input evidence and remain advisory.

## Safe operating guidance

Use a fine-grained token restricted to the repositories you need, with read-only Contents and Pull requests permissions. Prefer unauthenticated scans of public repositories where possible. Never execute code from a pull request during analysis. Treat reports as a review aid, not a security guarantee.
