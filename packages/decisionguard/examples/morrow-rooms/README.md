# Morrow Rooms — raw-document demo

Every company, person, interview, rule and test observation in this fixture is
fictional. No real customer documents or Notion pages were used. The `demo://` URLs
are fixture identifiers. “Observed” describes the fictional scenario, not research
conducted on actual customers or competitors.

`raw/note-01.md` through `raw/note-07.md` contain plain prose without type/topic
tags. Filenames and titles are neutral. `documents.json` contains only export
provenance and file locations. The known project root is a boundary supplied by
the caller; we do not ask the model to infer access permissions from prose.
`requests.json` contains three natural-language Korean requests, with explicit
project/scope/time/budget but no predefined type or topic.

The extraction job contains six in-project documents and 19 paragraphs. The
seventh document belongs to a different project and is excluded before the host
sees the job. The agent produced 17 records, six cited dependencies, 19 paragraph
dispositions and three task interpretations. Raw prose mixes languages and includes:

- An accepted 24-hour cutoff, its superseded 12-hour predecessor, an unaccepted
  72-hour proposal and an unexplained “48 hours confirmed” screenshot.
- Interview evidence about finding a deadline, which does not establish demand
  for changing that deadline; a deliberately invented competitor comparison.
- An untested loss-reduction assumption and an open display-timezone question.
- Approved boundary behavior, server-clock design, a stale-preview risk, accepted
  tests, an observed failure without a retest, and planned remedial work.
- Unrelated snack/invoice topics, an enterprise-only rule and an embedded attempt
  to instruct the assistant to change decisions and publish documents.

| Natural-language request | Expected useful context | Recorded selection |
| --- | --- | ---: |
| Understand demand using user difficulties and other services | Interviews, comparison, goal/current policy, proposals and uncertainty | 8 |
| Prepare screen and processing-flow design | Accepted behavior and implementation, customer evidence, known failure, tests, dependencies | 13 |
| Gather evidence before a release check | Expected behavior, test plan versus observed result, known defect, implementation and remaining work | 12 |

All three return `needs_context`: the screenshot's authority is unknown. The QA
packet also preserves the failed boundary test and absent retest. Context assembly
does not issue release clearance. The stale-preview risk uses a different inferred
topic and reaches design/QA through a cited dependency. Other scope/topic/history
records are not selected as current applicable context.

## Reproduce or replace the recorded run

Run commands from the repository root as shown in the main README.
`recorded-extraction.json` is the current host agent's response, with a brief
run record in `extraction-run.json`. It is **output**, not pre-tagged input to a
fresh extraction. The Python pipeline cannot create that semantic response alone.

`expectations.json` is a separate, author-labeled answer file. Only evaluation
loads it. The evaluator checks selected fact anchors, kinds/statuses, task types,
omissions and exclusions; these are development-set checks. The same agent wrote
the fixture, expectations, extraction and implementation. No blind independent
model test is claimed.

To test another host run, give it only the skill, raw input and generated job.
Keep the answer file and recorded response out of its context. Save its new JSON,
then run `python3 -B scripts/evaluate_raw_context.py --extraction <response.json>`.
If any document, provenance or request changes, create a new extraction job and
response: the old digest must fail. A new fixture needs separately reviewed
expectations; do not change labels merely to fit incorrect output.

Checking citations cannot prove an inference. One negative test deliberately
promotes a draft using a real quote: structural checks allow it, but the separate
expected status catches the error. This makes the boundary explicit rather than
claiming that an exact quote mechanically proves approval.
