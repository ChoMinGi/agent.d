# Unreleased

- Align the Korean README structure and version, host and license presentation with the other skills.
- Add a shared README presentation guide. Runtime instructions, helpers, version and license are unchanged.

---

# DecisionGuard v0.6.1

Focus the skill on completing the requested work with current decisions and
confirmed handoffs. Context-only requests still return a packet. Changed decisions
must affect recommendations and QA expectations, while unresolved inputs are tied
to the action they affect. Untagged prose can be read directly; full structured
extraction remains optional with its existing coverage and validation contract.

Clarify portable handoffs, confirmed destinations and reuse of an unchanged
confirmation. Current source access, evidence status and exact-change confirmation
for persistent memory or Notion writes remain required. Helpers and sealed
fictional recordings are unchanged. This is an instruction refinement, not a new
accuracy or user-effort benchmark.

---

# DecisionGuard v0.6.0

Carry confirmed judgments across tasks and agents. The new local handoff helper
shows exact memory changes, binds confirmation to the ledger and source state,
and rechecks current evidence before reuse. Prior approval cannot silently survive
supersession, conflicts, expiry or unavailable sources. Remembering an assumption
or planned test preserves its original status.

A wholly fictional ReadingLight study follows research, design and QA with three
fresh task agents and a separate fixture author. Confirmations are simulated;
recorded semantic review and reproducible replay are documented in
[the handoff evaluation](handoff-evaluation.md). This is one development case,
not a claim of general accuracy or measured time saving.

The helpers perform no model calls or external writes. Live memory, source
snapshots and receipts remain outside public source trees. Notion writes retain
the existing exact-change confirmation and readback protocol.

---

# DecisionGuard v0.5.0 — offline-validated alpha

- Version 2 raw requests require cited follow-up review for normative claims and
  questions, with explicit current, changed or unresolved outcomes.
- Markdown table rows retain exact source lines and column context independently.
- Relevant uncertainty, current goals, observed failures and approval boundaries
  are protected before ordinary context; cited priority overflow stays visible
  without exceeding the selected-record budget.
- Five new fictional Willow Atlas documents exercise research, design and QA,
  with budget-pressure and invalid-authority regressions. See
  [v2 validation](context-v2-evaluation.md) for results and limits.
- v1 input/response digests remain supported. Earlier blind-study artifacts stay
  sealed; current compatibility compares selected evidence by ID and permits new
  traces and ordering. No fresh blind study is claimed.

No private workspace data is included. No bundled model/API call, autonomous
Notion write, or GitHub publication was added. Concrete writes still need user
confirmation.

## Historical v0.4.1 notes


An open-source Agent Skill for preparing project context and reviewing proposed decisions against existing
Notion policies, decision records, and evidence.

- Prepare cited task context for market research, feature design, and QA review.
- Follow explicit prerequisites, retain draft/assumption labels, and expose gaps.
- Include a known failed test in both design and QA context.
- Independently author and freeze two new fictional corpora; keep answer keys hidden
  from four fresh extractors, then adjudicate source meaning in separate reviewer contexts.
- Preserve baseline failures and the improved trial regression in the public study.
- Retain bounded observations from incomplete sources, reconcile stale proposals,
  use task-specific relevance and distinguish planned tests from executed results.
- Correct a post-trial design-label warning without changing selected evidence.
- Extract evidence and task intent from untagged Korean/English prose using the
  host agent, then validate passage anchors and reuse the existing selector.
- Account for every supplied paragraph, bind responses to unchanged documents and
  requests, and preserve uncertain authority and failures without a retest.
- Include the fictional Morrow Rooms raw corpus, one recorded host extraction,
  three matched development cases and the original development recordings; the full suite now has 98 tests.
- Distinguish a recorded response replay from a fresh model run. General LLM
  extraction reliability and live connector performance remain unmeasured.
- Bootstrap existing workspace structure without imposing a new database schema.
- Explain potential conflicts, affected tasks, and missing evidence with citations.
- Present exact changes and require user confirmation before Notion writes;
  re-fetch evidence and verify results after applying confirmed changes.
- Run offline evidence checks, exact-value comparisons, and content-bound plan
  preflight using standard-library Python.
- Try the fully fictional Lantern Docs workspace and run regression tests.

This alpha contains no customer exports, real workspace identifiers, or credentials.
No backend, vector database, automatic write client, or marketplace package is
included. Live connector behavior and agent retrieval/conflict accuracy are not
yet measured. The helper does not prove semantic correctness or authenticate user
approval; those remain responsibilities of the host workflow and human review.

MIT licensed. Feedback should use fictional reproductions.
