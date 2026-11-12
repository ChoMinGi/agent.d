# v0.6.0 — confirmed context across tasks and agents

The new workflow remembers a user-confirmed set of evidence records, then checks
current sources before another task reuses them. It builds on the v0.5 selector;
it does not replace document authority with an agent's previous answer.

## Behavioral study

An independent author created ReadingLight, a wholly fictional library pilot,
as three short raw documents and a hidden evaluation map. Three fresh agents
handled research/prototype briefing, feature design, and QA in sequence. They
received the skill, only the raw documents available at their stage, and the
previous stage's approved ledger. They did not receive earlier chat history,
earlier prose answers, later documents, or the hidden evaluation map.

The coordinator simulated confirmation of each exact proposed memory delta.
Simulated approvals use `demo://` sources and are explicitly labeled. Source
policy authority comes from the fictional documents, not from these simulated
memory receipts. A separate reviewer assesses task answers against the author's
hidden facts after the stages finish.

The coordinator initially supplied a design review time before the second
document's dates. The design agent noticed this; the coordinator corrected the
fixture review date before the final design. The correction is preserved in the
study artifacts. This is a coordinator error, not evidence that future-dated
documents may establish earlier policy authority.

The QA agent and semantic reviewer encountered a temporary service usage limit.
Both resumed from their saved artifacts in the same separate agents. The QA agent
completed its own final answer with the original read restrictions; the coordinator
did not substitute a QA answer. After the interruption the coordinator read the
author key, but did not pass its answers or feedback to the QA agent.

This is one development study with a separate author and separate task agents,
not a controlled benchmark or a general accuracy estimate. File-read restrictions
were communicated in the agents' instructions, not enforced by separate operating
system accounts. The skill/helper received correctness fixes during development;
this was not a frozen before/after experiment. There was no no-skill comparison,
measured time saving, live connector trial, or real user's approval interaction.

## Observed results

The independent semantic reviewer completed 39 concrete checks: nine for research,
13 for design and 17 for QA, with no substantive failures in this case. Detailed
findings and caveats are preserved in the [adjudication](../examples/readinglight-handoff/adjudication.json).

| Stage | Current records selected | Previously confirmed records reused | Memory changes proposed |
| --- | ---: | ---: | ---: |
| Research / prototype brief | 8 | 0 | 8 additions |
| Feature design | 11 | 6 | 5 additions, 1 retirement update |
| QA | 19 | 9 | 10 additions |

Design replaces seat-level D-041 with accepted room-level D-052 and keeps the newer
contradictory concept as a draft. QA carries D-052 forward, catches prohibited
analytics despite passing display tests, and distinguishes failed Q-13 from unrun
Q-14, a proposed patch, and missing written release approval. Open interview
coverage remains separate from the release-critical execution gap.

All stages remain `needs_context`; that describes unresolved evidence, not a
failed handoff or a blanket prohibition on working. The answers identify which
actions can continue and which evidence is required before visitor release.
The review flags verbose audit material, conservative goal-authority warnings and
historical wording in unchanged rationales as usability caveats. The workflow now
explicitly calls for concise answers, separate audit artifacts, and labeling old
rationales as historical rather than preserving them just to maximize reuse.

The 149 automated tests (26 new handoff tests and one packaging regression) pass, as do the three-stage recorded
replay and prior context/decision examples. Test counts and this small semantic
review are not estimates of general extraction accuracy. The schema's `observed`
state alone also does not distinguish a test pass from failure; exact evidence,
attention annotations and host interpretation carry those outcomes.

## Reproducible checks

```sh
python3 -B -m unittest discover -s tests -q
python3 -B scripts/evaluate_handoff.py --output-dir work/handoff-replay
```

The evaluator verifies recording hashes and raw source preservation, rebuilds
each exact memory plan, checks its simulated confirmation, passes the resulting
ledger to the next stage, and checks current states/reuse traces. It saves readable
plans and local ledgers when an output directory is supplied. It does not run
agents again or independently judge the prose answers. The packaged adjudication
records that separate semantic review.

Unit tests additionally exercise declined/mismatched confirmation, changed plans,
changed source content/revisions, tampered receipts, stale or unavailable reads,
newly conflicting accepted decisions, supersession, expired or out-of-scope
prerequisites, and preservation of hypotheses and planned test states.

## Limits that matter in use

- Freshness and real permission are host responsibilities; timestamps and hashes
  do not authenticate a fetch or a person's consent.
- The memory file and receipts may contain private excerpts. They need the same
  access protection as the original sources; the helper is not multi-user ACL enforcement.
- A changed page conservatively invalidates reuse even if the edit seems unrelated.
  Current source evidence remains visible as current context, with its actual status.
- Memory confirmation never changes the source context packet or permits a write,
  deployment or broader sharing. An unverified assumption stays unverified.
- Exact excerpts and valid structures do not establish semantic entailment. The
  host must verify the actual relationship, authority, scope and follow-up evidence.
- No private workspace exports, actual project details or live Notion identifiers
  are used in the public fixture. No Notion writes or GitHub publishing were performed.
