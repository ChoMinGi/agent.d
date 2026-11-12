# Offline helper contract (v1)

Run from a repository checkout with Python 3.10+. The installed skill also works
without Python: the agent can follow the workflow with its connector.

```sh
python3 skills/decisionguard/scripts/decisionguard.py review \
  --snapshot examples/lantern-docs/snapshot.json \
  --proposal examples/lantern-docs/proposal.json
python3 skills/decisionguard/scripts/decisionguard.py plan \
  --snapshot examples/lantern-docs/snapshot.json \
  --edits examples/lantern-docs/edits.json
```

All commands read files and print JSON to stdout. They do not contact Notion,
change input files, apply patches, or authenticate approval. Exit 0 means the
command completed, **not** that a proposal is approved. Exit 2 means invalid input
or failed preflight. A conflict is a valid review result, so it returns exit 0.

## Snapshot

`schema_version: 1`, `coverage`, `sources`, `decisions`, and `impacts` are required.
Use the fictional fixture as a complete example.

| Field | Meaning |
| --- | --- |
| `coverage.scope` | Precisely bounded review scope |
| `coverage.complete` / `gaps` | Whether the stated retrieval scope was checked; not a claim about all workspace content |
| Source `id`, `title`, `url` | Stable local ID, original title, HTTPS source link (demo links for fiction only) |
| Source `revision`, `fetched_at` | Connector revision/edit timestamp and timezone-aware retrieval time |
| Source `content`, `complete` | Fetched body plus relevant properties as text, and whether needed content is complete |
| Decision `id`, `key`, `scope`, `value` | Unique ID and an explicitly normalized string value in an exact scope |
| Decision `status` | `accepted`, `draft`, `superseded`, `rejected`, `expired`, or `unknown` |
| Decision `source_id`, `quote`, `status_quote` | Source and exact excerpts supporting the claim and its status |
| Decision `superseded_by` | Required for superseded records; a supported accepted record with the same key and scope |
| Impact `decision_id`, `source_id`, `quote` | Explicit dependent evidence/task relationship and its excerpt |

Quotes must be present in the source. This validates traceability, not semantic
entailment: an unrelated excerpt would still pass the substring check. The agent
must inspect the meaning. Status, scope, exceptions, dates, units, and normalized
keys/values are agent-supplied interpretations and need evidence review. Multiple
sources can be represented as separate claim records. The helper does not infer
overlapping scopes, numeric inequalities, transitive dependencies, or time expiry.
For complex succession chains, supply the verified current successor and retain
the historical chain in the source excerpts; the helper accepts one direct edge.

## Proposal and output

For the additive `context` command and its optional snapshot extension, see
[context preparation](context.md). Existing v1 snapshots and commands remain valid.

A proposal has `summary` and a nonempty `claims` list containing `key`, `scope`,
and string `value`. One claim per key/scope. A different accepted value in exactly
the same scope creates a `potential_conflict`, with its source and status excerpt.
Drafts and superseded decisions cannot override an accepted record. Disagreeing
accepted values, unknown authority, incomplete relevant sources, and no accepted
match produce gaps. Findings and gaps can coexist; always read both.

The verdict is `potential_conflicts`, otherwise `needs_context` when there are
gaps, otherwise `no_conflict_in_checked_claims`. No verdict authorizes a mutation.

## Plans and confirmation records

Edits contain `changes`, each with `source_id`, exact `before` and `after`,
`rationale`, and nonempty `evidence_ids`. The helper supports one uniquely matched
nonempty replacement per target. Create/move/delete and complex block changes
remain connector-mediated plans using the skill's commit protocol. Resolve
snapshot gaps first; changing text cannot itself resolve missing evidence.

`plan` returns a content-bound `plan_id`, target revisions and content digests,
and a digest of all supplied evidence and interpretations. Retrieval timestamps
are excluded from the evidence digest. Save the output privately if needed.
After actual user confirmation, the host may record:

```json
{
  "plan_id": "the exact ID shown with the change set",
  "approved": true,
  "confirmed_by": "the confirming user in the host",
  "confirmation_reference": "the actual user-message reference"
}
```

Then fetch fresh evidence and run:

```sh
python3 skills/decisionguard/scripts/decisionguard.py check \
  --plan private/plan.json --snapshot private/fresh-snapshot.json \
  --approval private/approval.json
```

`check` rejects a missing/negative/mismatched confirmation record, changed plan,
or changed evidence. A successful result is **local preflight only**. A user or
agent can edit these files: this is not a cryptographic approval or access-control
system. The host is responsible for verifying the real user message and enforcing
connector permissions. Never generate an approval record to simulate a real user.
