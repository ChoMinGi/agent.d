# ReadingLight: research → design → QA

This is an entirely invented library pilot. No real customer documents, personal
data, Notion pages or company facts are included. `demo://` addresses identify
fictional sources; they are not network locations.

The raw documents were written by a separate agent. Each subsequent task was
performed by a fresh agent with the skill, sources available at that point, and
the previous stage's confirmed memory. Earlier conversations and prose answers
were not passed along. `requests.json` contains the natural task requests.
The research request also asks for a prototype brief; its research and supplemental
prototype tasks are both retained.

The coordinator used simulated confirmation to transfer each exact memory delta.
It did not simulate official authority: policy approval and release conditions
must be read from the fictional source documents. No real confirmation or external
write is represented by these files.

`snapshot.json`, `task.json`, `proposal.json`, `confirmation.json` and `result.md`
under each stage preserve the normalized evidence, request, proposed delta,
simulated receipt input and actual task answer. Public prose links are rewritten
from machine-specific paths to relative paths; their meaning is unchanged.
Plans and reuse reports make the handoffs inspectable. `trial.json` describes
review windows and source identities.

The author's hidden answer key was withheld from all task agents during the
study. It is published afterward as `author-expectations.json`. A separate reviewer
records semantic findings in `adjudication.json`; `replay-expectations.json`
contains grounded record/status checks for deterministic regression testing.
The author, task agents and semantic reviewer have distinct roles. This small
study has no baseline and does not establish time savings or general accuracy.

From the repository root:

```sh
python3 -B scripts/evaluate_handoff.py --output-dir work/handoff-replay
```

This checks sealed file hashes, raw text preservation, the plan/confirmation chain,
current record states and reuse traces, then writes inspectable plans and ledgers.
It does not run new agents or rescore the meaning of the prose. For a fresh study,
give agents only raw sources, the skill, their natural request and the prior
confirmed ledger; keep answers, existing results and later-stage sources hidden.

Read [the study methodology and limitations](../../docs/handoff-evaluation.md).
