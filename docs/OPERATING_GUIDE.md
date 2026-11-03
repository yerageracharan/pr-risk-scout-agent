# Operating guide

## Local diff mode

Use this when you already have a patch file.

~~~powershell
python -m pr_risk_scout --diff examples/sample.diff --format both --out reports/sample
~~~

The command creates JSON for other tools and Markdown for a person.

## GitHub mode

~~~powershell
$env:GITHUB_TOKEN="github_pat_read_only_value"
python -m pr_risk_scout --repo pallets/flask --pr 6168 --format both --out reports/flask-6168
~~~

Use a fine-grained token with read-only permissions. For public repositories, try without a token first.

## Understanding severity

- Critical: a newly added line matches a high-confidence credential pattern.
- High: a signal involving access control, database migration, TLS, or dangerous execution.
- Medium: an area that often deserves review, such as dependencies, CI workflows, runtime support, caching, schemas, timing, type analysis, parser behaviour, public interfaces, error handling, or serialization.
- Low: a test surface changed.

Severity is a review-priority hint, not a probability of failure.

## When a rule fires

Open the linked PR. Navigate to the file and line. Read surrounding code, not just the changed line. Ask the question included in the report. If the flag is harmless, record why. If it reveals a real issue, use the project's normal review process.

## When no rule fires

Do not infer that the PR is safe. It may involve a rule that does not exist, a pattern the tool cannot recognise, or behaviour that depends on runtime context. Human review remains necessary.
