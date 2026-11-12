# Fictional walkthrough: ReadingLight

ReadingLight is an invented library pilot. All people, observations, decisions and
test results below are fiction. The source files were authored as demo material,
not derived from a private workspace. `demo://` identifiers in the recorded
artifacts are fixture references, not live Notion addresses.

This walkthrough shows the intended behavior. A recorded development study exists,
but neither that study nor these prompts establishes general accuracy or saved time.

## 1. Research from limited evidence

Open [the discovery note](../examples/readinglight-handoff/raw/stage-1.md): six
visitor interviews and two observations at one branch. Decision D-041 accepts an
individual seat-map prototype. It does not approve visitor deployment.

From the repository checkout, ask the installed skill:

```text
Use $decisionguard with examples/readinglight-handoff/raw/stage-1.md only.
Write a short research brief for the ReadingLight pilot: what the observations
support, what remains unknown, and what can inform a staff-only prototype.
Propose a small handoff for the next design task, but do not save it before I
confirm its exact content and destination. Do not use recorded results or answer keys.
```

Look for bounded local observations, an unverified broader-demand hypothesis,
and the missing weekend and screen-reader research. That research gap limits
demand claims; it does not prevent the authorized prototype design.

If you want to continue across a fresh agent, confirm the proposed handoff at a
private destination and pass that location to the next agent. Otherwise continue
with the sources without claiming that durable memory was created.

## 2. Carry an accepted change into design

Add [the design correspondence](../examples/readinglight-handoff/raw/stage-2.md).
Accepted D-052 explicitly replaces D-041: show only room-level availability bands
and an update time, marking information stale after ten minutes. Displays, storage
and analytics must not retain individual seat IDs or exact counts. A later seat-map
concept is a draft and does not replace D-052.

```text
Use $decisionguard to draft the ReadingLight feature design from raw/stage-1.md
and raw/stage-2.md under examples/readinglight-handoff/. Recheck the confirmed
handoff if I supplied one. Apply the current decision to the UI, storage and
analytics, and state what changed. Propose only the necessary memory delta;
do not persist changes without confirmation. Do not use recorded answers.
```

The design should now use bands rather than preserve the old seat-level model.
It should carry the unresolved research gap separately from prototype permission.
A history summary that mentions D-052 but still designs seat-level analytics has
not applied the change.

## 3. Hand off to QA without inventing a pass

Add [the build review](../examples/readinglight-handoff/raw/stage-3.md). The screen
and stale marker checks passed. Analytics still sends old seat-level fields;
its privacy check failed. The proposed patch has not been merged or retested,
and the accessibility check has not run. The release authority has not approved
visitor deployment.

Give a fresh agent the skill, all three raw documents and the confirmed handoff
location if you created one. It does not need the earlier agent's prose answers.

```text
Use $decisionguard to prepare the ReadingLight QA review from the three raw
stage documents in examples/readinglight-handoff/raw/. Recheck any confirmed
handoff I supplied. State the current expected behavior, known results, tests
still needed and what prevents visitor release. Do not treat the proposed patch,
a planned opening date or design approval as a passed test or release approval.
Do not use recorded answers or adjudications.
```

A useful result keeps the analytics failure, unrun accessibility check and absent
release approval visible while allowing preparation of the QA plan. It does not
ask the user to choose again between the settled seat-map and band decisions.

## Inspect or replay the recorded example

The [recorded handoff example](../examples/readinglight-handoff/README.md) includes
actual development-run outputs, source bindings and **simulated** confirmations.
Its [methodology](handoff-evaluation.md) explains limitations and corrections made
during that study. Do not read its expected answers before a fresh extraction.

```sh
python3 -B scripts/evaluate_handoff.py
```

This validates the saved records and replays the helper logic. It does not start
new agents, measure your editing effort or prove that the prompts above work
reliably across hosts. Confirmation simulation is restricted to fictional sources.
