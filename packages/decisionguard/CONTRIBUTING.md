# Contributing

Keep DecisionGuard focused on applying current project decisions, reviewing changes
and carrying confirmed context into the next task. New connectors
should implement the capability contract in `skills/decisionguard/references/notion.md` without forcing
a database schema. Keep the skill usable without the Python helper.

Use independently authored fictional fixtures for every example or bug report.
Do not submit workspace exports, tokens, private URLs, customer names, or private
transcripts. Describe sensitive failures using the smallest fictional reproducer.

Before opening a pull request, run the unit tests and `python3 scripts/release_check.py`.
Add meaningful regression cases when changing evidence or confirmation behavior.
Update `MANIFEST.txt` deliberately when adding distributable files. The checker is
a heuristic; inspect the actual diff and release archive before publication.

For behavioral changes, include the request, cited evidence and observed outcome
from a fictional trial. Distinguish measured behavior from intended behavior.
For raw extraction, supply untagged prose and natural-language requests separately
from expected facts. Do not expose the answer labels or a recorded response to an
extractor in a fresh run. Record who authored the data and whether the run was
independent. A deterministic replay is not another LLM trial.
