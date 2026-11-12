# Willow Atlas — fictional v2 development case

All documents, organizations, participants, observations, dates and test runs are
invented for this repository. These are not anonymized customer exports.

Five raw documents mix an older decision, an unanswered question, an explicit
approved successor, a newer unapproved draft, a missing follow-up memo, a seven-row
table and a failed synthetic test. Three natural-language requests use the same
project and scope. Inputs have source provenance and native prose, not preassigned
task types/topics. The requests opt into `extraction_version: 2`.

The host-authored recorded extraction and expectations were written during
implementation by the same author. Replaying them is a deterministic development
check, not a new model evaluation or independent blind accuracy benchmark.

```sh
python3 -B skills/decisionguard/scripts/raw_context.py prompt \
  --bundle examples/willow-atlas/documents.json \
  --requests examples/willow-atlas/requests.json
python3 -B skills/decisionguard/scripts/raw_context.py prepare \
  --bundle examples/willow-atlas/documents.json \
  --requests examples/willow-atlas/requests.json \
  --extraction examples/willow-atlas/recorded-extraction.json \
  --request-id qa --format markdown
python3 -B scripts/evaluate_context_v2.py --output-dir work/willow-review
```

The replay selects 6 research, 11 design and 10 QA records. Old exact-location
publication and the answered grid-size question are historical; missing retention
authority stays unknown. The design quote for the device queue contains one table
row, with separate column headings, and excludes the adjacent free-trial interest.
QA preserves the failed run, missing tests and public-release approval boundary.
Budgets of 1, 4, 8 and 16 retain all seven priority facts in `selected` or the
explicit cited `attention` overflow, with `needs_context` when insufficient.

For a fresh evaluation, hide `recorded-extraction.json` and `expectations.json`
from the extracting agent. A genuinely new blind study needs new documents and
an independently sealed answer key; this now-public case is not unseen material.
