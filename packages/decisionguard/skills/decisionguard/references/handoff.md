# Carry confirmed context into the next task

Use this workflow to resume from an existing confirmed handoff or when the user
wants a decision or correction remembered across tasks or agents. Memory is a
traceable index of reviewed claims, never a replacement authority. It can be a
source-linked note or the optional helper's ledger; JSON is not required for
ordinary work. Preserve the format of an existing helper ledger.

## Work with the user

1. At task start, locate the relevant handoff using the supplied project path or
   links. Read its record IDs and source bindings, check current access, then
   retrieve applicable sources and follow-ups. Use prior rationale only after
   verifying its basis. A missing or changed source invalidates automatic reuse;
   do not expose old private excerpts as a fallback. Use accessible current
   evidence and disclose the limit. No handoff means no claimed memory reuse.
2. During work, distinguish a suggestion, an observation, an accepted policy and
   execution evidence. Record a correction as a candidate with its source and
   scope. A newer proposal is not a successor until its authority is established.
3. Apply the verified context to the requested deliverable. A changed decision
   must change the affected design or QA expectation, not just a history summary.
   Complete work that does not depend on unresolved inputs. The user's explicit
   instruction for this task can guide that task immediately; it does not become
   organization-wide policy or durable memory without the appropriate authority.
4. When remembering is requested and there is a useful delta, show its exact
   additions, replacements or retirements, supporting sources and destination.
   Persist only the confirmed set; reuse an unchanged confirmation rather than
   asking again. Do not append another receipt just to say nothing changed.
   Recording a hypothesis preserves its unverified status. Confirmation does not
   authorize implementation, launch, publication or a wider audience.
5. Give the next agent the confirmed note or ledger, task request and authorized
   access to current sources. It must repeat the source check and select context
   for its own task. Disclose consequential changes and gaps, with brief reuse
   provenance where useful. The previous agent's chat is not required and its
   conclusions are not authority.

## Keep a small, portable handoff

Retain only claims that can affect a subsequent task. For each, preserve its
stable ID, claim and rationale, project/applicability, evidence status, source
link and section/excerpt, checked revision/time, and actual memory confirmation
reference. Include explicit predecessor/successor evidence when a decision changes.
For an unresolved item, record the affected action and next check. Keep old
decisions as labelled history; do not present them alongside successors as two
simultaneously active rules. The confirmation binds the proposed content and
destination, not every future edit of the note.

Keep the full audit trail separately. A short user-facing handoff can say which
current decision was applied, which change affected this result, and what remains
unverified. Omit empty categories. Do not require users to supply this schema or
rewrite their past explanations into it.

For example, in a fictional project an accepted decision D-12 allows three guest
seats; an explicit accepted D-19 replaces it with one. A subsequent design and QA
task uses one, updates its boundary cases, and keeps D-12 historical. A newer draft
suggesting five does not replace D-19. If the one-seat test has not run, retain
that execution gap while still drafting the QA cases. Remember these changes
only through the confirmed-memory workflow above. This example describes intended
behavior, not a measured outcome.

An unchanged excerpt or old review rationale can still mention a retired decision.
Label that wording as historical, or propose a correction if it would mislead the
next task. Do not preserve inaccurate rationale merely to increase the reuse count.
Keep the task answer concise; put detailed memory diffs and audit material in
separate artifacts so the user can inspect them when needed.

For uncertainties, name the action affected. A missing market-size estimate may
be deferred for a prototype but not for a market-size claim. An unrun release test
blocks release evidence, not the act of drafting a QA review. State why an item
blocks that action or can be deferred, and the next useful check; do not turn every
unknown into a request to stop. Keep the existing cited attention/overflow visible.

If a new decision needs to become official, use the existing exact-change Notion
commit protocol first. Re-fetch and verify the source afterward, then record the
result for reuse. The local ledger cannot confer official policy authority. An
authorized user's explicit decision can be a source where the workspace's own
authority rules permit it; preserve the actual confirmation, scope and conditions.

## Optional local helper

`scripts/handoff.py` consumes the normalized context snapshot from
[context preparation](context.md), including snapshots produced by raw extraction.
It does not extract prose or search sources. Keep all live snapshots, ledgers,
plans and receipts outside a public source tree; they can contain private excerpts.
The host must enforce permissions on both the sources and the ledger. Pass only
currently authorized sources for one project. An `access_scope` field, hash or
approval JSON is not authentication, proof of consent or an access-control system.

The helper prints JSON to standard output. Save to a new file, validate success,
then replace the local ledger; never redirect onto an input file or update it in
parallel. The plan binds the entire prior ledger and snapshot, so changed state
requires a new plan and confirmation. There is no concurrent file locking or
multi-system transaction. The helper performs no Notion writes.

For agent handoffs, read `entries` and their source bindings first; consult receipt
history only when needed for a change or audit. Do not dump the entire growing
ledger into a model's context. Recheck the source and preserve unchanged normalized
records; re-extract changed claims instead of reconstructing every prior record.

```sh
python3 scripts/handoff.py init --project-id fictional-project
python3 scripts/handoff.py plan --ledger ledger.json --snapshot snapshot.json \
  --proposal proposal.json --format markdown
python3 scripts/handoff.py plan --ledger ledger.json --snapshot snapshot.json \
  --proposal proposal.json
python3 scripts/handoff.py confirm --ledger ledger.json --snapshot fresh.json \
  --plan plan.json --confirmation confirmation.json \
  --refresh-started-at 2027-02-01T10:01:00Z --as-of 2027-02-01T10:02:00Z
python3 scripts/handoff.py resume --ledger ledger-next.json --snapshot fresh.json \
  --task task.json --refresh-started-at 2027-02-02T10:00:00Z
```

Paths are relative to the installed skill in these commands. `proposal.json`:

```json
{"summary":"Remember the reviewed context for the next task","record_ids":["D-1","H-1"]}
```

`confirmation.json` records consent the host has actually obtained:

```json
{"approved":true,"plan_id":"exact generated plan hash","mode":"user_attested",
 "confirmed_by":"authorized reviewer","confirmation_reference":"actual user message reference",
 "confirmed_at":"2027-02-01T10:00:00Z"}
```

`mode: simulation` is allowed only with `demo://` sources. It is for fictional
tests, never a substitute for real confirmation. Re-read after confirmation;
`fetched_at` must lie between `refresh_started_at` and `as_of`. These timestamps
are host attestations, not verified network activity. Content, authority, relations,
scope or revisions changing after confirmation causes the check to fail.

Memory entries retain the normalized claim, citations in its evidence fields,
source identities/hashes and dependency bindings. They preserve original status.
Receipts preserve the approved before/after changes. Full pages are not copied
into the ledger. Review all these artifacts before sharing them.

`resume` returns a fresh `context` packet from the existing selector plus:

- `reused_ids`: selected records unchanged since memory confirmation.
- `memory_trace`: applicable records reusable, retired, expired or needing review.
- `unconfirmed_current_ids`: current selected evidence without a matching memory
  confirmation; it may still be authoritative source context. Do not call it approved memory.
- `withheld_memory_count`: unavailable memories without their old IDs or excerpts.

Preserve current facts and uncertainty even when no old memory can be reused.
Changed source pages conservatively trigger review even when edits look unrelated.
Quote matching and hashes cannot prove meaning, approval authority, or exhaustive
follow-up discovery. Host review remains necessary.
