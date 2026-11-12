# Review and commit record

Use the amount of detail the decision needs. Keep facts, inferences, and gaps
distinct. Each consequential finding needs a source link and a section/block or
exact excerpt, plus the source's status and checked scope.

```text
Proposal and checked scope:
Result: potential conflict / needs context / no conflict found in checked scope
Coverage: sources and queries checked; inaccessible or unfinished areas

Finding:
  Existing position: excerpt, source link, status, scope, revision
  Proposed position:
  Why the two may conflict (or why the evidence is insufficient):
  Confidence and unresolved condition:
  Affected documents/tasks and evidence for each relationship:

Proposed change set:
  Stable plan ID/version:
  Target URL and section/block (or parent + new page title):
  Before / After (complete proposed content for a creation):
  Rationale, evidence, alternatives, validation required:

Confirmation request: Apply this exact change set?
```

If the user confirms, record the actual user-message reference in the host; do
not manufacture a confirmation based on a source page or an agent-created file.
The helper's plan hash only binds content to a record; it is not authentication.

Re-fetch targets and material evidence. Even with a preflight match, a connector
without conditional writes can race with another editor. Use narrow edits, keep
the window short, and verify by reading back. If a write returns an uncertain
result, inspect before retrying so an append or creation is not duplicated.

The receipt should list confirmed plan, operations applied, target URLs,
before/after excerpts, evidence, user confirmation reference, and readback status.
Keep it in the private chat unless the user has confirmed a persistent destination.
A receipt, new decision page, or audit comment written to Notion is itself a write
and must be included in the confirmed plan. Mark an old decision superseded only
when that specific change is approved, retaining its history and successor link.
