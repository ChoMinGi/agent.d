# v0.5.0 context preparation checks

The v2 workflow adds explicit follow-up evidence, row-level Markdown table
passages, and priority checks that remain visible when a packet is too small.
Public validation uses wholly invented documents; no customer data is included.

## What changed

- New requests set `extraction_version: 2`. The host reviews each normative claim
  and question against applicable follow-ups, with exact evidence and a stated
  outcome. An explicit successor needs compatible scope and verified source
  availability. Resolved factual questions can cite observed evidence; proposed
  changes and completed tasks cannot impersonate approved rules or test results.
  Old/new citations appear as history when the current successor is selected.
- Markdown pipe tables split into a header and individual rows. Quotes and line
  numbers remain exact, including identical rows. Headers are preserved separately
  so a buying-intention row cannot leak into a product requirement quote.
  Fenced code is not treated as a table. The host still splits mixed claims within
  a row and normalizes HTML/merged tables when needed.
- Unknown states, open questions/risks, unverified assumptions, accepted goals and
  evidence-backed attention receive slots before ordinary context. Known failures
  and approval boundaries can carry explicit attention annotations. Any overflow
  stays visible at the top, with citations and `needs_context`, while `selected`
  still respects `max_items`. Excluded topics, unauthorized scopes and inactive
  records do not leak through this mechanism. A dropped cited prerequisite is
  named rather than hidden behind a general budget warning.

## Fictional replay

The [Willow Atlas case](../examples/willow-atlas/README.md) has five documents,
32 passages including seven table rows, and 17 extracted records.

| Request | Selected records | Missing labeled records | Unexpected records |
| --- | ---: | ---: | ---: |
| Market research | 6 | 0 | 0 |
| Feature design | 11 | 0 | 0 |
| QA review | 10 | 0 | 0 |

The host checked that the answered map-grid question did not erase the unexecuted
location check, that a newer draft did not override the approved review-and-consent
rule, and that the inaccessible retention memo remained a gap. Tests also reject
missing follow-up reviews, draft/self/incompatible successors, fabricated quotes,
adjacent-row quote contamination, and out-of-time authority.

| QA selected-record budget | Selected | Priority items in cited overflow | Priority items lost |
| --- | ---: | ---: | ---: |
| 1 | 1 | 6 | 0 |
| 4 | 4 | 3 | 0 |
| 8 | 8 | 0 | 0 |
| 16 | 10 | 0 | 0 |

Overflow is deliberate and disclosed. It is not a token-budget guarantee: the
user/host should narrow a broad task before downstream execution. The checks
also add 25 ordinary requirements and verify they do not displace the actual
failure, missing execution and approval boundaries from a 16-record packet.

## Reproduction and limits

```sh
python3 -B -m unittest discover -s tests -q
python3 -B scripts/evaluate_context.py
python3 -B scripts/evaluate_raw_context.py
python3 -B scripts/evaluate_context_v2.py
python3 -B scripts/evaluate_blind_context.py --compact
python3 -B scripts/release_check.py --require-git
```

The new corpus, extraction and expectations have the same author. These are
development cases and invariant checks, not independent accuracy measurements.
The replay scripts make no model calls. No new blind trial was run for v0.5.0.
Quote presence, source binding and review accounting cannot establish semantic
entailment: an unrelated quotation from the right page can still need human/host
correction. A regression test explicitly records this limitation.

The previous blind-study files and hashes are unchanged. Current replay checks
every historical selected field by record ID, allowing new trace fields and
priority ordering. Exact v0.4.1 packet equality is reported separately and is no
longer claimed. Historical study results are not recast as v0.5.0 results.

The Python helper does not search Notion or infer successors. Discovery and
interpretation are host-agent work guided by the skill. Writes still require
confirmation of the concrete change set. No public release is performed by these
checks or by the ZIP packager.
